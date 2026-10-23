import hashlib
import json
import os
import shutil
import sqlite3
import tempfile
import zipfile
from contextlib import closing
from pathlib import Path
from .locking import lock_file


def backup(settings,destination):
    destination=Path(destination).resolve()
    if destination.is_relative_to(settings.home):raise ValueError('Salve o backup fora da pasta de dados.')
    destination.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='repertorio-backup-') as tmp:
        snapshot=Path(tmp)/'library.sqlite3'
        with closing(sqlite3.connect(settings.db)) as source,closing(sqlite3.connect(snapshot)) as target:source.backup(target)
        with closing(sqlite3.connect(snapshot)) as db:
            paths={Path(r[0]) for r in db.execute('SELECT path FROM assets')}
        files={'library.sqlite3':snapshot}
        external=[]
        for p in paths:
            if p.is_relative_to(settings.home) and p.is_file():files[p.relative_to(settings.home).as_posix()]=p
            elif not p.is_relative_to(settings.home):external.append(str(p))
        manifest={'version':1,'root':str(settings.root),'home':str(settings.home),'external_files':sorted(external),'checksums':{}}
        temporary=destination.with_suffix(destination.suffix+'.tmp')
        with zipfile.ZipFile(temporary,'w',compression=zipfile.ZIP_DEFLATED) as archive:
            for name,p in files.items():
                h=hashlib.sha256()
                with p.open('rb') as f,archive.open(name,'w') as out:
                    for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk);out.write(chunk)
                manifest['checksums'][name]=h.hexdigest()
            archive.writestr('manifest.json',json.dumps(manifest,ensure_ascii=False))
        temporary.replace(destination)
    return {'backup':str(destination),'managed_files':len(files)-1,'external_originals':len(external)}


def known_versions(db):
    """Recusa backup de uma versão mais nova do app: o banco teria estrutura que esta versão não conhece."""
    from alembic.config import Config
    from alembic.script import ScriptDirectory
    script=ScriptDirectory.from_config(Config(str(Path(__file__).resolve().parents[1]/'alembic.ini')))
    row=db.execute('SELECT version_num FROM alembic_version').fetchone()
    if row and row[0] not in {r.revision for r in script.walk_revisions()}:
        raise ValueError('Este backup é de uma versão mais nova do Repertório. Atualize o app antes de restaurar.')


def restore(settings,source):
    lockpath=settings.home.parent/(settings.home.name+'.lock')
    lockpath.parent.mkdir(parents=True,exist_ok=True)
    with lockpath.open('a+b') as lock:
        try:lock_file(lock)
        except BlockingIOError:raise ValueError('Encerre o serviço antes de restaurar o backup.')
        with tempfile.TemporaryDirectory(dir=settings.home.parent,prefix='repertorio-restore-') as tmp:
            stage=Path(tmp)/'data';stage.mkdir()
            with zipfile.ZipFile(source) as archive:
                manifest=json.loads(archive.read('manifest.json'))
                if manifest.get('version')!=1:raise ValueError('Versão de backup não suportada.')
                if 'library.sqlite3' not in manifest['checksums']:raise ValueError('Banco ausente no backup.')
                for name,digest in manifest['checksums'].items():
                    p=(stage/name).resolve()
                    if not p.is_relative_to(stage) or name not in archive.namelist():raise ValueError('Caminho inválido no backup.')
                    if name!='library.sqlite3' and not name.startswith('assets/'):raise ValueError('Conteúdo inesperado no backup.')
                    p.parent.mkdir(parents=True,exist_ok=True)
                    h=hashlib.sha256()
                    with archive.open(name) as src,p.open('wb') as out:
                        for chunk in iter(lambda:src.read(1024*1024),b''):h.update(chunk);out.write(chunk)
                    if h.hexdigest()!=digest:raise ValueError('Checksum inválido: '+name)
            with closing(sqlite3.connect(stage/'library.sqlite3')) as db,db:
                if db.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise ValueError('Banco corrompido.')
                known_versions(db)
                for aid,value in db.execute('SELECT id,path FROM assets').fetchall():
                    p=Path(value)
                    if p.is_relative_to(Path(manifest['home'])):p=settings.home/p.relative_to(Path(manifest['home']))
                    elif p.is_relative_to(Path(manifest['root'])):p=settings.root/p.relative_to(Path(manifest['root']))
                    db.execute('UPDATE assets SET path=? WHERE id=?',(str(p),aid))
                db.execute("UPDATE operations SET state='failed',error='Restaurado de backup. Confira arquivos de origem antes de tentar novamente.' WHERE state IN ('queued','running')")
            previous=None
            if settings.home.exists():
                import time
                previous=settings.home.with_name(settings.home.name+'.before-restore-'+str(time.time_ns()))
                settings.home.rename(previous)
            try:stage.rename(settings.home)
            except Exception:
                if previous:previous.rename(settings.home)
                raise
    return {'restored':str(settings.home),'previous':str(previous) if previous else None}


