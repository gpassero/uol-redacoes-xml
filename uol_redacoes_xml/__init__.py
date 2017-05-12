"""This package provides a crawler to extract essays from UOL essays bank and a read for the generated XML file.

Repo: https://github.com/gpassero/uol-redacoes-xml
UOL Essays Bank: https://educacao.uol.com.br/bancoderedacoes/redacoes/
"""

import bz2
import logging
import os
import pickle
import re
from collections import Counter

from bs4 import BeautifulSoup

from uol_redacoes_xml.reader.commons import get_paragraphs, get_sentences, tokenize, xstr
from uol_redacoes_xml.reader.essays import Essay, Prompt

LOGGER = logging.getLogger(__name__)

XML_FILENAME = os.path.join(os.path.dirname(__file__), 'essays.xml.bz2')
DUMP_FILENAME = os.path.join(os.path.dirname(__file__), 'essays.pickle')
NO_SCORE_WARNING = 'No final score defined for essay {0}, using the sum of criteria ({1})'
WARNING_TEMPLATE = '{0}  ->  {1}'


def load(filter_prompt=None, save_dump=True, load_dump=True, xml_filename=XML_FILENAME, dump_filename=DUMP_FILENAME):
    """Return essays from crawled data (XML file)."""
    if load_dump and (os.path.isfile(DUMP_FILENAME) or os.path.isfile(dump_filename)):
        LOGGER.debug('Loading UOL essays bank from ' + dump_filename)
        essays = pickle.load(open(dump_filename, 'rb'))
        return essays

    with bz2.open(xml_filename, 'rt', encoding='utf-8') as f:
        xml = f.read()
    xml = re.sub('>[\r\n ]*', '>', xml)
    xml = re.sub('[\r\n ]*<', '<', xml)
    xml = re.sub('[ ]*[\r\n]+[ ]*', '\n', xml)
    xml = re.sub('\n[\n ]+', '\n', xml)
    soup = BeautifulSoup(xml, 'xml')

    i = 0
    essays = []
    warnings = []

    for s_prompt in soup.find_all('prompt'):
        prompt_title = s_prompt.find('name').string
        prompt_description = s_prompt.description.string if s_prompt.description is not None else ''
        if prompt_description == '':
            warnings.append('Prompt without description (but not skipped)')
        prompt_info = s_prompt.info.string if s_prompt.info is not None else ''
        if prompt_info == '':
            warnings.append('Prompt without description (but not skipped)')
        prompt_url = s_prompt.url.string if s_prompt.url is not None else ''
        prompt_date = s_prompt.date.string if s_prompt.date is not None else ''
        prompt = Prompt(prompt_title, prompt_description, prompt_info, prompt_url, prompt_date)

        if filter_prompt is not None:
            if filter_prompt.lower() not in prompt.title.lower():
                continue

        for essay in s_prompt.find_all('essay'):
            i = i + 1

            if essay.original is None or essay.original.string is None:
                warnings.append('No text')
                continue

            if essay.fixed is None or essay.fixed.string is None:
                warnings.append('No fixed text')
                continue

            if essay.score.string is not None:
                final_score = float(essay.score.string.replace(',', '.'))
            else:
                final_score = -1

            criteria_scores = {}
            criteria_score_sum = 0

            for criterion in essay.find_all('criterion'):

                if criterion.score.string is None:
                    continue

                criterion_name = xstr(criterion.find('name').string)
                criterion_score = criterion.score.string.replace(',', '.')
                criterion_score = re.sub('[^0-9,.]', '', criterion_score)
                criterion_score = float(criterion_score)
                criteria_scores[criterion_name] = criterion_score
                criteria_score_sum += criterion_score

            if len(criteria_scores) != 5:
                warnings.append('Not 5 criteria')
                continue

            if final_score == -1:
                LOGGER.warning(NO_SCORE_WARNING.format(i, criteria_score_sum))
                LOGGER.warning(essay.title.string)
                LOGGER.warning(essay.url.string)
                final_score = criteria_score_sum

            if criteria_score_sum != final_score:
                warnings.append('Final score != from sum of criteria score')
                continue

            errors = []
            for error in essay.find_all('error'):
                wrong = error.wrong.string if error.wrong.string is not None else ''
                right = error.right.string if error.right.string is not None else ''
                wrong, right = xstr(wrong), xstr(right)
                errors.append((wrong, right))

            original = essay.original.string
            fixed = essay.fixed.string
            essays.append(Essay(essay.title.string, original,
                                final_score, criteria_scores, prompt,
                                essay.url.string, fixed,
                                errors, essay.comments))

            if i % 100 == 0:
                LOGGER.info(str(i) + ' essays read...')

    warnings = Counter(warnings)

    if len(warnings) > 0:
        warnings_count = 0
        LOGGER.warning('UOL essays load warnings: ')
        for warning, count in warnings.items():
            LOGGER.warning(WARNING_TEMPLATE.format(warning, count))
            warnings_count += count

        LOGGER.warning('Total warnings: {0}'.format(warnings_count))

    LOGGER.info('Total essays loaded: {0}'.format(len(essays)))

    if save_dump:
        pickle.dump(essays, open(dump_filename, 'wb'))

    return essays
