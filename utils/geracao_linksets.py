import pandas as pd
import networkx as nx
from itertools import permutations
import os

def geracao_linkset_referencias(edicoes_reh):
    nodeset = pd.DataFrame(columns = ['ID', 'Label', 'Tipo'])
    linkset = pd.DataFrame(columns = ['Source','Target'])
    
    excluidos = ['Rio Estudos Históricos']

    for edicao in edicoes_reh:
        nodeset = nodeset._append({'ID':edicao['URL'],
                                   'Label':edicao['Titulo'],
                                   'Numero':edicao['Numero'],
                                   'Ano':edicao['Ano'],
                                   'Meses':edicao['Meses'],
                                   'URL':edicao['URL'],
                                   'Tipo':'Edição'},
                                   ignore_index=True)

        for artigo in edicao['Artigos']:
            nodeset = nodeset._append({'ID':artigo['URL'],
                                       'Label':artigo['Titulo'],
                                       'Subtitulo':artigo['Subtitulo'],
                                       'Edicao':artigo['Edicao'],
                                       'Data de Publicação':artigo['Data Publicacao'],
                                       'URL':artigo['URL'],
                                       'Tipo':'Artigo'},
                                       ignore_index=True)

            linkset = linkset._append({'Source':artigo['URL'],
                                       'Target':edicao['URL']},
                                       ignore_index=True)
            if 'Autores(as) Referencias' in artigo:
                if artigo['Autores(as) Referencias']:
                    for autor in artigo['Autores(as) Referencias']:
                        if autor['Nome'] not in excluidos:
                            nodeset = nodeset._append({'ID':autor['Nome'],
                                                       'Label':autor['Nome'],
                                                       'Tipo':'Autor Referenciado'},
                                                       ignore_index=True)
                            linkset = linkset._append({'Source':autor['Nome'],
                                                       'Target':artigo['URL']},
                                                       ignore_index=True)
    nodeset.drop_duplicates(inplace=True)
        
    # Criando o grafo com NetworkX
    G = nx.MultiDiGraph()  # Use DiGraph() para um grafo direcionado
    
    # Adicionando os nós com atributos
    for _, row in nodeset.iterrows():
        # Criando um dicionário de atributos que inclui apenas valores não NaN
        atributos = {col: row[col] for col in ['Tipo', 'Subtitulo', 'Edicao', 'Data de Publicação', 
                                               'Numero', 'Ano', 'Meses', 'URL'] if pd.notna(row[col])}
        
        # Adicionando o nó com atributos
        G.add_node(row['ID'], label=row['Label'], **atributos)

    
    # Adicionando as arestas
    for _, row in linkset.iterrows():
        G.add_edge(row['Source'], row['Target'])
    
    if not os.path.exists('./outputs/networks'):
        os.makedirs('./outputs/networks')
    if not os.path.exists('./outputs/networks/gephi'):
        os.makedirs('./outputs/networks/gephi')

    # Exportando para .gexf
    output_file = "./outputs/networks/gephi/grafo_referencias_REH.gexf"
    nx.write_gexf(G, output_file)    

    return nodeset, linkset

def geracao_linkset_autores(edicoes_reh):
    nodeset = pd.DataFrame(columns = ['ID', 'Label', 'Tipo'])
    linkset = pd.DataFrame(columns = ['Source','Target'])

    for edicao in edicoes_reh:
        nodeset = nodeset._append({'ID':edicao['URL'],
                                   'Label':edicao['Titulo'],
                                   'Numero':edicao['Numero'],
                                   'Ano':edicao['Ano'],
                                   'Meses':edicao['Meses'],
                                   'URL':edicao['URL'],
                                   'Tipo':'Edição'},
                                   ignore_index=True)

        for artigo in edicao['Artigos']:
            nodeset = nodeset._append({'ID':artigo['URL'],
                                       'Label':artigo['Titulo'],
                                       'Subtitulo':artigo['Subtitulo'],
                                       'Edicao':artigo['Edicao'],
                                       'Data de Publicação':artigo['Data Publicacao'],
                                       'URL':artigo['URL'],
                                       'Tipo':'Artigo'},
                                       ignore_index=True)

            linkset = linkset._append({'Source':artigo['URL'],
                                       'Target':edicao['URL']},
                                       ignore_index=True)
            if 'Autores(as)' in artigo:
                for autor in artigo['Autores(as)']:
                    nodeset = nodeset._append({'ID':autor['Nome'],
                                               'Label':autor['Nome'],
                                               'Tipo':'Autor'},
                                               ignore_index=True)
                    linkset = linkset._append({'Source':autor['Nome'],
                                               'Target':artigo['URL']},
                                               ignore_index=True)
                    
                # Criar uma lista para armazenar as coocorrências
                coocorrencias = []
                nomes = [autor['Nome'] for autor in artigo['Autores(as)']]
                pares = list(permutations(nomes, 2))
                coocorrencias.extend(pares)
                
                # Criar o DataFrame com as colunas "Source" e "Target"
                bd_coocorrencias = pd.DataFrame(coocorrencias, columns=['Source', 'Target'])
                linkset = pd.concat([linkset, bd_coocorrencias], ignore_index=True)


    nodeset.drop_duplicates(inplace=True)
        
    # Criando o grafo com NetworkX
    G = nx.MultiDiGraph()  # Use DiGraph() para um grafo direcionado
            
    for _, row in nodeset.iterrows():
        # Criando um dicionário de atributos que inclui apenas valores não NaN
        atributos = {col: row[col] for col in ['Tipo', 'Subtitulo', 'Edicao', 'Data de Publicação', 
                                               'Numero', 'Ano', 'Meses', 'URL'] if pd.notna(row[col])}
        
        # Adicionando o nó com atributos
        G.add_node(row['ID'], label=row['Label'], **atributos)
    
    # Adicionando as arestas
    for _, row in linkset.iterrows():
        G.add_edge(row['Source'], row['Target'])

    if not os.path.exists('./outputs/networks'):
        os.makedirs('./outputs/networks')
    if not os.path.exists('./outputs/networks/gephi'):
        os.makedirs('./outputs/networks/gephi')

    # Exportando para .gexf
    output_file = "./outputs/networks/gephi/grafo_autores_REH.gexf"
    nx.write_gexf(G, output_file)    

    return nodeset, linkset

