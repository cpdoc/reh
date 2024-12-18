import spacy

def identificar_nomes_pessoas(string):
    
    nlp = spacy.load("pt_core_news_sm")
    doc = nlp(string)
    nomes = [ent.text for ent in doc.ents if ent.label_ == "PER"]
    
    return nomes
