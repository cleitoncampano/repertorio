# Comunicação na empresa

Peças e conversas para dentro da empresa: anunciar uma mudança, falar com a equipe numa crise, dar feedback, ganhar credibilidade como líder, receber quem chega, atrair e manter pessoas, conduzir e avaliar um treinamento. Escolha este guia quando a audiência é a própria equipe ou os candidatos, e a peça é apresentação, comunicado, conversa ou treinamento. O resultado é um plano de comunicação (ou o roteiro da conversa), não só um slide bonito.

Base: e-books da agência SOAP com o GPTW, a Michael Page e outros parceiros (comunicação interna, credibilidade do líder, feedback, segurança para falar a verdade, guia completo do RH, facilitação e avaliação de treinamentos). Fichas em `get_guide("soap/<ficha>")`.

## Escolha pela situação

| situação | abra | modelo |
|---|---|---|
| Anunciar uma mudança, uma meta, um resultado para a equipe | `soap/comunicacao-interna` | `soap/plano-de-comunicacao-interna` |
| Crise: demissões, greve, queda de vendas, notícia ruim | `soap/comunicacao-na-crise` | `soap/plano-de-comunicacao-interna` |
| Conversa de feedback, de reforço ou de correção | `soap/conversa-de-feedback` | `soap/roteiro-de-feedback` |
| Líder novo, ou líder em quem a equipe não acredita | `soap/credibilidade-do-lider` | |
| A equipe esconde problemas e não discorda | `soap/seguranca-psicologica` | |
| Receber quem chega (primeiro dia ao primeiro ano) | `soap/onboarding` | `soap/plano-de-onboarding` |
| Atrair, recrutar e manter pessoas; marca empregadora | `soap/ciclo-de-talentos` | |
| Conduzir um treinamento | `soap/facilitacao-de-aprendizagem` e o guia `aula-e-workshop` | |
| Medir se o treinamento funcionou | `soap/avaliacao-de-treinamento` | `soap/matriz-kirkpatrick` |
| Pedir orçamento para o RH ou para a área | `soap/pedir-recursos` | `soap/roteiro-de-aprovacao-de-projeto` |

## O que vale para todas

1. **Informar não é comunicar** (`soap/comunicacao-interna`): a mensagem só chegou quando quem ouve, com outra posição e outros interesses, entendeu o sentido. Planeje do ponto A (onde a audiência está) ao ponto B (o que deve pensar, sentir e fazer).
2. **"E eu com isso?"**: diga o benefício ou o impacto para quem ouve antes do argumento da empresa.
3. **Três atos** (`soap/tres-atos`): comece pelo contexto da audiência (num anúncio que gera resistência, a abertura forte é uma dificuldade que ela vive), sustente com o porquê, termine com o que cada um faz agora.
4. **Uma voz só**: líderes alinhados antes de a equipe ouvir; a equipe sabe antes do mercado.
5. **Corpo, voz e fala na mesma direção** (`soap/credibilidade-do-lider`, `soap/credibilidade-e-autenticidade`): a equipe julga a credibilidade sem perceber.
6. **Escute**: a verdade só sobe quando o líder pergunta, ouve e mostra o próprio erro (`soap/seguranca-psicologica`).
7. **Fonte e ano** em todo número de pesquisa citado (GPTW, Michael Page e outros, como o material dá).

## Formato da entrega

```markdown
# <comunicação> para <audiência>
**Ponto A:** onde estão hoje   **Ponto B:** pensar, sentir, fazer
**E eu com isso?:** ...
## Três atos
Ato I (contexto) · Ato II (porquê e prova) · Ato III (o que cada um faz agora)
## Canais e momentos
| canal | quem fala | quando | o que vai |
## Perguntas que a equipe vai fazer
| pergunta | resposta |
```

Para feedback, onboarding e avaliação, a entrega é o modelo preenchido.

## Erros comuns

- Mandar o comunicado e chamar de comunicação: ninguém conferiu se o sentido chegou.
- Abrir pela estratégia da empresa e só no fim dizer o que muda para a pessoa.
- Em crise, silenciar até ter todas as respostas.
- Feedback de correção no corredor, sem fatos, ou em público.
- Treinamento sem diagnóstico antes e sem aplicação no trabalho depois.

## Prompt base

> Planeje <comunicação> para <audiência> sobre <assunto>, seguindo o guia `comunicacao-na-empresa` do Repertório. Abra a ficha da situação, escreva o ponto A, o ponto B e o "e eu com isso?", monte os três atos, os canais e quem fala, e liste as perguntas que a equipe vai fazer com a resposta. Se for apresentação, siga depois o fluxo do Repertório para os slides.

## Referências para abrir primeiro

- [Três atos com numeral em traço fino](http://127.0.0.1:8766/?workspace=7f53adaa-6bc5-496c-815e-f6159e2baec9&ref=soap-comunicacao-interna%2325): a comunicação interna em três atos.
- [Confiança que cresce com o cargo](http://127.0.0.1:8766/?workspace=7f53adaa-6bc5-496c-815e-f6159e2baec9&ref=soap-comunicacao-interna%2319): o dado que pede escuta.
- [Sete passos de preparação numerados](http://127.0.0.1:8766/?workspace=7f53adaa-6bc5-496c-815e-f6159e2baec9&ref=soap-feedback%2313): o feedback preparado.
- [Bocas abertas entre as letras de FALAR](http://127.0.0.1:8766/?workspace=7f53adaa-6bc5-496c-815e-f6159e2baec9&ref=soap-equipe-e-verdade%2311): a equipe que fala a verdade.
- [Pêndulo de Newton do relacionamento](http://127.0.0.1:8766/?workspace=7f53adaa-6bc5-496c-815e-f6159e2baec9&ref=soap-credibilidade-do-lider%2319): a credibilidade do líder.
