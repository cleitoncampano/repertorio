import hashlib
import json
import os
import shutil
import sqlite3
import tempfile
import zipfile
from pathlib import Path


def backup(settings,destination):
    destination=Path(destination).resolve()
    if destination.is_relative_to(settings.home):raise ValueError('Salve o backup fora da pasta de dados.')
    destination.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='repertorio-backup-') as tmp:
        snapshot=Path(tmp)/'library.sqlite3'
        with sqlite3.connect(settings.db) as source,sqlite3.connect(snapshot) as target:source.backup(target)
        with sqlite3.connect(snapshot) as db:
            paths={Path(r[0]) for r in db.execute('SELECT path FROM assets')}
        files={'library.sqlite3':snapshot}
        external=[]
        for p in paths:
            if p.is_relative_to(settings.home) and p.is_file():files[str(p.relative_to(settings.home))]=p
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


def restore(settings,source):
    import fcntl
    lockpath=settings.home.parent/(settings.home.name+'.lock')
    lockpath.parent.mkdir(parents=True,exist_ok=True)
    with lockpath.open('a') as lock:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
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
            with sqlite3.connect(stage/'library.sqlite3') as db:
                if db.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise ValueError('Banco corrompido.')
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
