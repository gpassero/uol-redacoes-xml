# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 22:54:52 2016

@author: Guilherme Passero <guilherme.passero0@gmail.com>
"""
from commons import handle_essay_content, write_to_file, close_conns
import parser_v1 as p1
import parser_v2 as p2
from xml.etree.ElementTree import Element, SubElement

CRITERIA_SHORTS = [('domínio da norma culta', 'Ortografia'),
                   ('compreender a proposta da redação', 'Adequação ao tema'),
                   ('organizar e interpretar informações', 'Coerência'),
                   ('conhecimento dos mecanismos ling', 'Coesão'),
                   ('respeito aos valores humanos', 'Ética')]

i = 0
ie = 0
def crawl(root, p):
    global i, ie

    themes = p.find_themes()

    for name, url in themes:

        i = i + 1
        print(i, name)
#        if i < 95:
#            continue

        date, description, essays = p.find_theme_essays(url)

        # Parsers v1 must not repeat what parser v2 is able to get
        if p == p1 and date > '2015-07-31':
            continue

        el_theme = SubElement(root, "theme")
        SubElement(el_theme, "name").text = name
        SubElement(el_theme, "url").text = url
        SubElement(el_theme, "date").text = date
        SubElement(el_theme, "description").text = description
        el_essays = SubElement(el_theme, "essays")

        if description is False:
            continue

        for title, url, score in essays:
            ie = ie + 1
            el_essay = SubElement(el_essays, "essay")
            SubElement(el_essay, "title").text = title
            SubElement(el_essay, "url").text = url
            SubElement(el_essay, "score").text = score

            content, comments, criteria = p.get_essay_info(url)
    #        SubElement(el_essay, "content").text = content
            original, fixed, errors, review = handle_essay_content(content)
            SubElement(el_essay, 'original').text = original
            SubElement(el_essay, 'fixed').text = fixed
            SubElement(el_essay, 'review').text = review

            SubElement(el_essay, "comments").text = comments
            el_criteria = SubElement(el_essay, "criteria")
            for description, score in criteria:
                el_criterion = SubElement(el_criteria, 'criterion')
                criterion_short_name = description + ' (?)'
                for pattern, short_name in CRITERIA_SHORTS:
                    if pattern.lower() in description.lower():
                        criterion_short_name = short_name
                        break

                SubElement(el_criterion, 'name').text = criterion_short_name
    #            SubElement(el_criterion, 'description').text = description
                SubElement(el_criterion, 'score').text = score

        if i % 1 == 0:
            write_to_file(root, 'essays.xml')
            print(i, ' essays theme and ', ie,' essays written to file.')

        close_conns()


root = Element('themes')

crawl(root, p2)
crawl(root, p1)

close_conns()