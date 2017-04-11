# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 23:35:21 2016

@author: Guilherme Passero <guilherme.passero0@gmail.com>
"""

from http.client import HTTPSConnection as httpc
from xml.etree.ElementTree import tostring
from xml.dom import minidom
from pyquery import PyQuery as pq
import html2text
import re
import bz2
import time

conn = {}

h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_images = True
h.ignore_emphasis = True
h.body_width = False


def get_conn(host):
    global conn
    if not host in conn or conn[host].sock is None:
        conn[host] = httpc(host, timeout=999999)

    return conn[host]


def close_conns():
    global conn
    for key, conn_ in conn.items():
        conn_.close()


def get_web_page_content(url):
    time.sleep(0.1)

    if not url or url == '' or url == '?': return False
    host, page = re.sub('.*http.?://', '', url).split('/', 1)

    if not host: host = 'educacao.uol.com.br'
    conn = get_conn(host)
    print('Requesting ' + page, end='')
    try:
        conn.request('GET', '/'+page)
        print(' OK', end='')
        response = conn.getresponse()
        print(' OK', end='')
        if response.status == 200:
            content = response.read()
            print(' OK')
        else:
            content = False
            print(' ERROR')
            print(response.status, response.reason)
    except:
        print('Error connecting to ' + page)
        return ''

#    conn.close()
    return content


def html2text(html):
    return h.handle(html)


def handle_essay_content(html):
    d = pq(html)

    if d.text() == '':
        return '', '', [], ''

    errors = d.find('u').map(lambda i, e: (pq(e).text(), pq(e).next().text()))

    d.remove('h1, h2, h3, h4')
    original = h.handle(d.remove('.certo, .texto-corrigido').html())
    # Remove suggestions that were not put inside "span.text-corrigido"
    original = re.sub(r' \[(.*?)\]([.?!,])', r'\2', original)
    original = re.sub(r'\[(.*?)\][ ]?', '', original)

    d = pq(html)
    d.remove('h1, h2, h3, h4')
    d.find('u').map(lambda i, e: pq(e).text(pq(e).next().text().replace('[', '').replace(']', '')))
    d.remove('.certo, .texto-corrigido')
    fixed = h.handle(d.html())

    d = pq(html)
    d.remove('h1, h2, h3, h4')
    d.find('.certo, .texto-corrigido').map(lambda i, e: pq(e).text('['+pq(e).text()+']'))
    d.find('u').map(lambda i, e: pq(e).text('#-'+pq(e).text()+'-#'))
    d.find('.erro, .texto-errado, u').map(lambda i, e: pq(e).text('*-'+pq(e).text()+'-*'))
    review = h.handle(d.html())
    return original, fixed, errors, review


def write_to_file(root, filename='essays.xml'):
    xml = minidom.parseString(tostring(root)).toprettyxml(indent="\t")
#    xml = re.sub('>[\r\n ]*', '>', xml)
#    xml = re.sub('[\r\n ]*<', '<', xml)
    xml = re.sub('[ ]*[\r\n]+[ ]*', '\n', xml)
    xml = re.sub('\n[\n ]+', '\n', xml)
    with open(filename, 'wt', encoding = 'utf-8') as f:
        f.write(xml)
    with bz2.open(filename+'.bz2', 'wt', encoding='utf-8') as f:
        f.write(xml)
