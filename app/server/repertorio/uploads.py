"""Arquivos enviados pela interface: cada arquivo vira uma referência publicada no espaço escolhido, com a ficha
marcada para o agente completar (ideia e como aplicar). Usa o mesmo registro e processamento dos agentes."""
import re
import shutil
import uuid
from pathlib import Path
from . import schemas
from .jobs import register
from .workspaces import Problem

UPLOADS={'.png','.jpg','.jpeg','.webp','.gif','.pdf','.pptx','.mp4','.mov','.webm'}
LIMIT=1024*1024*1024
# Texto da ficha até o agente escrever a explicação; o agente encontra essas fichas buscando por ele.
PENDING_IDEA='Ainda sem explicação. Peça ao seu agente para descrever a ideia desta referência e como aplicá-la.'


def safe_name(name):
    name=re.split(r'[\\/]',name or '')[-1].strip()
    stem,suffix=Path(name).stem,Path(name).suffix.lower()
    stem=re.sub(r'[^\w .()-]+','-',stem,flags=re.UNICODE).strip(' .-')[:100] or 'arquivo'
    return stem+suffix


def receive(lib,workspace_id,files):
    """files: lista de (nome, arquivo aberto). Devolve as operações de processamento, uma por arquivo."""
    lib.workspace(workspace_id)
    if not files:raise Problem(422,'Escolha ao menos um arquivo.')
    if len(files)>60:raise Problem(422,'Envie até 60 arquivos de cada vez.')
    names=[safe_name(name) for name,_ in files]
    refused=[n for n in names if Path(n).suffix not in UPLOADS]
    if refused:raise Problem(422,'Formato não aceito: '+', '.join(refused)+'. Envie imagens, PDF, PowerPoint ou vídeo.')
    root=lib.settings.home/'envios';root.mkdir(parents=True,exist_ok=True)
    project=lib.project(schemas.Project(name='Envios pelo app',root=str(root)))
    context=lib.start(schemas.StartContext(project_id=project['id'],demand='Arquivos adicionados pelo app',workspace_ids=[workspace_id]))
    operations=[]
    for name,(_,stream) in zip(names,files):
        folder=root/uuid.uuid4().hex;folder.mkdir()
        target=folder/name;size=0
        try:
            with target.open('wb') as out:
                for chunk in iter(lambda:stream.read(1024*1024),b''):
                    size+=len(chunk)
                    if size>LIMIT:raise Problem(413,f'{name} passa de 1 GB, o limite por arquivo.')
                    out.write(chunk)
            title=re.sub(r'[-_]+',' ',Path(name).stem).strip()[:240] or 'Arquivo'
            data=schemas.ReferenceData(title=title,description='Arquivo adicionado pelo app.',idea=PENDING_IDEA)
            operations.append(register(lib,schemas.Register(context_id=context['id'],target_workspace_ids=[workspace_id],request_key='app-'+folder.name,
                                                            data=data,files=[(folder/name).relative_to(root).as_posix()],user_requested=True)))
        except Exception:
            shutil.rmtree(folder,ignore_errors=True)
            raise
    return {'operations':operations,'context_id':context['id']}


def clean_up(settings,paths):
    """Depois do processamento, a cópia enviada sai da pasta de envios (o app já guardou a sua)."""
    root=(settings.home/'envios').resolve()
    for value in paths:
        p=Path(value).resolve()
        if p.is_relative_to(root) and p.parent!=root:
            p.unlink(missing_ok=True)
            if not any(p.parent.iterdir()):p.parent.rmdir()
