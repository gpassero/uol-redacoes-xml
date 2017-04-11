# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 10:34:00 2016

@author: Guilherme Passero <guilherme.passero0@gmail.com>
"""

import logging
from uol_redacoes_xml.reader.commons import get_paragraphs, get_sentences, tokenize, xstr

LOGGER = logging.getLogger(__name__)


class Prompt:

    def __init__(self, title, description, info, url, date):
        self.title = xstr(title)
        self.description = xstr(description)
        self.info = xstr(info)
        self.url = xstr(url)
        self.date = xstr(date)

    def __repr__(self):
        return self.title + '\n' + self.url


class Essay:

    def __init__(self, title, text, final_score, criteria_scores, prompt, url,
                 fixed_text, errors, comments):
        self.title = xstr(title)
        self.text = xstr(text)
        self.criteria_scores = criteria_scores
        self.final_score = final_score
        self.prompt = prompt
        self.url = xstr(url)
        self.fixed_text = xstr(fixed_text)
        self.errors = errors
        self.comments = xstr(comments)

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

        LOGGER.info('Extracted features from essay "' + self.title + '"\n')
        LOGGER.info('-' * 20)
        LOGGER.info(self.text)
        LOGGER.info('-' * 20)
        LOGGER.info('Score: {0}'.format(self.final_score))
        LOGGER.info('Features: ')
        for key in self.features:
            LOGGER.info(key + ': ' + str(self.features[key]))

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
