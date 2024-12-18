import requests
from bs4 import BeautifulSoup
import re

def get_edicoes_reh():
    
    def corrigir_chaves(lista_dicionarios, mapeamento_chaves):
        nova_lista = []
        
        # Converter o mapeamento de chaves para ter todas as chaves em minúsculas
        mapeamento_chaves_lower = {k.lower(): v for k, v in mapeamento_chaves.items()}
        
        for dicionario in lista_dicionarios:
            novo_dict = {}
            
            for chave, valor in dicionario.items():
                # Converter a chave atual para minúscula para verificar no mapeamento
                chave_lower = chave.lower()
                
                # Se a chave em minúsculo está no mapeamento, corrigir
                if chave_lower in mapeamento_chaves_lower:
                    nova_chave = mapeamento_chaves_lower[chave_lower]
                    # Se a nova chave já existe, concatenar os valores
                    if nova_chave in novo_dict:
                        novo_dict[nova_chave] += f", {valor}"
                    else:
                        novo_dict[nova_chave] = valor
                else:
                    # Se a chave não está no mapeamento, mantê-la inalterada
                    novo_dict[chave] = valor
            
            nova_lista.append(novo_dict)
        
        return nova_lista

    mapeamento_chaves = {
        'Estagiário' : 'Estagiários/as',
        'Estagiária' : 'Estagiários/as',
        'Estagiários' : 'Estagiários/as',
        'Estagiárias' : 'Estagiários/as',
        'Editor Convidado' : 'Editores(as) Convidados(as)',
        'Editora Convidada' : 'Editores(as) Convidados(as)',
        'Editores Convidados' : 'Editores(as) Convidados(as)',
        'Editoras Convidadas' : 'Editores(as) Convidados(as)',
        'Secretário' : 'Secretários(as)',
        'Secretária' : 'Secretários(as)',
        'Secretários' : 'Secretários(as)',
        'Secretárias' : 'Secretários(as)',
        'Editor' : 'Editores(as)',
        'Editora' : 'Editores(as)',
        'Editores' : 'Editores(as)',
        'Editoras' : 'Editores(as)',
        'Digitador' : 'Digitadores(as)',
        'Digitadora' : 'Digitadores(as)',
        'Digitadores' : 'Digitadores(as)',
        'Digitadoras' : 'Digitadores(as)',
        'Pareceristasad hoc' : 'Pareceristas ad hoc'
    }

    # URL da página prrincipal
    url = "https://periodicos.fgv.br/reh/issue/archive"
    
    # Cabeçalho para simular um navegador real
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    # Faz a requisição para a página com o cabeçalho
    response = requests.get(url, headers=headers)
    
    #%%
    
    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Parseia o conteúdo HTML da página
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Encontra a <ul> que contém a classe 'issues_archive'
        issues_ul = soup.find('ul', class_='issues_archive')
        
        # Inicializa a lista que armazenará os dados
        issues_list = []
        
        # Itera sobre cada <li> dentro da <ul>
        for issue in issues_ul.find_all('li'):
            # Extrai o link e título
            title_tag = issue.find('a', class_='title')
            title = title_tag.text.strip() if title_tag else None
            link = title_tag['href'] if title_tag else None
            
            # Extrai a série (número da edição)
            series_tag = issue.find('div', class_='series')
            series = series_tag.text.strip() if series_tag else None
            versao = re.findall(r"v\.\s*(\d+)", series)[0]
            numero = re.findall(r"n\.\s*(\d+)", series)[0]
            ano = re.findall(r"\(\s*(\d+)\s*\)", series)[0]
            
            # Extrai a descrição e captura todos os <p>
            description_tag = issue.find('div', class_='description')
            
            ###
            
            meses = description_tag.find_all('p')[0].get_text(strip=True) if not description_tag.find_all('p')[0].find('strong') else None
            
            nomes_metadados_edicao = {}
            current_key = None
            for p in description_tag.find_all('p'):
                strong_tag = p.find('strong')
                
                # Se encontrarmos uma tag <strong>, definimos a chave
                if strong_tag:
                    current_key = strong_tag.get_text(strip=True)
                    if len(current_key) > 0:
                        nomes_metadados_edicao[current_key] = []
                # Se for um parágrafo sem <strong>, adicionamos o texto ao valor da chave corrente
                elif current_key:
                    nomes_metadados_edicao[current_key].append(p.get_text(strip=True))
            
            # Converter as listas de valores em strings unidas por vírgula
            for key, value in nomes_metadados_edicao.items():
                nomes_metadados_edicao[key] = ', '.join(value)
                    
            # Extrai a imagem da capa
            cover_tag = issue.find('a', class_='cover')
            if cover_tag:
                img  = cover_tag.find('img')
                cover_url = img['src'] if img else None
            else:
                cover_url = None
            
            # Monta o dicionário com os dados, incluindo os pares chave-valor e 'meses'
            issue_data = {
                'Titulo': title,
                'URL': link,
                'Versao':versao,
                'Numero':numero,
                'Ano':ano,
                'Meses': meses,  # Primeiro item extraído da descrição
                'Capa': cover_url
            }
            
            # Adiciona os pares chave-valor extraídos ao dicionário raiz
            issue_data.update(nomes_metadados_edicao)
            
            # Adiciona os dados extraídos à lista
            issues_list.append(issue_data)
        
        issues_list = corrigir_chaves(issues_list, mapeamento_chaves)
        return issues_list
    else:
        print(f"Erro ao acessar a página: {response.status_code}")