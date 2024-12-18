# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 00:15:08 2024

@author: danie
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')

data = pd.DataFrame({'title': lista_de_titulos, 'abstract': lista_de_resumos})

stop_words = set(stopwords.words('portuguese'))

def preprocess_text(text):
    tokens = word_tokenize(text.lower())  # Tokenização e conversão para minúsculas
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    return " ".join(filtered_tokens)

data['processed_abstract'] = data['abstract'].apply(preprocess_text)

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(data['processed_abstract'])
# Aplicação do linkage
linkage_matrix = linkage(tfidf_matrix.toarray(), method='ward')

plt.figure(figsize=(10, 7))
dendrogram(linkage_matrix, labels=data['title'].values, leaf_rotation=90)
plt.title('Dendrograma de Clusterização Hierárquica')
plt.xlabel('Artigos')
plt.ylabel('Distância')
plt.show()
