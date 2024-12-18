import requests
from bs4 import BeautifulSoup

def get_artigos_edicao(edicao):
    # Cabeçalho para simular um navegador real
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    url = edicao['URL']
    # Faz a requisição para a página com o cabeçalho
    response = requests.get(url, headers=headers)
    
    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Parseia o conteúdo HTML da página
        soup = BeautifulSoup(response.content, 'html.parser')
        
        sections = soup.find_all('div', class_='section')

        for section in sections:
            # Procura o h2 dentro da section
            h2 = section.find('h2')
            
            # Verifica se o h2 contém o texto 'Artigos'
            if h2 and 'Artigos' in h2.get_text():
                # Encontra a <ul> que contém a classe 'issues_archive'
                issues_ul = section.find('ul', class_='cmp_article_list articles')
                
                artigos = []
                
                if issues_ul:
                    for artigo in issues_ul.find_all('div', class_='obj_article_summary'):
                        url = artigo.find('a')['href']
                        response = requests.get(url, headers=headers)
                        
                        if response.status_code == 200:
                            soup = BeautifulSoup(response.content, 'html.parser')
                            
                            #TITULO
                            titulo = soup.find('h1', class_='page_title')
                            if titulo:
                                titulo = titulo.get_text(strip=True)
                            else:
                                titulo = None
                            
                            #SUBTITULO
                            subtitulo = soup.find('h2', class_='subtitle')
                            if subtitulo:
                                subtitulo = subtitulo.get_text(strip=True)
                            else:
                                subtitulo = None
                            
                            #AUTORES
                            autores = []
                            autores_ul = soup.find('ul', class_='authors')
                            if autores_ul:
                                for autor in autores_ul.find_all('li'):
                                    
                                    #NOME AUTORES
                                    autor_nome = autor.find('span', class_='name')
                                    if autor_nome:
                                        autor_nome = autor_nome.get_text(strip=True)
                                    else:
                                        autor_nome = None
                                    
                                    #AFILIACAO AUTORES
                                    afiliacao = autor.find('span', class_='affiliation')
                                    if afiliacao:
                                        afiliacao = afiliacao.get_text(strip=True)
                                    else:
                                        afiliacao = None
                                    autores.append({'Nome':autor_nome,
                                                    'Afiliacao':afiliacao})
                            
                            #PALAVRAS CHAVE
                            palavras_chave_section = soup.find('section', class_='item keywords')
                            if palavras_chave_section:
                                palavras_chave = palavras_chave_section.find('span', class_='value')
                                if palavras_chave:
                                    palavras_chave = palavras_chave.get_text(strip=True)
                                    palavras_chave = [palavra_chave.strip().lower() for palavra_chave in palavras_chave.split(',')]
                                else:
                                    palavras_chave = None
                            else:
                                palavras_chave = None
                            
                            #RESUMO
                            resumo = soup.find('section', class_='item abstract')
                            if resumo:
                                try:
                                    resumo = resumo.find('p').get_text(strip=True)
                                except:
                                    resumo = resumo.get_text(strip=True)
                            else:
                                resumo = None
                            
                            #URL PDF
                            url_pdf = soup.find('a', class_='obj_galley_link pdf')
                            if url_pdf:
                                url_pdf = url_pdf['href']
                            else:
                                url_pdf = None
                            
                            #DATA PUBLICAÇÃO
                            data_publicacao_section = soup.find('div', class_='item published')
                            data_publicacao = data_publicacao_section.find('div', class_='value')
                            if data_publicacao:
                                data_publicacao = data_publicacao.get_text(strip=True)
                            else:
                                data_publicacao = None
                            
                            #EDIÇÃO
                            edicao_section = soup.find('div', class_='item issue')
                            edicao = edicao_section.find('a', class_='title')
                            if edicao:
                                edicao = edicao.get_text(strip=True)
                            else:
                                edicao = None
                            
                            #GERAÇÃO DICIONÁRIO DE METADADOS DO ARTIGO
                            artigos.append({
                            'Titulo' : titulo,
                            'Subtitulo' : subtitulo,
                            'Autores(as)' : autores,
                            'Palavras chave' : palavras_chave,
                            'Resumo' : resumo,
                            'Data Publicacao' : data_publicacao,
                            'Edicao' : edicao,
                            'URL' : url,
                            'URL_PDF' : url_pdf
                                })

                        else:
                            print(f"Erro na requisição para a URL {url}: {response.status_code}")
                        # title_element = artigo.find('h3', class_='title')
                        # if title_element:
                        #     a_tag = title_element.find('a')
                        #     titulo = a_tag.find(string=True, recursive=False).strip()
                            
                        #     subtitulo_tag = a_tag.find('span', class_='subtitle')
                        #     subtitulo = subtitulo_tag.get_text(strip=True) if subtitulo_tag else None
                
                        #     autores_tag = artigo.find('div', class_='authors')
                        #     autores = autores_tag.get_text(strip=True) if autores_tag else None
                            
                        #     # Link para o artigo completo
                        #     url = title_element.a['href'] if title_element and title_element.a else None
                            
                        #     # Link para o PDF
                        #     pdf_url_tag = artigo.find('a', class_='obj_galley_link pdf')
                        #     pdf_url = pdf_url_tag['href'] if pdf_url_tag else None
            
                        #     artigos.append({
                        #     'Titulo': titulo,
                        #     'Subtitulo': subtitulo,
                        #     'Autores(as)': autores,
                        #     'URL' : url,
                        #     'URL_PDF' : pdf_url
                        #         })
                
                return artigos
    else:
        return f"Erro na requisição para a URL {url}: {response.status_code}"