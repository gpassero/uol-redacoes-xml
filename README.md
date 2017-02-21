# UOL Redações em XML
O banco de redações da UOL (http://educacao.uol.com.br/bancoderedacoes/) é atualizado mensalmente com 20 redações. Estas redações são avaliadas por um especialista conforme os critérios do ENEM e visam auxiliar estudantes a melhorar sua escrita. 

Neste repositório todas as redações publicadas até então estão disponível em um arquivo XML, extraído a partir de um programa via requisições HTTP automáticas e interpretação das páginas HTML. Este corpus pode servir como modelo de testes e validação de técnicas de PLN (Processamento de Linguagem Natural) sobre redações.

No processo de extração foram obtidos o texto original, o texto corrigido, o tema, a nota final, as notas por critério e, para redações mais recentes, erros gramaticais e ortográficos e a versão corrigida pelo avaliador.

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
4. Detecção de fuga ao tema;
5. Geração de feedback sobre a escrita (os comentários do avaliador podem auxiliar nessa tarefa).

# Métricas de validação
Como métricas de validação sugiro usar Correlação de Pearson e RMSE (Root Mean Squared Error) para as tarefas 1) e 2) e F1 score e Acurácia para a tarefa 3). Avise-me se você souber de critérios melhores ou que podem suplementar os citados na validação dessas tarefas.

# Instalação
Instale este pacote com o comando pip abaixo:

```
    pip install git+https://github.com/gpassero/uol-redacoes-xml.git
```

# Como carregar as redações
Em reader/essays.py você encontra um algoritmo para carregar todos os dados do XML em uma estrutura fácil de ser manipulada em Python.
O comando abaixo mostra como carregar as redações usando o método *load_uol_essays_bank*:

```python
from uol_redacoes_xml.reader.essays import load_uol_essays_bank
essays = load_uol_essays_bank(xml_filename='uol_essays_bank.xml.bz2')
print(len(essays))
# ~2000
print(essays[0].text)
# texto original da primeira redação
```

# Baseline
Dependências:
* sklearn
* matplotlib
* scipy

Em reader/baseline.py são carregadas *features* simples e é utilizada Regressão Linear para prever a nota final das redações. Você pode usar esse código para estudar o carregamento e aplicação de features e eventualmente estender essa baseline para atingir melhores resultados. Atualmente os resultados dessa baseline são:

    Modelo      Pearson	  RMSE              
    Baseline    0.42      2.04

Um algoritmo com performance similar à humana precisa atingir ao menos Pearson > 0.8 e RMSE < 0.5 (sugestão, pois não existe consenso sobre esses números).

Essa baseline utiliza as seguintes *features*:
* Número de caracteres
* Número de palavras
* Número de parágrafos
* Tamanho médio dos parágrafos
* Número de palavrás únicas (vocabulário)
* Repetição de palavras (total / vocabulário)
* Tamanho médio das palavras

# Validação cruzada k-fold
Dependências:
* sklearn
* matplotlib

Em reader/commons.py você encontra o método *kfold_cross_validation* para realizar uma validação cruzada estratificada 10-fold. Isto é, o banco de redações é dividido em 10 partes com cerca de 200 redações cada e são realizadas 10 iterações. Em cada iteração 9 partes são usadas para treino e 1 para teste. Ao final das 10 iterações, todo o banco de redações foi testado de modo que em nenhum momento uma redação apresentada no treino foi reconsiderada no teste.

```python
from uol_redacoes_xml.reader.commons import kfold_cross_validation
kfold_cross_validation(classifier, X, y, plot=True)
```

O comando acima aciona os métodos **fit** e **predict** de *classifier*. Estes métodos estão presentes na maioria dos algoritmos de aprendizado automático do pacote *sklearn*. O método acima retorna duas métricas de validação: Correlação de Pearson (r) e RMSE e também exibe esses valores na saída de texto padrão. 

Quando este método é chamado com o parâmetro *plot=True*, é apresentado um gráfico de dispersão das notas calculadas em comparação às notas humanas (*scatter plot*):

![Gráfico de dispersão da baseline](https://github.com/gpassero/uol-redacoes-xml/raw/master/image/baseline_scatter_plot.png)

# Ranking
Caso você esteja desenvolvendo programas para avaliação automática de redações o convidamos a compartilhar seus resultados sobre este corpus.

## Nota final

    Modelo      Pearson	  RMSE              
    Baseline    0.42      2.04

# Versão
Versão de janeiro/2017 com + 2000 redações e + 100 propostas temáticas.

# Publicações
As publicações científicas abaixo tratam sobre a avaliação automática de redações e fazem uso do banco de redações da UOL (não necessariamente usando este *web crawler*):

[[2013] Bruno S. Bazelato e Evelin C. F. Amorim. A Bayesian Classifier to Automatic Correction of Portuguese Essays.](http://www.tise.cl/volumen9/TISE2013/779-782.pdf)

[[2016] Jário José Santos, Ranilson Paiva, Ig Ibert Bittencourt. Lexical-Syntactic Evaluation of written activities based on Genetic Algorithm and Natural Language Processing: An experiment on ENEM.](http://www.br-ie.org/pub/index.php/rbie/article/view/6450)

Não encontrei mais publicações científicas utilizando esse corpus. Por favor, avise-me se souber de alguma.

# Web crawler
Na pasta **crawler** está disponível o código fonte do programa em Python usado para extrair os dados do site da UOL.

As dependências abaixo são necessárias para executá-lo e podem ser instaladas com o comando *pip*:
* pyquery
* html2text

Às vezes o servidor da UOL bloqueia ou demora a responder as requisições HTTP. Nesse caso, eu executei o programa duas ou três vezes, filtrando metade ou um terço das redações (salvando em um arquivo separado e ao final juntando as partes).

# Termos de uso
Copyright UOL. Todos os direitos reservados. É permitida a reprodução apenas em trabalhos escolares, sem fins comerciais e desde que com o devido crédito ao UOL e aos autores.
