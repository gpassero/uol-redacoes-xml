# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 22:54:52 2016

@author: Guilherme Passero <guilherme.passero0@gmail.com>
"""
from uol_redacoes_xml.crawler.commons import handle_essay_content, write_to_file, close_conns
import uol_redacoes_xml.crawler.parser_v1 as p1
import uol_redacoes_xml.crawler.parser_v2 as p2
from xml.etree.ElementTree import Element, SubElement

CRITERIA_SHORTS = [('domínio da norma culta', 'Competência 1'),
                   ('domínio norma culta', 'Competência 1'),
                   ('compreender a proposta da redação', 'Competência 2'),
                   ('organizar e interpretar informações', 'Competência 3'),
                   ('conhecimento dos mecanismos ling', 'Competência 4'),
                   ('respeito aos valores humanos', 'Competência 5')]

# For essays that are present in both new and old versions, only from the new version the extraction will occur
# This is a fix for the prompt dates, since the published date are all the same for prompts in both new and old site
PROMPT_FIXED_DATES = {}
PROMPT_BASE_URL = 'https://educacao.uol.com.br/bancoderedacoes/propostas/'
PROMPT_FIXED_DATES['bandido-bom-e-bandido-morto.htm'] = '2015-11-01'
PROMPT_FIXED_DATES['o-sucesso-vem-da-escola-ou-do-esforco-individual.htm'] = '2015-10-01'
PROMPT_FIXED_DATES['disciplina-ordem-e-autoridade-favorecem-a-educacao.htm'] = '2015-09-01'
PROMPT_FIXED_DATES['forma-fisica-corpo-perfeito-e-consumismo.htm'] = '2015-08-01'
PROMPT_FIXED_DATES['intolerancia-religiosa-regra-ou-excecao-no-brasil.jhtm'] = '2015-07-01'

i = 0
ie = 0


def crawl(root, p):
    global i, ie

    prompts = p.find_prompts()

    for name, url in prompts:

        i = i + 1
        print(i, name)

        date, description, info, essays = p.find_prompt_essays(url)

        # Parsers v1 must not repeat what parser v2 is able to get
        if p == p1 and date > '2015-07-31':
            continue

        el_prompt = SubElement(root, "prompt")
        SubElement(el_prompt, "name").text = name
        SubElement(el_prompt, "url").text = url
        page = url.replace(PROMPT_BASE_URL, '')
        if page in PROMPT_FIXED_DATES:
            date = PROMPT_FIXED_DATES[page]
        SubElement(el_prompt, "date").text = date
        SubElement(el_prompt, "description").text = description
        SubElement(el_prompt, "info").text = info
        el_essays = SubElement(el_prompt, "essays")

        if description is False:
            continue

        for title, url, score in essays:
            ie = ie + 1
            el_essay = SubElement(el_essays, "essay")
            SubElement(el_essay, "title").text = title
            SubElement(el_essay, "url").text = url
            SubElement(el_essay, "score").text = score
            content, comments, criteria = p.get_essay_info(url)
            original, fixed, errors, review = handle_essay_content(content)
            SubElement(el_essay, 'original').text = original
            SubElement(el_essay, 'fixed').text = fixed
            SubElement(el_essay, 'review').text = review
            SubElement(el_essay, "comments").text = comments
            el_errors = SubElement(el_essay, 'errors')
            for wrong, right in errors:
                el_error = SubElement(el_errors, 'error')
                SubElement(el_error, 'wrong').text = wrong
                SubElement(el_error, 'right').text = right
            el_criteria = SubElement(el_essay, "criteria")
            for description, score in criteria:
                el_criterion = SubElement(el_criteria, 'criterion')
                criterion_short_name = description + ' (?)'
                for pattern, short_name in CRITERIA_SHORTS:
                    if pattern.lower() in description.lower():
                        criterion_short_name = short_name
                        break

                SubElement(el_criterion, 'name').text = criterion_short_name
                SubElement(el_criterion, 'score').text = score

        if i % 1 == 0:
            write_to_file(root, 'essays.xml')
            print(i, ' essays prompt and ', ie, ' essays written to file.')

        close_conns()


root = Element('prompts')

crawl(root, p2)
crawl(root, p1)

close_conns()
