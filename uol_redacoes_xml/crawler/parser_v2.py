# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 22:49:21 2016

@author: Guilherme Passero <guilherme.passero0@gmail.com>

This parser works with new UOL essays bank layout (http://educacao.uol.com.br/bancoderedacoes/).

Essays since Aug. 2015 up to now.
"""

from commons import get_web_page_content, html2text
from pyquery import PyQuery as pq
import re


def find_prompts(host = 'educacao.uol.com.br', page = '/bancoderedacoes/'):
    html_content = get_web_page_content(host+page)
    d = pq(html_content)
    prompts = d('#conteudo-principal h1 a').map(lambda i, e: (pq(e).text(), pq(e).attr('href')))
    prompts = [(re.sub(' REDAÇÕES CORRIGIDAS', '', name), url)
              for name, url in prompts]
    return prompts


def find_prompt_essays(url):
    html_content = get_web_page_content(url)
    d = pq(html_content)
    date = d('#conteudo-principal .info-header time').attr('datetime')
    description = d('#bancoderedacoes, #texto').html()
    d2 = pq(description)
    d2.remove('.imagem-representativa')
    description = '\n'.join(d2.children('p').map(lambda i, e: pq(e).text()))
    essays = d('.redacoes-corrigidas a').map(lambda i, e: (pq(e).text(), pq(e).attr('href'), pq(e).closest('tr').find('td').eq(1).text()))

    html_content = get_web_page_content(url+'?full')
    if html_content is False:
        info = 'XXX'
    else:
        d = pq(html_content)
#        articles = d('#bancoderedacoes, #texto').find('.list-items').eq(0).find('article')
#        info = []
#        for article in articles:
#            d2 = pq(article)
#            title = d2.find('.titles').eq(0).text()
#            if title == 'Observações':
#                continue
#            info.append(title + '\n'
#                        + '\n'.join(d2.children('.description p, p')
#                                      .map(lambda i, e: pq(e).text())))
#        info = '\n\n'.join(info)
        articles = d('#bancoderedacoes, #texto').find('.list-items').eq(0).html()
        info = html2text(articles)
        info = re.sub('[# ]+Observações[\r\n]+.*', '', info, flags=re.DOTALL)

    return date, description, info, essays


def get_essay_info(url):
    html_content = get_web_page_content(url)
    d = pq(html_content)
    paragraphs = []
    for child in d('#texto').children():
        if not pq(child).is_('p'):
            break
        paragraphs.append(pq(child).html())
    content = '<p>' + '</p><p>'.join(paragraphs) + '</p>'
    comments = d('#texto section.list-items').html();
    if comments != None and len(comments) > 10:
        comments = html2text(comments)
        comments = re.sub('#[^#]+', '', comments, 1)
    criteria = d('h2:contains("Competências avaliadas")').parent().find('table.table-redacoes tbody').eq(0).find('tr').map(lambda i, e: (pq(e).find('td').eq(0).text(), pq(e).find('td').eq(1).text()))
    return content, comments, criteria
