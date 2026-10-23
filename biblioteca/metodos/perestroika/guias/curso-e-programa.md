# Curso e programa

Vários encontros que formam uma jornada: curso, trilha de treinamento, programa de onboarding, imersão de vários dias, escola corporativa. Escolha este guia para desenhar o todo e propor o programa; cada encontro depois segue `aula-e-workshop`.

Base: Experience Learning (escola Perestroika) e o catálogo de cursos In Company. Fichas em `get_guide("perestroika/<ficha>")`.

## No método

- **Arco.** O curso conta uma história principal ao longo dos encontros, como a temporada de uma série: cada aula tem histórias próprias, mas em todas a tese do curso avança (`perestroika/arco`).
- **Framework de curso.** O programa é desenhado em blocos por tipo de encontro: check-in, conceitos, ferramentas (how to), vivencial, cases e master class, connecting dots e check-out, projeto e banca. No curso Empreendedorismo Criativo, 15 aulas: 1 check-in, 3 conceitos, 2 vivenciais, 3 ferramentas, 3 cases, 2 de conexão e check-out, 1 de projeto e banca, com um checkpoint depois da nona aula (`perestroika/framework-de-curso`).
- **Mapa conectivo.** Alguém costura as aulas para o curso não virar "colcha de retalhos": um regente que assina o curso, um conector, um report de melhores momentos na manhã seguinte (`perestroika/mapa-conectivo`).
- **Checkpoint.** Se o fio se perde, uma aula extra amarra o que veio antes; pode já estar prevista (`perestroika/checkpoint`).
- **Vínculo e prática.** Aula inaugural, happy hour e festa final com datas reservadas desde o início, projeto real com banca no fim (`perestroika/aula-inaugural`, `perestroika/happy-hour-festa-final`, `perestroika/projetos-banca-go-pro`).

## Passo a passo

1. **Tese do curso e tagline.** Uma tese por curso, uma por módulo e uma por aula (`perestroika/tese`, `perestroika/ficha-de-tese`).
2. **Perguntas e instrumentos por aula.** Uma tabela com a pergunta que cada aula responde e o instrumento que a turma leva (`perestroika/entrega-minima-e-dia-seguinte`). Se duas aulas respondem a mesma pergunta, junte; se uma pergunta da tese não tem aula, falta um encontro.
3. **Framework.** Distribua as aulas pelos blocos de `perestroika/framework-de-curso`, preenchendo o modelo `perestroika/grade-de-curso`. Não copie o modelo: um workshop intensivo e prático pode não ter bloco de conceitos. Garanta pelo menos um encontro de fazer (ferramentas, vivencial ou projeto) a cada dois de ouvir.
4. **Costura.** Defina quem faz o papel de regente ou conector, onde fica o checkpoint e como cada aula retoma a anterior (`perestroika/mapa-conectivo`).
5. **Formato e horas.** Escolha entre presencial, ao vivo online, gravado, híbrido ou palestra, e as horas de cada um (`perestroika/formatos-de-encontro`).
6. **Proposta.** Escreva o programa no padrão do catálogo: promessa em uma linha, público, módulos com uma frase por aula, formato e horas, entregas (`perestroika/proposta-de-programa`).

## Formato da entrega

```markdown
# <Nome do programa>
Promessa: <uma linha>        Público: ...        Formato e horas: ...
Tese do curso: ...           Tagline: "..."
Arco: de <onde a turma começa> a <onde termina>.

| # | aula | bloco do framework | pergunta que responde | instrumento que leva | treco |
|---|---|---|---|---|---|
Checkpoint: depois da aula N.   Costura: <regente/conector, report>.
Vínculo: aula inaugural, happy hour (datas), festa final.
Projeto final e banca: ...
```

## Erros que derrubam

- Lista de temas sem arco: cada aula é boa, o curso não chega a lugar nenhum.
- Mesmo framework para qualquer programa ("seria uma armadilha", diz o material).
- Programa que só expõe: sem ferramentas, vivencial ou projeto, não há dia seguinte.
- Check-in e check-out espremidos dentro de outras aulas, sem tempo próprio.
- Proposta que descreve conteúdo em vez de promessa e entrega.

## Prompt base

> Desenhe um programa de <N> encontros de <duração> para <público> sobre <tema>, seguindo o guia `curso-e-programa` do Repertório. Defina a tese e a tagline do curso, o arco, a tabela por aula (pergunta que responde, instrumento que leva, bloco do framework), onde fica o checkpoint e como as aulas se costuram. Feche com a proposta no padrão de `perestroika/proposta-de-programa`.

## Fichas para abrir, nesta ordem

`perestroika/arco`, `perestroika/framework-de-curso`, `perestroika/grade-de-curso`, `perestroika/entrega-minima-e-dia-seguinte`, `perestroika/mapa-conectivo`, `perestroika/checkpoint`, `perestroika/formatos-de-encontro`, `perestroika/proposta-de-programa`. Para educação corporativa: `perestroika/escola-corporativa`.

## Referências para abrir primeiro

- [Mapa do curso em blocos numerados](http://127.0.0.1:8766/?workspace=0cbf5669-0d0a-4745-844e-0745357c0419&ref=perestroika-06-estrutural%2312) e [o mesmo mapa com outro item em destaque](http://127.0.0.1:8766/?workspace=0cbf5669-0d0a-4745-844e-0745357c0419&ref=perestroika-06-estrutural%2329): um único desenho que volta a cada capítulo.
- [Rascunho à mão do framework do Yakuza](http://127.0.0.1:8766/?workspace=0cbf5669-0d0a-4745-844e-0745357c0419&ref=perestroika-06-estrutural%2314): o programa sendo construído em cartolina.
- [Linha que costura retalhos coloridos](http://127.0.0.1:8766/?workspace=0cbf5669-0d0a-4745-844e-0745357c0419&ref=perestroika-03-conteudo%2332): a metáfora do mapa conectivo.
- [Tabela de perguntas por aula](http://127.0.0.1:8766/?workspace=0cbf5669-0d0a-4745-844e-0745357c0419&ref=perestroika-03-conteudo%2321) e [tese do curso com grade aula a aula](http://127.0.0.1:8766/?workspace=0cbf5669-0d0a-4745-844e-0745357c0419&ref=perestroika-04-forma%2333).
- [Peres In Company · Catálogo de cursos](http://127.0.0.1:8766/?workspace=0cbf5669-0d0a-4745-844e-0745357c0419&ref=perestroika-perestroika-catalogo-cursos-incompany): como cada curso é apresentado numa proposta.
