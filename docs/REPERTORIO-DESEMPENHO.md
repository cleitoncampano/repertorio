# Revisão de desempenho do Repertório

Revisão de 18/10/2026, restrita a reduzir trabalho repetido. O visual e o comportamento aprovados pelo usuário continuam iguais. Não foram adicionadas dependências nem alterados o esquema do banco ou os arquivos do acervo.

## Mudanças

- Grafo e busca agora carregam em uma consulta os vínculos das referências e de seus pais. A resolução conserva estado, revisão, ordem, escopo e disponibilidade dos pais. Consultas individuais continuam disponíveis para fichas isoladas. Não há cache de curadoria que possa ficar desatualizado.
- O mapa agrupa a atualização do viewport por quadro e reutiliza as coleções de nós de referência e técnica. A câmera é gravada após 160 ms sem movimento, em vez de escrever em armazenamento síncrono a cada evento. Troca de visualização, saída da página e desmontagem gravam a posição final imediatamente.

## Medição do servidor

Comparação com o commit `62a7dbb`, na mesma cópia SQLite do acervo real. Cinco amostras por caso, alternando código anterior e atual no mesmo processo e com o mesmo banco, após aquecimento. Tempos são medianas da construção da resposta no servidor; não incluem rede, imagens ou desenho do mapa.

| Espaço e operação | Antes | Depois | Consultas antes | Consultas depois |
|---|---:|---:|---:|---:|
| PP Treta, grafo com 1.021 referências | 227,37 ms | 111,67 ms | 1.024 | 4 |
| PP Treta, página de busca com 48 referências | 302,05 ms | 291,85 ms | 179 | 5 |
| Growmate, grafo com 33 referências | 54,49 ms | 46,81 ms | 36 | 4 |
| Growmate, busca com 33 referências | 227,59 ms | 226,98 ms | 69 | 5 |

O maior ganho medido está no grafo maior, cerca de 51% no tempo de construção. A busca Growmate ficou praticamente estável. As quatro respostas completas são idênticas antes e depois, conferidas por igualdade e SHA-256. As medições são deste computador e não representam uma garantia para outros acervos ou máquinas.

## Medição da interface

Chrome, 1440 × 900, escala de pixels 2, PP Treta com 1.021 referências e 4.182 conexões. Três amostras de 480 eventos de deslocamento ao longo de 120 quadros, com 300 ms para concluir a gravação.

- Antes: 480 gravações de câmera por amostra durante o movimento.
- Depois: nenhuma gravação durante o movimento e uma gravação final por amostra.
- As capturas do mapa antes e depois têm pixels idênticos. As nove organizações, paletas, seleção, busca, filtros, arraste dos templates e câmeras independentes continuam funcionando.

## Validação e continuidade

- Build de produção, 34 testes Python, 34 testes unitários da interface e 25 testes de navegador aprovados.
- Testes novos verificam que a quantidade de SQL não cresce com o número de referências, comparam os resumos individuais e em lote em vários espaços e estados dos pais e conferem a câmera após muitos eventos e recarga imediata.
- Testes com escrita usam biblioteca temporária. Medições do servidor usam uma cópia consistente via backup SQLite; a medição do navegador apenas lê o serviço real. Evidências e scripts em `_saida/repertorio-qa/performance/`, fora do Git.
- Para código da interface, compilar e atualizar o app com ⌘R. Para código do servidor, seguir o reinício documentado em `biblioteca/manual-agentes.md`. Não é necessário recompilar o app nativo.
- Servidor atualizado ativado pelo reinício automático do app, com saúde e esquema `0004` confirmados. Os grafos reais Growmate e PP Treta continuam com 33 e 1.021 referências e respostas idênticas às verificadas na cópia, após normalizar apenas a porta dos links.
- Futuras revisões devem medir primeiro e preservar esses contratos. A busca ainda concentra tempo na seleção e ordenação SQL; o ganho medido nela foi pequeno, e uma nova revisão deve partir de planos de consulta antes de mudar índices ou semântica.
