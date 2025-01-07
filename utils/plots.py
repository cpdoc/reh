import matplotlib.pyplot as plt
import os 
import seaborn as sns
import numpy as np
import pandas as pd

# Configuração para evitar conflito de OpenMP
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

def plot_generos_por_ano_artigos(edicoes_reh, categoria):
    
    if not os.path.exists('./outputs/plots'):
        os.makedirs('./outputs/plots')
    
    # Preparar os dados para análise
    entries = []
    
    # Iterar sobre as edições
    for edition in edicoes_reh:
        ano = edition.get('Ano')
        artigos = edition.get('Artigos', [])
    
        if not artigos:
            print(f"Aviso: Nenhum artigo encontrado para a edição do ano {ano}.")
    
        # Iterar sobre os artigos
        for artigo in artigos:
            autores_referencias = artigo.get(categoria, [])
        
            # Iterar sobre os autores nas referências
            if autores_referencias:
                for autor in autores_referencias:
                    genero = autor.get('Genero', 'Desconhecido')
                    entries.append({'Ano': ano, 'Genero': genero})
    
    if not entries:
        print("Erro: A lista 'entries' está vazia. Verifique a estrutura do JSON.")
    
    # Criar um DataFrame
    df = pd.DataFrame(entries)
    
    if df.empty:
        print("Erro: O DataFrame está vazio. Não há dados para processar.")
    else:
        # Contar o número de homens, mulheres e outros gêneros por ano
        genero_por_ano = df.groupby(['Ano', 'Genero']).size().reset_index(name='Quantidade')
        
        # Calcular a diferença entre homens e mulheres (isso requer ajustes no agrupamento inicial)
        genero_pivot = genero_por_ano.pivot(index='Ano', columns='Genero', values='Quantidade').fillna(0)
        genero_pivot['Diferença'] = genero_pivot.get('Masculino', 0) - genero_pivot.get('Feminino', 0)
        genero_por_ano = genero_pivot.reset_index().melt(id_vars=['Ano', 'Diferença'], var_name='Genero', value_name='Quantidade')
        
        # Adicionar coluna numérica para regressão
        genero_por_ano['Ano_Num'] = pd.to_numeric(genero_por_ano['Ano'], errors='coerce')
        
        # Definir as cores
        cores = {
            'Masculino': 'cornflowerblue',
            'Feminino': 'orchid',
            'Desconhecido': 'darkgray'
        }
        
        # Primeiro gráfico: Quantidade por gênero
        plt.figure(figsize=(12, 6))
        sns.lineplot(
            data=genero_por_ano[genero_por_ano['Genero'] != 'Diferença'],  # Excluir diferença do primeiro gráfico
            x='Ano',
            y='Quantidade',
            hue='Genero',
            palette=cores,
            marker='o'
        )
        plt.title(f'Gêneros por ano de publicação dos artigos na categoria {categoria}', weight='bold')
        plt.xlabel('Ano', weight='bold')
        plt.ylabel('Quantidade', weight='bold')
        plt.legend(title='Gênero')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"./outputs/plots/generos_{categoria}.png", dpi=300)
        
        # Segundo gráfico: Diferença de homens e mulheres
        plt.figure(figsize=(10, 6))
        sns.lineplot(
            data=genero_pivot,
            x='Ano',
            y='Diferença',
            marker='o',
            color='purple',
            label='Diferença (Masculino - Feminino)'
        )
        
        # Adicionar linha de tendência
        z = np.polyfit(genero_pivot.index.astype(float), genero_pivot['Diferença'], 1)
        p = np.poly1d(z)
        plt.plot(genero_pivot.index, p(genero_pivot.index.astype(float)), linestyle='--', color='orange', label='Tendência')
        
        plt.title(f'Diferença de homens e mulheres por ano na categoria {categoria}', weight='bold')
        plt.xlabel('Ano', weight='bold')
        plt.ylabel('Diferença (Homens - Mulheres)', weight='bold')
        plt.axhline(0, color='darkgray', linestyle='--', linewidth=0.8)
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"./outputs/plots/diferenca_generos_{categoria}.png", dpi=300)
        
def plot_generos_por_ano_edicoes(edicoes_reh, categoria):

    if not os.path.exists('./outputs/plots'):
        os.makedirs('./outputs/plots')
    
    # Preparar os dados para análise
    entries = []
    
    # Iterar sobre as edições
    for edition in edicoes_reh:
        ano = edition.get('Ano')
        
        edition_referencias = edition.get(categoria, [])
    
        # Iterar sobre os autores nas referências
        for autor in edition_referencias:
            genero = autor.get('Genero', 'Desconhecido')
            entries.append({'Ano': ano, 'Genero': genero})
    
    if not entries:
        print("Erro: A lista 'entries' está vazia. Verifique a estrutura do JSON.")
    
    # Criar um DataFrame
    df = pd.DataFrame(entries)
    
    if df.empty:
        print("Erro: O DataFrame está vazio. Não há dados para processar.")
    else:
        # Contar o número de homens, mulheres e outros gêneros por ano
        genero_por_ano = df.groupby(['Ano', 'Genero']).size().reset_index(name='Quantidade')
        
        # Calcular a diferença entre homens e mulheres (isso requer ajustes no agrupamento inicial)
        genero_pivot = genero_por_ano.pivot(index='Ano', columns='Genero', values='Quantidade').fillna(0)
        genero_pivot['Diferença'] = genero_pivot.get('Masculino', 0) - genero_pivot.get('Feminino', 0)
        genero_por_ano = genero_pivot.reset_index().melt(id_vars=['Ano', 'Diferença'], var_name='Genero', value_name='Quantidade')
        
        # Adicionar coluna numérica para regressão
        genero_por_ano['Ano_Num'] = pd.to_numeric(genero_por_ano['Ano'], errors='coerce')
        
        # Definir as cores
        cores = {
            'Masculino': 'cornflowerblue',
            'Feminino': 'orchid',
            'Desconhecido': 'darkgray'
        }
        
        # Primeiro gráfico: Quantidade por gênero
        plt.figure(figsize=(12, 6))
        sns.lineplot(
            data=genero_por_ano[genero_por_ano['Genero'] != 'Diferença'],  # Excluir diferença do primeiro gráfico
            x='Ano',
            y='Quantidade',
            hue='Genero',
            palette=cores,
            marker='o'
        )
        plt.title(f'Gêneros por ano de publicação das edições na categoria {categoria}', weight='bold')
        plt.xlabel('Ano', weight='bold')
        plt.ylabel('Quantidade', weight='bold')
        plt.legend(title='Gênero')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"./outputs/plots/generos_{categoria}.png", dpi=300)

        
        # Segundo gráfico: Diferença de homens e mulheres
        plt.figure(figsize=(10, 6))
        sns.lineplot(
            data=genero_pivot,
            x='Ano',
            y='Diferença',
            marker='o',
            color='purple',
            label='Diferença (Masculino - Feminino)'
        )
        
        # Adicionar linha de tendência
        z = np.polyfit(genero_pivot.index.astype(float), genero_pivot['Diferença'], 1)
        p = np.poly1d(z)
        plt.plot(genero_pivot.index, p(genero_pivot.index.astype(float)), linestyle='--', color='orange', label='Tendência')
        
        plt.title(f'Diferença de homens e mulheres por ano na categoria {categoria}', weight='bold')
        plt.xlabel('Ano', weight='bold')
        plt.ylabel('Diferença (Homens - Mulheres)', weight='bold')
        plt.axhline(0, color='darkgray', linestyle='--', linewidth=0.8)
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"./outputs/plots/diferenca_generos_{categoria}.png", dpi=300)
