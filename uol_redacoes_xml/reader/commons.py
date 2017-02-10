# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 20:21:16 2016

@author: Guilherme Passero <guilherme.passero0@gmail.com>
"""

import nltk
from nltk.tokenize import word_tokenize
from sklearn import model_selection
from scipy.stats import pearsonr
from matplotlib import pyplot as plt
from math import sqrt
import re

def xstr(s):
    '''Treat None as empty string.'''
    if s is None:
        return ''
    return str(s)


def tokenize(text):
    return word_tokenize(text)


def get_paragraphs(text):
    return text.split('\n')


def find(pattern, text):
    return [(i.start(), i.end()) for i in re.finditer(pattern, text)]


sent_tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')
def get_sentences(text):
    return sent_tokenizer.tokenize(text)


def eval_regression(gold_values, sys_values, model_name='', plot=False):
    '''
    Evaluate the semantic similarity output of the system against a gold score.
    Results are printed to stdout.
    Adapted from PROPOR-ASSIN Workshop.
    '''

    pearson = pearsonr(gold_values, sys_values)[0]
    absolute_diff = gold_values - sys_values
    rmse = sqrt((absolute_diff ** 2).mean())

    print('{:25}\t{:7}\t{:18}'.format('Modelo', 'Pearson', 'RMSE'))
    print('{:25}\t{:7.2f}\t{:18.2f}'.format(model_name, pearson, rmse))

    if plot:
        fig, ax = plt.subplots()
        fig.canvas.set_window_title('Resultados')
        ax.scatter(gold_values, sys_values, alpha=.05, s=200)
        ax.plot([gold_values.min(), gold_values.max()], [gold_values.min(), gold_values.max()], 'k--', lw=4)
        ax.set_xlabel('Humano')
        ax.set_ylabel('Computador')
        plt.show()

    return pearson, rmse


def kfold_cross_validation(clf, X, y, n_sets=10, model_name='', plot=False):
    y_predicted = model_selection.cross_val_predict(clf, X, y, cv=n_sets)
    return eval_regression(y, y_predicted, model_name=model_name, plot=plot)