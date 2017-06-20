"""This spider extracts essays from Brasil Escola (http://vestibular.brasilescola.uol.com.br/banco-de-redacoes/).
"""
import scrapy
import html2text
import re
from pyquery import PyQuery as pq

h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_images = True
h.ignore_emphasis = True
h.body_width = False

IGNORE_CHAR = re.compile(r'(^[\r\n\t\s]+|[\r\n\t\s]+$)')
EXTRACT_NUMBER = re.compile(r'[^\d](\d+([.,]\d+)?).*')
PROMPT_DESCRIPTION_SUB = re.compile(r'Saiba como fazer uma boa.+', re.DOTALL)
PROMPT_INFO_SUB = re.compile(r'.+Elabore sua redação[^\r\n]+[\r\n]*', re.DOTALL)
ESSAY_COMMENTS_SUB = re.compile(r'.+Comentários do corretor', re.DOTALL)
ESSAY_COMMENTS_SUB2 = re.compile(r'Competências avaliadas.+', re.DOTALL)


def strip(text):
    return IGNORE_CHAR.sub('', text)

def get_text(response, select):
    text = response.css(select+'::text').extract_first()
    if not text: return ''
    return strip(text)

def get_div_text(html):
    return strip(h.handle(html))

def extract_number(text):
    number = EXTRACT_NUMBER.findall(text)
    if len(number) == 0:
        return None
    return float(number[0][0])

def remove_double_breaks(text):
    text = re.sub(r'.\s+[\r\n]+', '.\n', text)
    text = re.sub(r'[\r\n]+', '\n', text)
    text = re.sub(r'(^\n+|\n+$)', '', text)
    return strip(text)

def handle_prompt_content(html):
    d = pq(html)
    if d.text() == '':
        return '', '', ''

    text = get_div_text(html)
    text = re.sub(r'^PUBLICIDADE\s*', '', text)

    description = PROMPT_DESCRIPTION_SUB.sub('', text)
    description = remove_double_breaks(strip(description))

    info = PROMPT_INFO_SUB.sub('', text)
    info = remove_double_breaks(strip(info))

    date = ''

    return description, info, date

def handle_essay_content(html):
    d = pq(html)
    if d.text() == '':
        return '', []
    errors = d.find('s').map(lambda i, e: (pq(e).text()))
    original = h.handle(d.remove('p > span').html())
    original = strip(original.replace('~~', ''))
    original = remove_double_breaks(original)
    return original, errors

def handle_essay_comments(html):
    d = pq(html)
    if d.text() == '':
        return '', []
    comments = h.handle(d.html())
    comments = ESSAY_COMMENTS_SUB.sub('', comments)
    comments = ESSAY_COMMENTS_SUB2.sub('', comments)
    comments = remove_double_breaks(strip(comments))
    return comments

class BrasilEscolaSpider(scrapy.Spider):
    name =  'brasilescolaspider'
    allowed_domains = ['vestibular.brasilescola.uol.com.br']
    start_urls = ['http://vestibular.brasilescola.uol.com.br/banco-de-redacoes/']

    def parse(self, response):
        prompt_url = response.url
        print('Reading prompt from URL {0}'.format(prompt_url))
        description, info, date = handle_prompt_content(response.css('#secao_texto').extract_first())
        yield {
            'type': 'prompt',
            'title': get_text(response, '.definicao').replace('Tema: ', ''),
            'description': description,
            'info': info,
            'url': prompt_url,
            'date': date
        }

        for essay_url in response.css('table#redacoes_corrigidas a::attr(href)').extract():
            print('Reading essay from URL {0}'.format(essay_url))
            if essay_url == '': continue
            yield response.follow(essay_url, self.parse_essay, meta={'prompt': prompt_url})
            # break

        next_page = response.css('div.paginador a::attr(href)').extract()[0]
        if next_page != '': # and 'caminhos' in next_page:
            yield response.follow(next_page, self.parse)

    def parse_essay(self, response):
        title = strip(get_text(response, '.conteudo-pagina h1').replace('Banco de Redações', ''))
        scores = {}
        i = 1
        for score_text in response.css('.conteudo-pagina table tr td:nth-child(2)::text').extract()[1:6]:
            scores['Competência {0}'.format(i)] = float(strip(score_text))
            i += 1

        score_text = response.css('.conteudo-pagina table tr td[colspan="2"] span::text').extract_first()
        total_score = extract_number(score_text)

        html_text = ''.join(response.css('.conteudo-pagina .conteudo-materia > p').extract())
        review = remove_double_breaks(get_div_text(html_text))
        original_text, errors = handle_essay_content(html_text)

        html_comments = ''.join(response.css('.conteudo-pagina .conteudo-materia > div').extract())
        comments = handle_essay_comments(html_comments)
        yield {
            'type': 'essay',
            'prompt': response.meta['prompt'],
            'date': get_text(response, '#redacao_dt_tema_left').replace('Redação enviada em ', ''),
            'title': title,
            'text': original_text,
            'final_score': total_score,
            'criteria_scores': scores,
            'url': response.url,
            'review': review,
            'errors': errors,
            'comments': comments
        }


