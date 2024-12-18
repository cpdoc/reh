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

if input('Ler últimos dados salvos (1) ou coletar novamente (2)?\n') == '1':
    with open("./Outputs/edicoes_reh.json", "r", encoding="utf-8") as arquivo:
        edicoes_reh = json.load(arquivo)
else:
    print("Coletando conjunto de edições publicadas...")
    edicoes_reh = get_edicoes_reh()
    print(f"{len(edicoes_reh)} edições identificadas.")
    
    edicoes_reh = [d for d in edicoes_reh if int(d.get("Ano", 0)) >= 2001]
    
    #%%
    for edicao in tqdm(edicoes_reh, desc="Coletando artigos das edições..."):
        if 'Artigos' not in edicao.keys():
            edicao['Artigos'] = get_artigos_edicao(edicao)
    
    #%%
    for edicao in tqdm(edicoes_reh, desc="Coletando autores das bibliografias...", position=0):
        # for artigo in tqdm(edicao['Artigos'], desc=f"{edicao['Titulo']}", position=1, leave=False):
        for artigo in edicao['Artigos']:
            if 'Autores Referencias' not in artigo.keys():
                artigo['Autores Referencias'] = get_autores_referencias(artigo)
    
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
                        edicao[categoria] = [gender_guesser(nome) 
                                             if isinstance(nome, str) else nome
                                             for nome in edicao[categoria]]
                    
        for artigo in edicao['Artigos']:
            if 'Autores Referencias' in artigo.keys():
                if artigo['Autores Referencias']:
                    for autor in artigo['Autores Referencias']:
                        autor['Genero'] = gender_guesser(autor['Nome'])

            if 'Autores(as)' in artigo.keys():
                if artigo['Autores(as)']:
                    for autor in artigo['Autores(as)']:
                        autor['Genero'] = gender_guesser(autor['Nome'])

#%%
autores_referencias = pd.DataFrame([
    autor['Nome'].replace('.','')
    for edicao in edicoes_reh
    for artigo in edicao['Artigos']
    if 'Autores Referencias' in artigo.keys()
    for autor in artigo['Autores Referencias']
]).value_counts()

#%%
print("Gerando linkset de publicações...")
nodeset_referencias, linkset_referencias = geracao_linkset_referencias(edicoes_reh)

nodeset_autores, linkset_autores = geracao_linkset_autores(edicoes_reh)

with open("./Outputs/edicoes_reh.json", "w", encoding="utf-8") as arquivo:
    json.dump(edicoes_reh, arquivo, ensure_ascii=False, indent=4)

#%% PLOTS

plot_generos_por_ano_artigos(edicoes_reh, 'Autores(as)')
plot_generos_por_ano_artigos(edicoes_reh, 'Autores Referencias')
plot_generos_por_ano_edicoes(edicoes_reh, 'Editores(as)')
plot_generos_por_ano_edicoes(edicoes_reh, 'Pareceristas ad hoc')
plot_generos_por_ano_edicoes(edicoes_reh, 'Pareceristas ad hoc')

#%%
artigos_abreviados = []
for edicao in tqdm(edicoes_reh, desc="Identificando nomes/gêneros dos metadados..."):
    for artigo in edicao['Artigos']:
        if 'Autores Referencias' in artigo.keys():
            for autor in artigo['Autores Referencias']:
                if len(autor['Nome'].split()[0]) == 1:
                    artigos_abreviados.append(artigo)
            if artigo['Autores Referencias'] is None:
                artigo['Autores Referencias'] = []
