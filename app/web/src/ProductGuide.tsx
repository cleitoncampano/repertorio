import {ArrowUpRight,BookOpen,Layers,ListChecks,Monitor,Network,Search,Sparkles} from 'lucide-react';
import type {Workspace} from './types';
import {useQuery} from '@tanstack/react-query';
import {api} from './api';

type Props={workspace?:Workspace;onExplore:()=>void;onSearch:(query:string)=>void;onSkills:()=>void;onConnect:()=>void;onCopy:(text:string)=>void};
const steps=[
 ['01','Você traz a ideia','Um pedido, uma história, uma campanha ou algo que precisa explicar.'],
 ['02','O agente encontra referências','Ele consulta seu acervo e explica quais ideias podem servir ao trabalho.'],
 ['03','Você escolhe a direção','Aprove, corte e comente as referências na tela Escolhas.'],
 ['04','A criação acontece no seu projeto','O agente usa a direção aprovada e a identidade da sua marca.'],
];

export function ProductGuide({workspace,onExplore,onSearch,onSkills,onConnect,onCopy}:Props){
 const health=useQuery({queryKey:['health'],queryFn:()=>api<{demo?:boolean}>('/health'),staleTime:Infinity});
 const example=[
  'Quero criar uma capa de LinkedIn para apresentar minha empresa.',
  workspace?`Busque referências no espaço ${JSON.stringify(workspace.name)} do Repertório (workspace_id: ${workspace.id}).`:'Liste os espaços do Repertório e me pergunte quais usar como inspiração.',
  'Explique a ideia de cada referência e mostre a seleção em Escolhas. Espere minha revisão antes de criar.',
  'Siga a identidade da minha empresa e salve os rascunhos, imagens e arquivos finais no projeto desta produção.',
 ].join('\n\n');
 return <section className="collection-page product-page" aria-labelledby="product-title">
  <div className="product-intro"><span className="eyebrow">CONHEÇA O REPERTÓRIO</span>{health.data?.demo&&<span className="product-demo" role="status">Demonstração com exemplos originais e marcas fictícias.</span>}<h1 id="product-title">Suas referências, prontas para orientar a criação.</h1><p>Reúna referências visuais, entenda por que elas funcionam e use esse conhecimento com seu agente de IA para criar apresentações, páginas, posts e vídeos com a sua identidade.</p><div className="product-actions"><button className="product-primary" onClick={onExplore}>Explorar minhas referências <ArrowUpRight size={17}/></button><button onClick={onConnect}>Conectar meu agente</button></div><span className="product-platform"><Monitor size={16}/> Local no navegador, em Mac e Windows. No Mac, o aplicativo também é uma opção.</span></div>
  <div className="product-benefits">
   {[{icon:Layers,title:'Uma biblioteca para cada contexto',body:'Separe marcas, clientes e temas em espaços. Consulte o acervo adequado a cada demanda.'},{icon:BookOpen,title:'A ideia por trás da referência',body:'Cada ficha reúne contexto, técnica e uma explicação de como levar a ideia para outro trabalho.'},{icon:ListChecks,title:'Sua decisão antes da criação',body:'A seleção fica em Escolhas, com aprovações, cortes e comentários para orientar o agente.'}].map(item=><article key={item.title}><item.icon size={22}/><h2>{item.title}</h2><p>{item.body}</p></article>)}
  </div>
  <section className="product-section" aria-labelledby="product-flow"><div className="product-section-heading"><span className="eyebrow">DO PEDIDO À DIREÇÃO</span><h2 id="product-flow">Você participa das escolhas que definem o resultado.</h2></div><ol className="product-steps">{steps.map(([number,title,body])=><li key={number}><span>{number}</span><h3>{title}</h3><p>{body}</p></li>)}</ol></section>
  <section className="product-section product-example" aria-labelledby="product-example"><div><span className="eyebrow">EXPERIMENTE NA SUA CONVERSA</span><h2 id="product-example">Uma capa de LinkedIn começa com uma direção.</h2><p>Depois de conectar seu agente, copie este pedido para a conversa do projeto em que você vai produzir.</p><span className="product-space"><Layers size={16}/>{workspace?`Espaço de inspiração: ${workspace.name}`:'Você vai escolher os espaços com o agente.'}</span><button className="product-primary" onClick={()=>onCopy(example)}>Copiar exemplo de pedido <ArrowUpRight size={16}/></button></div><blockquote>{example.split('\n\n').map(line=><p key={line}>{line}</p>)}</blockquote></section>
  <section className="product-section" aria-labelledby="product-try"><div className="product-section-heading"><span className="eyebrow">OLHE DE PERTO</span><h2 id="product-try">Busque uma ideia. Abra a ficha. Entenda o recurso.</h2><p>Os resultados dependem das referências do espaço escolhido.</p></div><div className="product-searches">{[['escala','Contraste de tamanho'],['comparacao','Comparação'],['percurso','Percurso']].map(([query,label])=><button key={query} onClick={()=>onSearch(query)}><Search size={16}/>{label}<ArrowUpRight size={15}/></button>)}</div><button className="product-skills" onClick={onSkills}><Sparkles size={18}/><span><strong>Já sabe o que quer criar?</strong> Veja as skills e prepare um pedido para o agente.</span><ArrowUpRight size={17}/></button></section>
  <section className="product-section product-faq" aria-labelledby="product-questions"><div className="product-section-heading"><span className="eyebrow">ANTES DE COMEÇAR</span><h2 id="product-questions">O papel de cada parte fica claro.</h2></div>
   <details><summary>O Repertório cria os materiais?</summary><p>Seu agente de IA faz a criação. O Repertório fornece referências, contexto e as escolhas que você aprovou. Ferramentas, skills e contas de IA são configuradas separadamente.</p></details>
   <details><summary>O que eu posso guardar na biblioteca?</summary><p>Referências de apresentações, imagens, documentos e outros materiais, cadastradas pelo agente com explicação e contexto. Monte o acervo com materiais próprios ou autorizados. As possibilidades de reutilização ficam na ficha.</p></details>
   <details><summary>Como uso no Mac e no Windows?</summary><p>Nos dois sistemas, o serviço roda no computador e você acessa pelo navegador. No Mac, também pode abrir o aplicativo em uma janela própria. O aplicativo e o navegador acessam a mesma biblioteca local.</p></details>
   <details><summary>Onde ficam o acervo e as minhas criações?</summary><p>O acervo e sua curadoria ficam no computador. Rascunhos, imagens e entregas ficam no projeto de cada produção. Você escolhe quando incorporar um resultado à biblioteca.</p></details>
   <details><summary>Preciso de internet para usar?</summary><p>A consulta ao acervo local funciona com o serviço em execução. Instalação, ferramentas de IA e serviços externos podem precisar de internet. Quando você conecta um agente, o conteúdo que ele consulta segue também as regras desse serviço.</p></details>
  </section><div className="product-closing"><Network size={23}/><p>Seu repertório acumula referências e decisões para o próximo trabalho.</p><button onClick={onExplore}>Abrir a biblioteca <ArrowUpRight size={16}/></button></div>
 </section>;
}
