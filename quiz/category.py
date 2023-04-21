import pandas as pd
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from nltk import pos_tag
# from nltk.tokenize import word_tokenize
import pymorphy2
import numpy as np
from spellchecker import SpellChecker
# import time


morph = pymorphy2.MorphAnalyzer()
spell_checker = SpellChecker(language='ru')


def nouns_only(text):
    text = text.replace(',', ' ')
    text = text.replace('(', ' ')
    text = text.replace(')', ' ')
    words = text.split()
    nouns = []
    for word in words:
        parsed = morph.parse(word)[0]

        nouns.append(parsed.normal_form)
    return nouns


def categorize(right_anwser, user_anwser):
    nouns_user = nouns_only(user_anwser)
    nouns_right = nouns_only(right_anwser)
    print(nouns_user)
    print(nouns_right)
    set_user = set(nouns_user)
    set_right = set(nouns_right)
    total_set = set_user | set_right
    vector1 = np.array([nouns_user.count(word) for word in total_set])
    vector2 = np.array([nouns_right.count(word) for word in total_set])

    cos = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))

    return cos

