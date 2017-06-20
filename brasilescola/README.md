# (em construção)

# Banco de Redações Brasil Escola
O banco de redações do portal Brasil Escola (http://vestibular.brasilescola.uol.com.br/banco-de-redacoes/),
de modo similar ao do portal UOL Educação, é atualizado mensalmente com um novo tema e diversas redações.
As redações também são avaliadas por um especialista conforme os critérios do ENEM e visam auxiliar estudantes a melhorar sua escrita.

Esta pasta contém um projeto baseado no framework *scrapy* criado com objetivo de extrair as redações do portal Brasil Escola para um formato estruturado.
O mecanismo de extração é bastante diferente do projeto inicial deste repositório, que utilizava os pacotes http, pyquery e html2text para extrair o banco de redações da UOL Educação.

[Scrapy](https://doc.scrapy.org/en/latest/intro/overview.html) é um framework de crawling que auxilia na extração de dados a partir de páginas da web.
Para utilizar o scrapy na extração de redações do portal Brasil Escola, um novo projeto python foi criado utilizando a estrutura de pastas padrão desse framework.

# Dependências
* scrapy
* pyquery
* html2text

# Execução
Para executar este crawler, faça uma cópia do projeto, posicione-se no diretório raiz e execute o seguinte comando:

```
    scrapy crawl -o "essays.json" --logfile "essays.json.log" brasilescolaspider
```

As redações extraídas serão armazenadas no formado JSON no arquivo *essays.json* e o log da execução do script será salvo no arquivo *essays.json.log*.
Para ver outros parâmetros de execução do scrapy, execute apenas o comando *scrapy* ou *scrapy crawl*.

Se preferir, você pode pular essa etapa e baixar o arquivo *essays.json.zip* a partir [deste repositório](essays.json.zip) (versão de junho/2017).

# Versão
Em junho de 2017 o portal Brasil Escola já continha mais de 4.500 redações.

# Publicações
Tomei conhecimento do banco de redações desse portal no VIII Computer on the Beach (2017), através do trabalho
intitulado [*Proposta de um Sistema de Avaliação Automática de Redações do ENEM Utilizando Técnicas de Aprendizagem de Máquina e Processamento de Linguagem Natural*](http://siaiap32.univali.br/seer/index.php/acotb/article/view/10592), desenvolvido na UFES.
Este trabalho avalia uma abordagem para correção automática de redações do ENEM, quanto à competência 1 (domínio da norma culta da língua),
utilizando um conjunto de redações do portal Brasil Escola para validação.

# Termos de uso
Copyright UOL. Todos os direitos reservados. É permitida a reprodução apenas em trabalhos escolares, sem fins comerciais e desde que com o devido crédito ao UOL e aos autores.
