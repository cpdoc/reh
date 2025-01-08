import os
import json
import pandas as pd
from tqdm import tqdm
from utils.get_dados_edicoes import get_edicoes_reh
from utils.get_artigos_edicao import get_artigos_edicao
from utils.get_autores_referencias import get_autores_referencias
from utils.geracao_linksets import geracao_linkset_referencias, geracao_linkset_autores
from utils.identificar_nomes_pessoas import identificar_nomes_pessoas
from utils.gender_guesser import gender_guesser
from utils.plots import plot_generos_por_ano_artigos, plot_generos_por_ano_edicoes
from utils.topic_modelling import topic_modelling_artigos

if not os.path.exists('./outputs'):
    os.makedirs('./outputs')
        
print("Lendo base de dados atual...")

try:
    with open("./outputs/edicoes_reh.json", "r", encoding="utf-8") as arquivo:
        edicoes_reh = json.load(arquivo)
except FileNotFoundError:
    if input('Arquivo "edicoes_reh.json" não encontrado na pasta "outputs".\nDeseja realizar toda a coleta novamente? (s/n)\n') == 'n':
        exit()
    else:
        edicoes_reh = []
    
print("Coletando conjunto de edições publicadas...")
edicoes_reh_site = get_edicoes_reh()
print(f"{len(edicoes_reh_site)} edições identificadas no site da REH.")

# VERIFICAR NOVAS EDIÇÕES 

i = 0
for edicao in edicoes_reh_site:
    # Verificar se já existe um dicionário em edicoes_reh com a mesma URL
    if not any(d['URL'] == edicao['URL'] for d in edicoes_reh):
        edicoes_reh.append(edicao)
        i += 1
        
print(f"{i} edições novas encontradas para processamento.")

if i > 0:      
    
    #%%
    for edicao in tqdm(edicoes_reh, desc="Coletando artigos das edições..."):
        if 'Artigos' not in edicao.keys():
            edicao['Artigos'] = get_artigos_edicao(edicao)
    
    #%%
    for edicao in tqdm(edicoes_reh, desc="Coletando autores das bibliografias...", position=0):
        # for artigo in tqdm(edicao['Artigos'], desc=f"{edicao['Titulo']}", position=1, leave=False):
        for artigo in tqdm(edicao['Artigos'], desc=f"{edicao['Titulo']}", position=1):
            if 'Autores(as) Referencias' not in artigo.keys():
                artigo['Autores(as) Referencias'] = get_autores_referencias(artigo)
    
    #%%
    for edicao in tqdm(edicoes_reh, desc="Identificando nomes/gêneros dos metadados..."):
        for categoria in ['Conselho Consultivo', 'Editores(as)', 
                          'Editores(as) Convidados(as)', 'Pareceristas ad hoc',
                          'Pareceristas', 'Secretários(as)', 
                          'Digitadores(as)', 'Estagiários/as'
                          ]:
            if categoria in edicao.keys():
                if isinstance(edicao[categoria], str):
                    edicao[categoria] = identificar_nomes_pessoas(edicao[categoria])
                    if len(edicao[categoria]):
                        edicao[categoria] = [{'Nome':nome,
                                              'Genero':gender_guesser(nome)} 
                                             if isinstance(nome, str) else nome
                                             for nome in edicao[categoria]]
                    
        for artigo in edicao['Artigos']:
            if 'Autores(as) Referencias' in artigo.keys():
                if artigo['Autores(as) Referencias']:
                    for autor in artigo['Autores(as) Referencias']:
                        if isinstance(autor, dict):
                            autor['Genero'] = gender_guesser(autor['Nome'])
    
            if 'Autores(as)' in artigo.keys():
                if artigo['Autores(as)']:
                    for autor in artigo['Autores(as)']:
                        if isinstance(autor, dict):
                            autor['Genero'] = gender_guesser(autor['Nome'])
    
    print("Salvando resultados...")

    with open("./outputs/edicoes_reh.json", "w", encoding="utf-8") as arquivo:
        json.dump(edicoes_reh, arquivo, ensure_ascii=False, indent=4)
                        
#%%
autores_referencias = pd.DataFrame([
    autor['Nome'].replace('.','') 
    for edicao in edicoes_reh
    for artigo in edicao['Artigos']
    if 'Autores(as) Referencias' in artigo and isinstance(artigo['Autores(as) Referencias'], list)
    for autor in artigo['Autores(as) Referencias'] if autor is not None
]).value_counts()

#%% 
print('Realizando Topic Modelling dos artigos...')

topic_modelling_artigos(edicoes_reh)

#%% 
print("Gerando plots...")

# PLOTS ARTIGOS
for categoria in ['Autores(as)', 'Autores(as) Referencias']:
    plot_generos_por_ano_artigos(edicoes_reh, categoria)

# PLOTS EDIÇÒES
for categoria in ['Conselho Consultivo', 'Editores(as)', 
                  'Editores(as) Convidados(as)', 'Pareceristas ad hoc',
                  'Pareceristas', 'Secretários(as)', 
                  'Digitadores(as)', 'Estagiários(as)'
                  ]:
    plot_generos_por_ano_edicoes(edicoes_reh, categoria)

#%%
print("Gerando linkset de publicações...")

nodeset_referencias, linkset_referencias = geracao_linkset_referencias(edicoes_reh)
nodeset_autores, linkset_autores = geracao_linkset_autores(edicoes_reh)

#%%
print("Processo concluído com sucesso.")