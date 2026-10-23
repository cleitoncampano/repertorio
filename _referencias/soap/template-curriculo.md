# template-curriculo: Template para Currículo Diferenciado (SOAP)

## O que é

Template de PowerPoint da SOAP para montar um currículo em slides, com duas versões (informal e formal), exportado para PDF a partir de `soap/templates/Template_Curriculo.pptx`. 20 páginas: capa do template, introdução, orientação sobre o perfil da audiência, sete slides da versão informal, banco de ícones, seis slides da versão formal, dica para a entrevista e duas páginas de divulgação. Sem data nem parceiros citados (logo antigo da SOAP).

## O que ensina

**Instruções de uso** (`editar-template-no-powerpoint`):
- "Lembre-se: os elementos em vermelho são apenas orientação de preenchimento e devem ser apagados ao fechar/ salvar seu currículo, ok?" (p2, texto exato).
- As páginas de orientação levam a etiqueta "Ao fechar seu arquivo, delete este slide!" (p2, p3, p4, p12, p18, p19, p20).
- Notas de preenchimento em etiquetas vermelhas manuscritas: "Se você não tiver mais que uma formação, apague o restante" (p6, p14); "Coloque seu nome em todos os slides" (p6); "Se não falar a língua, apague" (p7, p15); "Dê dois cliques na estrela e preencha, em preenchimento de forma, de acordo com o nível de conhecimento" (p7; "bolinha" na p15); "Se você ficou no mesmo cargo, apague este" (p9, p16); "Se não tiver, apague a coluna ou o slide" (p10, p17).
- Sumário do arquivo (p2): Perfil da audiência (slide 3), Perfil informal (slides 4 a 10), Perfil formal (slides 11 a 17), Dicas para quem foi aprovado (slide 18).

**Perfil da audiência antes do currículo** (`perfil-da-audiencia`, p3, p4, p12): antes de montar o currículo, pesquisar o perfil da empresa de interesse; entrar no site, descobrir missão, visão e valores e verificar se estão de acordo com as próprias expectativas (p3). O estilo do currículo segue o perfil da empresa: para empresa mais informal, mostrar que você compartilha desse perfil, com um conceito que sugere mais liberdade (p4); para empresa mais conservadora, slides com mais formalidade (p12).

**Estrutura do currículo em slides** (`curriculo-em-slides`), igual nas duas versões:

1. Capa (p5 informal, p13 formal): nome completo, "C.V. para a oportunidade: [nome do cargo]" e, na informal, o LinkedIn.
2. Dados pessoais e formação (p6, p14): idade, e-mail, telefone, endereço; formação acadêmica com até quatro blocos de instituição, curso e período.
3. Línguas e habilidades/competências (p7, p15): Inglês, Espanhol, Francês, Alemão; Word, Excel, Outlook e campos livres; nível em cinco estrelas (informal) ou cinco bolinhas (formal).
4. Outros interesses (p8, só informal): cinema, música, esporte, comida, livros, hobby, viagens.
5. Experiências (p9, p16): por empresa, logo, nome, período, 1º e 2º cargo e "Desafios e resultados". Pergunta-guia da versão formal: "Fale brevemente dos desafios que enfrentou e resultados que obteve neste cargo. Quais foram os principais obstáculos e como a empresa se beneficiou com o seu trabalho?" (p16).
6. Diferenciais (p10, p17): experiência no exterior, trabalho voluntário, premiações.
7. Banco de 32 ícones bônus (p11).
8. Depois do envio: "Foi chamado para a entrevista?" indica o e-book "10 dicas poderosas de linguagem corporal" (p18); "Passou? A vaga é sua?" pede para contar a experiência à SOAP (p19).

Diferença entre as versões: a informal usa fundo creme, cores (coral, verde-água, azul-marinho), círculos, títulos serifados e interesses pessoais; a formal usa papel branco texturizado, só preto, branco e cinza, faixas pretas e não tem o slide de interesses.

## Frases-chave

