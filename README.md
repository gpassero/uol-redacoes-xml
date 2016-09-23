# UOL Redações em XML
O banco de redações da UOL (http://educacao.uol.com.br/bancoderedacoes/) é atualizado mensalmente com 20 redações. Estas redações são avaliadas por um especialista conforme os critérios do ENEM e visam auxiliar estudantes a melhorar sua escrita. 

Neste repositório todas as redações publicadas até então estão disponível em um arquivo XML, extraído a partir de um programa via requisições HTTP automáticas e interpretação das páginas HTML. Este corpus pode servir como modelo de testes e validação de técnicas de PLN (Processamento de Linguagem Natural) sobre redações.

No processo de extração foram obtidos o texto original, o texto corrigido, o tema, a nota geral, as notas por critério e os erros comentados (expressão errada e versão corrigida pelo avaliador).

# Critérios de avaliação
Os critérios de avaliação utilizados pela UOL no seu banco de redações são os mesmos do ENEM:

1. Demonstrar domínio da modalidade escrita formal da língua portuguesa (aspectos gramaticais e ortográficos);
2. Compreender a proposta de redação e aplicar conceitos das várias áreas de conhecimento para desenvolver o tema, dentro dos limites estruturais do texto dissertativo-argumentativo em prosa (adequação ao tema);
3. Selecionar, relacionar, organizar e interpretar informações, fatos, opiniões e argumentos em defesa de um ponto de vista (coerência);
4. Demonstrar conhecimento dos mecanismos linguísticos necessários para a argumentação (coesão);
5. Elaborar proposta de intervenção para o problema abordado, respeitando os direitos humanos (moral e ética).

Neste corpus a cada critério foi atribuída uma nota de 0 a 2 por um especialista da UOL. Somando-se a nota de cada critério obtém-se a nota final (entre 0 e 10).

# Tarefas
Algumas tarefas a serem trabalhadas no corpus:

1. Avaliação automática de redações conforme um dos critérios do ENEM (computar uma nota válida de 0 a 2 por critério);
2. Avaliação automática da qualidade geral de redações (computar uma nota válida de 0 a 10);
3. Detecção de erros ortográficos (comparação com erros detectados pelo avaliador);
4. Geração de feedback sobre a escrita (os comentários do avaliador podem auxiliar nessa tarefa).

# Métricas de validação
Como métricas de validação pretende-se usar Correlação de Pearson e RMSE (Root Mean Squared Error) para as tarefas 1) e 2) e F1 score e Acurácia para a tarefa 3). Avise-me se você souber de critérios melhores ou que podem suplementar os citados na validação dessas tarefas.

# Ranking
Caso você esteja desenvolvendo programas para avaliação automática de redações o convidamos a compartilhar seus resultados sobre este corpus.

# Versão
Versão de julho/2016 com + 2000 redações.

# Publicações
Não tenho conhecimento de alguma publicação científica utilizando esse corpus. Por favor, avise-me se souber de alguma.

# Código fonte do web crawler
Em breve será postado o programa em Python utilizado para extrair os dados. Este programa pode ser reutilizado para extrair dados das próximas redações. Neste programa também estarão disponíveis métodos para validar modelos criados para atender as tarefas acima.

Também será postado em breve uma baseline em Python para importar todos os dados e realizar algumas análises simples.

# Termos de uso
Copyright UOL. Todos os direitos reservados. É permitida a reprodução apenas em trabalhos escolares, sem fins comerciais e desde que com o devido crédito ao UOL e aos autores.
