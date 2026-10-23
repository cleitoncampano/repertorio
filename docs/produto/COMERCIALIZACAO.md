# Preparação comercial do Repertório

## Oferta da landing page em 23/10/2026

Decisão revista pelo Cleiton no mesmo dia: a compra leva só o aplicativo, com a biblioteca vazia. Cada pessoa monta a própria curadoria, enviando arquivos pelo app ou pedindo ao seu agente. A biblioteca de desenvolvimento não vai ao comprador: das cerca de 1.350 referências, só uma está marcada como livre para reutilizar, e parte delas vem de cursos pagos e de galerias de terceiros. A landing page precisa deixar de prometer biblioteca incluída. O valor de R$ 97 é provisório e fica editável; link de checkout e condições comerciais ainda não foram definidos.

Registro anterior, substituído: a compra incluiria o aplicativo e a biblioteca de referências do Cleiton (apresentações, materiais de estudo e vídeos de motion).

A landing page está no Growmate Marketing, em `produtos/repertorio/landing-page/`, com prévia privada em https://repertorio-para-criar.loyalmoon67.chatgpt.site. Fonte, direção e continuidade ficam naquela produção. A página demonstra o aplicativo com exemplos originais; a criação do pacote para entregar ao comprador é outra tarefa. O pacote de avaliação descrito abaixo continua sendo o candidato de software preparado em 19/10, sem o acervo particular.

## O produto a apresentar

Uma biblioteca visual local para pessoas e agentes de IA: referências com contexto, busca, mapa e revisão da direção antes da criação. [Definição do produto](PRODUTO.md).

Decisões do Cleiton em 19/10/2026: uso local pelo navegador em Mac e Windows; aplicativo opcional no Mac. O app e o navegador acessam a mesma biblioteca local. As produções ficam nos projetos de destino, separados do acervo.

## Explicação em quinze segundos

“O Repertório organiza as referências que eu quero usar e explica a ideia por trás delas. Meu agente consulta essa biblioteca, me mostra uma seleção e espera minha revisão antes de criar com a identidade da minha marca.”

## Explicação em um minuto

“Quando a gente cria com IA, precisa dar uma direção. No Repertório, eu reúno referências em espaços por marca, cliente ou tema. Cada ficha traz o que funciona naquela peça e como aplicar a ideia em outro contexto. Posso explorar pelo mapa ou pedir ao agente que busque referências para um trabalho. Ele me diz quais referências vai usar e por quê, eu abro cada uma no app, ajusto a direção e só depois ele cria no projeto da produção. O Repertório fica no meu computador e acumula referências e decisões para os próximos trabalhos.”

## Outras chamadas para testar

- “Dê à sua IA as referências que você escolheu.” Foco em quem já usa agentes.
- “Uma biblioteca de ideias para orientar o próximo trabalho.” Foco em organização e continuidade.

A chamada principal descreve o benefício; o fluxo de seleção e revisão demonstra como ele acontece. Os nomes técnicos ficam nos passos de conexão e operação.

## Público e oferta a validar

Público inicial: profissionais de marketing, designers, criadores e equipes que já produzem com agentes de IA. Essa é uma hipótese de posicionamento, ainda sem pesquisa de demanda ou validação de preço.

Primeira conversa: demonstração guiada de cinco minutos, seguida de uso com uma demanda e referências próprias do interessado. O [roteiro](DEMONSTRACAO.md) ajuda a mostrar o fluxo e a observar se a pessoa entendeu a função do produto.

Forma de contratação, preço, suporte, atualizações e acesso ao código-fonte ainda precisam de decisão do proprietário. Nenhum valor, plano, depoimento ou resultado financeiro foi inventado. As contas e ferramentas de IA são separadas do Repertório.

## A preparação entregue

- README orientado ao usuário, definição do produto e respostas às dúvidas básicas.
- Guia **Conheça o Repertório** dentro do aplicativo, com um exemplo de pedido, explicação do fluxo e ações reais para explorar e conectar um agente.
- Demonstração isolada com seis referências originais, dois espaços fictícios e uma demanda iniciada.
- Instalação local por scripts de Mac e Windows, com inicialização limpa e preservação de bibliotecas existentes.
- Empacotador que seleciona somente os arquivos do software e da documentação de produto.

Evidências e resultados de validação ficam em [app/VALIDACAO.md](../../app/VALIDACAO.md). A presença de um script ou de um workflow não equivale a uma execução aprovada no sistema de destino.

## O que faz parte do pacote de avaliação de 19/10/2026

O pacote de avaliação leva o software, a interface compilada, scripts de preparação e documentação de produto. A demonstração é gerada localmente com exemplos originais. Uma instalação nova começa vazia, com um vocabulário próprio de técnicas e intenções.

O pacote não leva banco real, histórico Git, backups, originais, mídias de cursos, fichas de desenvolvimento, carrosséis Growmate ou projetos de clientes. Perestroika e SOAP permanecem nesta biblioteca a pedido do Cleiton, para documentação em sessões futuras; não são apagadas nem empacotadas.

```sh
python3 ferramentas/empacotar_produto.py --destino /pasta-de-destino/repertorio-avaliacao.zip
```

O destino é explícito e fica fora do repositório. O pacote contém um inventário de arquivos e hashes. Ele é um candidato de avaliação interna, sem atribuir licença ao código ou autorizar redistribuição do acervo.

## Decisões reais antes da distribuição comercial

1. **Licença do Repertório.** As prévias de PDF passaram a usar pypdfium2 (BSD e Apache) em 23/10/2026; o produto não depende mais de bibliotecas com licença AGPL. As licenças do que vai no pacote estão em [AVISOS-DE-TERCEIROS.md](AVISOS-DE-TERCEIROS.md), gerado por `ferramentas/avisos_terceiros.py`. Falta escolher a licença ou o termo de uso do próprio Repertório: não foi aplicada uma licença MIT ou proprietária ao repositório.
2. **Entrega no computador do cliente.** Os testes do servidor e os iniciadores de instalação passaram em Mac e Windows hospedados, na [execução aprovada](https://github.com/cleitoncampano/repertorio/actions/runs/39272717798). Acompanhar também um piloto no computador de um cliente. Assinatura, notarização e um instalador completo do aplicativo do Mac são etapas diferentes do build local existente.
3. **Oferta e atendimento.** Definir preço, o que a pessoa recebe, suporte e política de atualizações, incluindo o que depende de agentes e serviços externos.

## Plano de validação, até noventa dias

| Período | Trabalho | Evidência para decidir |
| --- | --- | --- |
| Semanas 1 a 3 | Demonstrar para profissionais do público inicial e observar uma demanda real | A pessoa explica o produto e identifica uma situação em que o usaria |
| Semanas 4 a 6 | Acompanhar instalação, cadastro e primeira seleção com referências próprias | A pessoa chega à revisão e consegue continuar no projeto de produção |
| Semanas 7 a 9 | Definir oferta, licença, suporte e processo de instalação | Escopo, custo e responsabilidade de cada parte estão documentados |
| Semanas 10 a 12 | Fazer uma primeira venda acompanhada e registrar o uso | Instalação concluída, primeiro trabalho e dúvidas de atendimento registrados |

Esse plano é uma proposta de validação. Não cria compromissos comerciais nem inicia divulgação ou contato com terceiros.
