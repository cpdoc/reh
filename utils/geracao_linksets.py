import pandas as pd
import networkx as nx
from itertools import permutations

def geracao_linkset_referencias(edicoes_reh):
    nodeset = pd.DataFrame(columns = ['ID', 'Label', 'Tipo'])
    linkset = pd.DataFrame(columns = ['Source','Target'])

    for edicao in edicoes_reh:
        nodeset = nodeset._append({'ID':edicao['URL'],
                                   'Label':edicao['Titulo'],
                                   'Tipo':'Edição'},
                                   ignore_index=True)

        for artigo in edicao['Artigos']:
            nodeset = nodeset._append({'ID':artigo['URL'],
                                       'Label':artigo['Titulo'],
                                       'Tipo':'Artigo'},
                                       ignore_index=True)

            linkset = linkset._append({'Source':artigo['URL'],
                                       'Target':edicao['URL']},
                                       ignore_index=True)
            if 'Autores Referencias' in artigo:
                for autor in artigo['Autores Referencias']:
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
        G.add_node(row['ID'], label=row['Label'], tipo=row['Tipo'])
    
    # Adicionando as arestas
    for _, row in linkset.iterrows():
        G.add_edge(row['Source'], row['Target'])
    
    # Exportando para .gexf
    output_file = "./outputs/grafo_referencias_REH.gexf"
    nx.write_gexf(G, output_file)    

    return nodeset, linkset

def geracao_linkset_autores(edicoes_reh):
    nodeset = pd.DataFrame(columns = ['ID', 'Label', 'Tipo'])
    linkset = pd.DataFrame(columns = ['Source','Target'])

    for edicao in edicoes_reh:
        nodeset = nodeset._append({'ID':edicao['URL'],
                                   'Label':edicao['Titulo'],
                                   'Tipo':'Edição'},
                                   ignore_index=True)

        for artigo in edicao['Artigos']:
            nodeset = nodeset._append({'ID':artigo['URL'],
                                       'Label':artigo['Titulo'],
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
    
    # Adicionando os nós com atributos
    for _, row in nodeset.iterrows():
        G.add_node(row['ID'], label=row['Label'], tipo=row['Tipo'])
    
    # Adicionando as arestas
    for _, row in linkset.iterrows():
        G.add_edge(row['Source'], row['Target'])
    
    # Exportando para .gexf
    output_file = "./outputs/grafo_autores_REH.gexf"
    nx.write_gexf(G, output_file)    

    return nodeset, linkset

