# UOL Redações em XML
O banco de redações da UOL (http://educacao.uol.com.br/bancoderedacoes/) é atualizado mensalmente com 20 redações. Estas redações são avaliadas por um especialista conforme os critérios do ENEM e visam auxiliar estudantes a melhorar sua escrita. 

Neste repositório todas as redações publicadas até então estão disponível em um arquivo XML, extraído a partir de um programa via requisições HTTP automáticas e interpretação das páginas HTML. Este corpus pode servir como modelo de testes e validação de técnicas de PLN (Processamento de Linguagem Natural) sobre redações.

No processo de extração foram obtidos o texto original, o texto corrigido, o tema, a nota geral, as notas por critério e os erros comentados (expressão errada e versão corrigida pelo avaliador).

Versão de julho/2016 com + 2000 redações.

Em breve será postado o programa em Python utilizado para extrair os dados. Este programa pode ser reutilizado para extrair dados das próximas redações. 

Também será postado em breve uma baseline em Python para importar todos os dados e realizar algumas análises simples.
