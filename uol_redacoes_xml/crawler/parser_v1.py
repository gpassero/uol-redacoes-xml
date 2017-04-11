# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 22:48:30 2016

@author: Guilherme Passero <guilherme.passero0@gmail.com>

This parser works with old UOL essays bank layout (http://educacao.uol.com.br/bancoderedacoes/temas.jhtm).

Essays since Nov. 2007 up to Jan. 2016.
"""

from commons import get_web_page_content, html2text
from pyquery import PyQuery as pq
import re

MONTHS = ['', 'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
          'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']

# Some essays may point to same URL (e.g. "Sem título 1"). In this case,
# only the latest version is available, so we ignore the older versions.
LOADED_URLS = []

# These essays have no content (e.g. http://educacao.uol.com.br/bancoderedacoes/redacoes/militarizacao-problema-ou-solucao.htm)
# no URL or no criteria score
BAD_TITLES = ['Militarização: Problema ou Solução?', 'Chegaremos à Rio + 100?',
              '(Sem título 018)', '[Sem titulo]']

def find_prompts(host = 'educacao.uol.com.br',
                page = '/bancoderedacoes/temas.jhtm'):
    html_content = get_web_page_content(host+page)
    d = pq(html_content)
    prompts = d('#bancoderedacoes ul li a').map(lambda i, e: (pq(e).text(), pq(e).attr('href')))

    global DATES_PER_URL
    DATES_PER_URL = {}
    for name, url in prompts:
        date = re.sub(':.*', '', name)
        if len(date.split(' ')) == 3:
            month, _, year = tuple(date.split(' '))
            date = '{0}-{1:02d}-01'.format(year, MONTHS.index(month.lower()))

        DATES_PER_URL[url] = date

    prompts = [(re.sub('^.*\d\d: ', '', name), url) for name, url in prompts]
    prompts = [(re.sub('^: ', '', name), url) for name, url in prompts]
    return prompts


def find_prompt_essays(url):
    global DATES_PER_URL, LOADED_URLS, BAD_TITLES

    html_content = get_web_page_content(url)
    if html_content is False:
        return False, False

    d = pq(html_content)

#    obs = d('#bancoderedacoes h3:contains("Observações")').html()
#    match = re.search('Confira as redações avaliadas a partir de ([\d]*) de ([^ ])* de ([\d])*', obs)
    date = DATES_PER_URL[url]
    # First essays had no date in title, so we search in content
    if date == '':
        date_content = d('#bancoderedacoes #listabox').text()
        # Some have the text "Confira as redações avaliadas a partir de ",
        # but some don't.
        match = re.search('Envie .* até o dia \d\d? de ([^ ]*) de (\d{4})', date_content)
        if match:
            month = match.group(1)
            year = match.group(2)
            if month in MONTHS:
                month = MONTHS.index(month.lower()) + 1
                if month > 12:
                    month = 1
                    year = int(year) + 1

                date = '{0}-{1:02d}-01'.format(year, month)

    description = d('#bancoderedacoes #conteudo, #texto').html()
    d2 = pq(description)
    d2.remove('.modfoto')
    description = '\n'.join(d2.children('p').map(lambda i, e: pq(e).text()))
    description = re.sub('Observações[\r\n ]Seu texto deve', '', description)

    info = pq(html_content).find('#listabox').html()
    info = html2text(info)
    info = re.sub('[# ]+Observações[\r\n]+.*', '', info, flags=re.DOTALL)

    essays_list_url = d('a:contains("Leia as redações avaliadas")').attr('href')
    html_content = get_web_page_content(essays_list_url)
    d = pq(html_content)
    d('#corrigidas a').filter(lambda i, e: pq(e).text() == '').remove()
    essays = d('#corrigidas a').map(lambda i, e: (pq(e).text(), pq(e).attr('href'), pq(e).next().text()))
    for i in range(len(essays)):
        title, url, score = essays[i]
        if score == '' or score == '0':
            score = re.sub('.* ([\d]{1,2},?\d?)$', '\\1', title)
            title = re.sub(' [\d,]*$', '', title)
            essays[i] = (title, url, score)

    essays = [(title, url, score) for title, url, score in essays
                                  if url not in LOADED_URLS
                                  and title not in BAD_TITLES]

    return date, description, info, essays


def get_essay_info(url):
    global LOADED_URLS
    LOADED_URLS.append(url)

    html_content = get_web_page_content(url)
    d = pq(html_content)

    paragraphs = []
    if len(d('#texto').find('p')) > 0:
        for child in d('#texto').children():
            if pq(child).is_('h1'):
                continue

            if not pq(child).is_('p'):
                break

            paragraphs.append(pq(child).html())

    else: # page layout until 2010 didn't had a 'p'
        if d('#texto').html() != None:
            text = re.sub('<h3.*', '', d('#texto').html())
            text = re.sub('<h1[^<]*h1>[\r\n\t ]*', '', text)
            paragraphs.append(text)

    if len(paragraphs) == 0:
        print('Couldn\'t read {0} content.'.format(url))

    content = '<p>' + '</p><p>'.join(paragraphs) + '</p>'

    comments = d('#texto').html()
    if comments:
        # Sometimes "Comentário geral", else " Comentários gerais"
        comments = re.sub('.*<h3>.?Comentário.? gera..?</h3>', '<h3>Comentário geral</h3>', comments)
    if comments != None and len(comments) > 10:
        comments = html2text(comments)

    criteria = d('#redacao h3:contains("Competências avaliadas")').next().find('tr').map(lambda i, e: (pq(e).find('td').eq(1).text(), pq(e).find('td').eq(2).text()))
    criteria = [(name, score) for name, score in criteria if name != 'Competência' and name  != '' and score != '']

    return content, comments, criteria
