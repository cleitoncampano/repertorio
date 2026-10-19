#!/usr/bin/env python3
"""Opera a aba autenticada do Firefly no Chrome, sem ler credenciais.

python3 ferramentas/firefly.py status
python3 ferramentas/firefly.py generate --prompt-file pedido.txt
python3 ferramentas/firefly.py download --out imagem.png
"""
import argparse
import json
import shutil
import subprocess
import time
import uuid
from pathlib import Path


APPLE_SCRIPT = '''on run argv
  with timeout of 25 seconds
    tell application "Google Chrome"
      repeat with w in windows
        repeat with t in tabs of w
          if (URL of t) starts with "https://firefly.adobe.com/" then
            set URL of t to (item 1 of argv)
            repeat 80 times
              delay 0.05
              set responseText to execute t javascript "document.documentElement.getAttribute('data-pptreta-firefly-result') || ''"
              if responseText contains (item 2 of argv) then return responseText
            end repeat
            error "O Firefly não respondeu ao controle da página."
          end if
        end repeat
      end repeat
    end tell
  end timeout
  error "Abra uma aba do Firefly autenticada no Chrome."
end run'''

UI = '''
const nodes = () => {
  const roots = [document], found = [];
  for (let i = 0; i < roots.length; i++) for (const e of roots[i].querySelectorAll('*')) {
    found.push(e);
    if (e.shadowRoot) roots.push(e.shadowRoot);
  }
  return found;
};
const releaseClosedIntro = () => {
  let count = 0;
  for (const e of nodes()) {
    if (e.tagName === 'SP-OVERLAY' && e.open === false && e.state === 'closed' &&
        e.getRootNode().host?.tagName === 'FIREFLY-INTRO-MODAL-DIALOG' && e._focusTrap?.active) {
      e._focusTrap.deactivate({returnFocus: false});
      count++;
    }
  }
  return count;
};
'''


def run_ui(body):
    request = uuid.uuid4().hex
    code = ("javascript:void((()=>{try{" + UI + "const result=(()=>{" + body +
            "})();document.documentElement.setAttribute('data-pptreta-firefly-result',JSON.stringify({request:" +
            json.dumps(request) + ",ok:true,result}));}catch(e){document.documentElement.setAttribute(" +
            "'data-pptreta-firefly-result',JSON.stringify({request:" + json.dumps(request) +
            ",ok:false,error:String(e)}));}})())")
    response = subprocess.run(['/usr/bin/osascript', '-e', APPLE_SCRIPT, code, request],
                              capture_output=True, text=True, timeout=30)
    if response.returncode:
        raise RuntimeError(response.stderr.strip() or 'O Chrome não respondeu.')
    payload = json.loads(response.stdout)
    if not payload['ok']:
        raise RuntimeError(payload['error'])
    return payload.get('result')


def status():
    return run_ui('''
      const all = nodes();
      return {
        generating: all.some(e => e.id === 'generate-button' && e.pending),
        settings: all.filter(e => e.tagName === 'SP-PICKER').map(e => ({id:e.id,value:e.value})),
        promptLength: all.find(e => e.getAttribute('aria-label') === 'Prompt')?.textContent.length || 0,
        images: all.filter(e => e.tagName === 'IMG' && e.getBoundingClientRect().width > 200)
          .map(e => ({width:e.naturalWidth,height:e.naturalHeight,description:e.alt})),
        closedIntroCapturingFocus: all.some(e => e.tagName === 'SP-OVERLAY' &&
          e.open === false && e.state === 'closed' && e._focusTrap?.active &&
          e.getRootNode().host?.tagName === 'FIREFLY-INTRO-MODAL-DIALOG')
      };
    ''')