def backup_dir(settings):
    """Pasta das cópias semanais. REPERTORIO_BACKUP_DIR escolhe o lugar (outro disco, iCloud, OneDrive).
    Sem ela, as cópias ficam ao lado da pasta de dados, no próprio computador; quem já guardava no iCloud Drive continua lá.
    Nada vai para a nuvem sem a pessoa escolher."""
    if os.getenv('REPERTORIO_BACKUP_DIR'):return Path(os.environ['REPERTORIO_BACKUP_DIR']).expanduser()
    icloud=Path.home()/'Library/Mobile Documents/com~apple~CloudDocs/Backups/Repertório'
    if any(icloud.glob('repertorio-*.zip')):return icloud
    # Instalação antiga (dados em app/.runtime) usa app/backups; as novas, "Repertorio Backups" ao lado dos dados.
    return settings.home.parent/('backups' if settings.home.name=='.runtime' else settings.home.name+' Backups')


def before_upgrade(settings):
    """Cópia automática antes de atualizar o banco para uma versão nova do app. Devolve o caminho ou None."""
    from datetime import datetime
    if not settings.db.exists():return None
    from alembic.config import Config
    from alembic.script import ScriptDirectory
    head=ScriptDirectory.from_config(Config(str(Path(__file__).resolve().parents[1]/'alembic.ini'))).get_current_head()
    with closing(sqlite3.connect(settings.db)) as db:
        try:current=db.execute('SELECT version_num FROM alembic_version').fetchone()
        except sqlite3.OperationalError:return None
    if not current or current[0]==head:return None
    target=backup_dir(settings)/f"repertorio-antes-da-atualizacao-{datetime.now().strftime('%Y-%m-%d-%H%M%S')}.zip"
    return backup(settings,target)['backup']


def backup_now(lib,target,keep=6):
    """Uma cópia da curadoria (banco e criações) e do histórico do projeto; guarda só as mais recentes."""
    import subprocess
    from datetime import datetime
    target.mkdir(parents=True,exist_ok=True)
    stamp=datetime.now().strftime('%Y-%m-%d-%H%M%S')
    result=backup(lib.settings,target/f'repertorio-{stamp}.zip')
    if (lib.settings.root/'.git').exists():
        done=subprocess.run(['git','-C',str(lib.settings.root),'bundle','create',str(target/f'repertorio-{stamp}.bundle'),'--all'],capture_output=True,text=True)
        result['history']=str(target/f'repertorio-{stamp}.bundle') if done.returncode==0 else 'falhou: '+done.stderr.strip()[-200:]
    for pattern in ('repertorio-*.zip','repertorio-*.bundle'):
        for old in sorted(target.glob(pattern))[:-keep]:old.unlink()
    with lib.db.engine.begin() as conn:lib.db.log(conn,'backup_created',**result)
    return result


def weekly(lib,stop,every=7*86400):
    """Confere a cada 6 horas; faz a cópia quando a última tem mais de uma semana (ou ainda não existe)."""
    import logging
    import time
    while not stop.is_set():
        target=backup_dir(lib.settings)
        try:
            latest=max((p.stat().st_mtime for p in target.glob('repertorio-*.zip')),default=0)
            if time.time()-latest>every:backup_now(lib,target)
        except Exception:
            logging.exception('Backup semanal falhou; nova tentativa em 6 horas.')
        stop.wait(6*3600)
