# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 20:53:56 2016

@author: Guilherme Passero <guilherme.passero0@gmail.com>
"""

from .essays import load_uol_essays_bank
from .commons import kfold_cross_validation
import numpy as np
from sklearn import model_selection
from sklearn.linear_model import LinearRegression

def extract_features(essays):

    print('Extracting features from essays...')

    first_essay = essays[0]
    first_essay.get_features()
    features_names = first_essay.features.keys()
    features_names = np.array(list(features_names))
    features_names.sort()

    i = 0
    total = len(essays)
    last_percent_complete = 0
    features = []
    for essay in essays:
        i += 1
        features.append(essay.get_features(features_names))

        percent_complete = round(i / total, 2) * 100
        if percent_complete - last_percent_complete >= 1:
          print(str(percent_complete) + '% of essays have been processed..')
          last_percent_complete = percent_complete

    features = np.array(features)
    return features, features_names


def extract_targets(essays):
    targets = {}
    targets['Nota final'] = np.array([essay.final_score for essay in essays])

    for criterion in essays[0].criteria_scores:
        targets[criterion] = np.array([essay.criteria_scores[criterion]
                                      if criterion in essay.criteria_scores else 0
                                      for essay in essays])

    return targets


if __name__ == '__main__':
    essays = load_uol_essays_bank()
    X, X_legend = extract_features(essays)
    y = extract_targets(essays)['Nota final']

    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.1, random_state=0)

    regressor = LinearRegression(n_jobs=-1)
    regressor.fit(X_train, y_train)

    kfold_cross_validation(regressor, X, y, model_name='Baseline', plot=True)
