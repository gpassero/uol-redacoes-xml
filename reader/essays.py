# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 10:34:00 2016

@author: Guilherme Passero <guilherme.passero0@gmail.com>
"""

from commons import xstr, tokenize, get_paragraphs, get_sentences
import numpy as np
from bs4 import BeautifulSoup
from collections import Counter
from os.path import isfile
import re
import bz2
import pickle


class EssayTheme:

    def __init__(self, title, description, url):
        self.title = xstr(title)
        self.description = xstr(description)
        self.url = xstr(url)

    def __repr__(self):
        return self.title + '\n' + self.url


class Essay:

    def __init__(self, title, text, final_score, criteria_scores, theme, url,
                 fixed_text, errors):
        self.title = xstr(title)
        self.text = xstr(text)
        self.criteria_scores = criteria_scores
        self.final_score = final_score
        self.theme = theme
        self.url = xstr(url)
        self.fixed_text = xstr(fixed_text)
        self.errors = errors

    def _extract_features(self):
        self.words = tokenize(self.text)
        self.paragraphs = get_paragraphs(self.text)
        self.sentences = get_sentences(self.text)
        self.paragraphs_size = [len(paragraph) for paragraph in self.paragraphs]
        unique_words_count = len(set(self.words))

        self.features = {
                    'chars_count': len(self.text),
                    'words_count': len(self.words),
                    'paragraphs_count': len(self.paragraphs),
                    'paragraphs_size_avg': len(self.text) / len(self.paragraphs),
                    'unique_words_count': unique_words_count,
                    'repetition_avg': (len(self.words) / unique_words_count) * 100,
                    'word_length_avg': len(self.text) / len(self.words)
                  }

        print('Extracted features from essay "' + self.title + '"\n')
        print('-'*20)
        print(self.text)
        print('-'*20)
        print('Score: {0}'.format(self.final_score))
        print('Features: ')
        for key in self.features:
            print(key + ': ' + str(self.features[key]))


    def get_features(self, features_name=None):
        if not hasattr(self, 'features'):
            self._extract_features()

        features = []
        if features_name is None:
            features = list(self.features.values())
        else:
            for feature_name in features_name:
                features.append(self.features[feature_name])

        return features


    def __repr__(self):
        return self.title + '\n' + self.text


NO_SCORE_WARNING = 'No score defined for essay {0}, ' + \
                   'using the sum of criteria ({1})'
BANK_XML_FILENAME = 'uol_essays_bank.xml.bz2'
BANK_DUMP_FILENAME = 'uol_essays_bank.pickle'

def load_uol_essays_bank(filter_theme=False, save_dump=True, load_dump=True, dump_filename=BANK_DUMP_FILENAME):

    if load_dump and (isfile(BANK_DUMP_FILENAME) or isfile(dump_filename)):
        print('Loading UOL essays bank from ' + dump_filename)
        essays = pickle.load(open(dump_filename, 'rb'))
        return essays

    with bz2.open(BANK_XML_FILENAME, 'rt', encoding='utf-8') as f:
        xml = f.read()

    xml = re.sub('>[\r\n ]*', '>', xml)
    xml = re.sub('[\r\n ]*<', '<', xml)
    xml = re.sub('[ ]*[\r\n]+[ ]*', '\n', xml)
    xml = re.sub('\n[\n ]+', '\n', xml)
    soup = BeautifulSoup(xml, 'xml')

    i = 0
    essays = []
    warnings = []

    for s_theme in soup.find_all('theme'):
        theme_title = s_theme.find('name').string
        theme_description = s_theme.description.string if s_theme.description is not None else ''
        if theme_description == '':
            warnings.append('Theme without description (but not skipped)')
#        theme_description = re.sub('[#]* Redações corrigidas.*', '', theme_description, flags=re.DOTALL)
#        theme_description = re.sub('[#]* Observações.*', '', theme_description, flags=re.DOTALL)
        theme_url = s_theme.url.string if s_theme.url is not None else ''
        theme = EssayTheme(theme_title, theme_description, theme_url)

        if filter_theme is not False:
            if filter_theme.lower() not in theme.title.lower():
                continue

        for essay in s_theme.find_all('essay'):
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
                print(NO_SCORE_WARNING.format(i, criteria_score_sum))
                print(essay.title.string)
                print(essay.url.string)
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
                                final_score, criteria_scores, theme,
                                essay.url.string, fixed,
                                errors))

            if i % 100 == 0:
                print(str(i) + ' essays read...')

    warnings = Counter(warnings)

    if len(warnings) > 0:
        warnings_count = 0
        print('Warnings: ')
        WARNING_TEMPLATE = '{0}  ->  {1}'
        for warning, count in warnings.items():
            print(WARNING_TEMPLATE.format(warning, count))
            warnings_count += count

        print('Total warnings: {0}'.format(warnings_count))

    print('Total essays loaded: {0}'.format(len(essays)))

    if save_dump:
        pickle.dump(essays, open(dump_filename, 'wb'))

    return essays