def generate(args):
    prompt = args.prompt_file.read_text(encoding='utf-8').strip()
    if not prompt:
        raise ValueError('O arquivo de descrição está vazio.')
    if status()['generating']:
        raise RuntimeError('Já existe uma geração em andamento. Não foi enviada outra.')
    run_ui('releaseClosedIntro(); return true;')
    # A resolução deve mudar antes da proporção: as dimensões das opções dependem dela.
    for picker_id, option_id in [('model', 'adobe:firefly:colligo:image5'),
                                  ('output-resolution', args.resolution), ('size', args.ratio)]:
        run_ui('''
          const all = nodes();
          const picker = all.find(e => e.tagName === 'SP-PICKER' && e.id === __PICKER_ID__);
          const option = all.find(e => e.tagName === 'SP-MENU-ITEM' && e.id === __OPTION_ID__);
          if (!picker || !option) throw new Error('Opção de geração indisponível.');
          picker.value = option.value;
          picker.dispatchEvent(new Event('change',{bubbles:true,composed:true}));
          return true;
        '''.replace('__PICKER_ID__', json.dumps(picker_id)).replace('__OPTION_ID__', json.dumps(option_id)))
        time.sleep(0.12)
    run_ui('''
      const field = nodes().find(e => e.tagName === 'FIREFLY-MENTION-TEXT-FIELD');
      if (!field) throw new Error('O editor do Firefly mudou. Confira o controle antes de gerar.');
      const content = [{type:'text',value:PROMPT}];
      field.content = content;
      field.dispatchEvent(new CustomEvent('fragmentsChanged',{
        bubbles:true,composed:true,detail:{getContent:()=>content}
      }));
      return true;
    '''.replace('PROMPT', json.dumps(prompt)))
    time.sleep(0.15)
    if args.prepare_only:
        return {'prepared': True, **status()}
    run_ui('''
      releaseClosedIntro();
      const button = nodes().find(e => e.id === 'generate-button');
      if (!button || button.disabled || button.pending) throw new Error('Gerar indisponível.');
      button.click();
      return {generationRequested:true};
    ''')
    time.sleep(0.4)
    return status()


def download(args):
    destination = args.out.resolve()
    if destination.exists():
        raise FileExistsError('O destino já existe; escolha outro nome.')
    downloads = Path.home() / 'Downloads'
    before = set(downloads.iterdir())
    run_ui('''
      releaseClosedIntro();
      const buttons = nodes().filter(e =>
        e.getAttribute('data-testid') === 'thumbnail-button-download' && e.getBoundingClientRect().width);
      if (!buttons[INDEX]) throw new Error('Resultado de imagem indisponível para download.');
      buttons[INDEX].click();
      return true;
    '''.replace('INDEX', str(args.index)))
    deadline = time.monotonic() + 45
    while time.monotonic() < deadline:
        results = [p for p in downloads.iterdir() if p not in before and
                   p.name.startswith('Firefly_') and p.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp'}]
        if len(results) > 1:
            raise RuntimeError('Mais de um download novo do Firefly; selecione o arquivo manualmente.')
        if results and results[0].stat().st_size > 0:
            size = results[0].stat().st_size
            time.sleep(0.3)
            if results[0].stat().st_size == size:
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(results[0], destination)
                return {'saved': str(destination), 'bytes': size}
        time.sleep(0.25)
    raise TimeoutError('O download não terminou. Confira os avisos visíveis do Firefly.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('status')
    creation = sub.add_parser('generate')
    creation.add_argument('--prompt-file', type=Path, required=True)
    creation.add_argument('--resolution', choices=['1K', '2K'], default='2K')
    creation.add_argument('--ratio', choices=['portrait', 'square', 'widescreen'], default='portrait')
    creation.add_argument('--prepare-only', action='store_true', help='Confere o preenchimento sem gerar ou consumir créditos.')
    transfer = sub.add_parser('download')
    transfer.add_argument('--out', type=Path, required=True)
    transfer.add_argument('--index', type=int, default=0)
    args = parser.parse_args()
    result = status() if args.command == 'status' else generate(args) if args.command == 'generate' else download(args)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