- "Na hora da seleção dos candidatos todos os cuidados contam, então porque não se diferenciar já na primeira fase?" (p2)
- "os elementos em vermelho são apenas orientação de preenchimento e devem ser apagados" (p2)
- "Antes de montar seu currículo, pesquise o perfil da empresa do seu interesse" (p3)
- "Entre no site, descubra a missão, visão e valores." (p3)
- "aproveite a oportunidade para mostrar que você compartilha desse perfil" (p4)
- "Quais foram os principais obstáculos e como a empresa se beneficiou com o seu trabalho?" (p16)
- "Ao fechar seu arquivo, delete este slide!" (p2)

## Linguagem visual do deck

- Paleta das páginas de orientação: preto #000000 e laranja #DF752A em faixa texturizada, etiquetas vermelhas #E0201B. Versão informal: creme #F3EEE8, coral #E77B79, verde-água #6DBDC4, azul-marinho #242A3B, ícones em verde, vermelho, amarelo e azul. Versão formal: papel branco #F6F6F6, preto, cinza #C4C4C4.
- Tipografia: títulos das orientações em sem serifa condensada negrito (laranja e preto); versão informal com títulos em serifada negrito de alto contraste; corpo em sem serifa geométrica (parece Century Gothic); notas em letra manuscrita branca sobre etiqueta vermelha.
- Modelos que se repetem: faixa laranja com fios pontilhados nas páginas pretas, rodapé "Seu Nome" em todas as páginas do currículo, círculos e semicírculos que saem da borda, ícones planos redondos com sombra longa.
- Marcante: a mesma estrutura em dois tons de formalidade, e as orientações escritas como etiquetas que se apagam.
- Falhas de exportação: nenhuma visível. Oito páginas sem texto extraível (p1-4, p12, p18-20): o texto está na imagem e foi lido pela imagem.

## Ficha do deck

```json
{"titulo":"Currículo em slides, versões informal e formal",
 "resumo":"Template de currículo em slides com a mesma estrutura (capa, contatos e formação, línguas e habilidades, experiências com desafios e resultados, diferenciais) em duas versões: informal colorida e formal em preto e branco.",
 "ideia":"Pesquise o perfil da empresa e escolha o tom visual do currículo de acordo: cores e formas soltas para quem é informal, preto e branco e faixas para quem é conservador.",
 "como_funciona":"As páginas pretas e laranja orientam e depois são apagadas; o currículo em si tem uma página por bloco de informação, com ícones, estrelas e arcos que permitem ler cada bloco de relance.",
 "intencoes":["APRESENTAR","AGRUPAR","COMPARAR"],
 "tecnicas":["similaridade","emprestimo-de-codigo","hierarquia-de-leitura","regiao-comum"],
 "movimento":["estatico"],
 "estetica":["claro","colorido","pastel"],
 "tom":["acolhedor","serio"],
 "forca":3,
 "bom_para":["currículo para processo seletivo","apresentação pessoal","perfil profissional em slides"],
 "capa":5}
```

## Repetições

- p18 divulga o e-book "10 dicas poderosas de linguagem corporal", material da SOAP que está em outro lote (`linguagem-corporal-dicas`); as telas mostradas são as dicas 8, 9 e a capa.
- Página de divulgação p20 ("Conheça os produtos SOAP", "Baixe outros materiais gratuitos", "Gostou? Compartilhe"): mesmo texto de `template-copa-do-mundo` p10, com outra imagem.
- O tema "perfil da audiência" (p3) dialoga com o e-book de audiência da SOAP de outro lote.

## Ids de conceito usados

- `curriculo-em-slides`: estrutura de currículo apresentado como slides (capa com cargo, contatos e formação, línguas e habilidades com nível, interesses, experiências com desafios e resultados, diferenciais) em versão informal e formal.
- `perfil-da-audiencia`: pesquisar a empresa ou o público (site, missão, visão, valores) antes de montar o material e ajustar o tom a esse perfil.
- `editar-template-no-powerpoint`: orientações de preenchimento em vermelho e slides a apagar ao fechar o arquivo.

## Páginas puladas ou duvidosas

- Nenhuma ilegível. p1 (capa do template), p2 (introdução), p4 e p12 (divisores) não foram selecionadas por serem orientação; as versões formais p14-17 repetem os modelos da informal; p18-20 são divulgação.
