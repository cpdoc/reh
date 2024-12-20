from gensim.models.ldamodel import LdaModel
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis
from gensim.corpora import Dictionary
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import spacy

# Baixar dependências do NLTK

for rec in ['tokenizers/punkt','corpora/stopwords','stemmers/rslp']:
    try:
        nltk.data.find(rec)
    except LookupError:
        nltk.download(rec.split('/')[-1])
        
nlp = spacy.load("pt_core_news_sm")

def topic_modelling_artigos(json_data):
    
    print('Realizando Topic Modelling dos artigos...')
    # Pré-processamento dos textos

    def preprocess_text(text):
        stop_words = set(stopwords.words('portuguese'))
        palavras_ignoradas = {'artigo', 'pesquisa', 'estudo', 'sobre', 'analisar'}  # Palavras adicionais
        stop_words.update(palavras_ignoradas)
        text_lemma = " ".join([token.lemma_ for token in nlp(text)])
        tokens = word_tokenize(text_lemma.lower())
        tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
        return tokens

    # Coletar resumos e palavras-chave
    textos = []
    for edicao in json_data:
        for artigo in edicao['Artigos']:
            resumo = artigo['Resumo'] if isinstance(artigo['Resumo'], 
                                                    str) else ''
            palavras_chave = " ".join(artigo['Palavras chave']) if isinstance(artigo['Palavras chave'], 
                                                                              list) else ''
            textos.append(resumo + " " + palavras_chave)
    
    # Pré-processar os textos
    textos_tokenizados = [preprocess_text(texto) for texto in textos]

    # Criar o dicionário e a matriz de corpus para o LDA
    dictionary = Dictionary(textos_tokenizados)
    corpus = [dictionary.doc2bow(texto) for texto in textos_tokenizados]

    # Modelagem de tópicos com LDA
    num_topics = 10  # Definir número de tópicos desejados
    lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=20, random_state=99999)

    # Atribuir tema predominante a cada artigo
    temas_artigos = []
    for doc_bow in corpus:
        tema_dominante = max(lda_model[doc_bow], key=lambda x: x[1])[0]
        temas_artigos.append(tema_dominante)

    # Adicionar tema aos artigos no JSON
    for edicao in json_data:
        for i, artigo in enumerate(edicao['Artigos']):
            artigo['Tema'] = f"Tema {temas_artigos[i]}"
            
    vis_data = gensimvis.prepare(lda_model, corpus, dictionary)
    pyLDAvis.display(vis_data)
    pyLDAvis.save_html(vis_data, './outputs/lda_artigos_REH.html')