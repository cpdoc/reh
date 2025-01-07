from pdf2image import convert_from_bytes
from pytesseract import pytesseract
import re
from io import BytesIO
import requests

def get_autores_referencias(artigo):
    
    # Função para localizar a seção de referências
    def find_references_section(texto):
        """
        Encontra a seção de referências com base em padrões comuns.
        
        :param texto: Texto completo do documento
        :return: Texto a partir da seção de referências
        """
        pattern = r"refer[êe]nc(ia|ias|es)|bibliogra(fia|phy)"
        match = re.search(pattern, texto, re.IGNORECASE)
        
        if match:
            # Retorna o texto a partir do início da seção de referências
            return texto[match.start():]
        else:
            return None

    def extract_author_names(referencia):
        """
        Extrai o nome do autor (ou autores) de uma referência no formato:
        ULTIMO, Primeiro Segundo ou ULTIMO, Primeiro Segundo.
        
        :param referencia: String contendo uma referência completa
        :return: Lista de autores extraídos
        """
        # Expressão regular para capturar o padrão: ULTIMO, Primeiro Segundo (opcionalmente seguido de ponto)
        # padrao_autor = r"([A-Z]+),\s([A-Z][a-z]+(?:\s[A-Z][a-z]+)*\.?)"
        padrao_autor = r'([A-ZÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÃÕÄËÏÖÜÇÑ-]{2,}(?: [A-ZÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÃÕÄËÏÖÜÇÑ-]+)*)\,?\s+([A-Z][a-záéíóúàèìòùâêîôûãõäëïöüç.]+(?:\s+[A-Z][a-záéíóúàèìòùâêîôûãõäëïöüç]+)*)\s*(?:et al\.)?'
        
        # Busca por todas as correspondências que seguem o padrão de nomes
        autores = re.findall(padrao_autor, referencia)
        
        # Formatar a lista de autores: juntar o sobrenome e o(s) primeiro(s) nome(s)
        # autores_formatados = [f"{nomes.strip('.')} {sobrenome.title()}".strip() for sobrenome, nomes in autores]
        autores_formatados = [{'Nome':(re.sub(' +', ' ', autor[1].strip()) + 
                               ' ' + 
                               re.sub(' +', ' ', autor[0].title().strip())).replace('.','')} 
                              for autor in autores]

        return autores_formatados

    # Função para dividir e isolar as referências individuais
    def split_references(texto_referencias):
        """
        Divide as referências com base em padrões comuns (números ou letras maiúsculas).
        
        :param texto_referencias: Texto da seção de referências
        :return: Lista de referências individuais
        """
        # Dividindo com base em quebras de linha e numerais ou letras maiúsculas
        referencias = re.split(r"\n\n(?=[A-Z\s]+[A-Z]{2,})", texto_referencias)
        
        # Limpar as referências (remover espaços em branco desnecessários)
        referencias = [ref.strip() for ref in referencias if ref.strip()]
        
        return referencias

    # Função principal para extrair e processar as referências do PDF
    def extract_references_from_pdf(pdf_path):
        """
        Extraí todas as referências bibliográficas de um PDF.
        
        :param pdf_path: Caminho para o arquivo PDF
        :return: Lista de referências extraídas
        """
        
        pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        imagens = convert_from_bytes(pdf_path.getvalue(), 
                                     poppler_path="C:\\Program Files\\poppler-24.08.0\\Library\\bin")
        texto = ""

        for imagem in reversed(imagens):
            texto = pytesseract.image_to_string(imagem, lang="por") + ' \n ' + texto
        
            references_section = find_references_section(texto)
            if references_section:
                # Dividir e retornar as referências individuais
                referencias = split_references(references_section)
                referencias = [referencia.replace('\n'," ") for referencia in referencias]
                referencias = [re.sub(r'(?<!\b\w)\.', '', referencia) for referencia in referencias]
                
                return references_section, referencias
            
        print(f"Seção de referências não encontrada para o artigo {artigo['URL']}.")
        return [], []
    
    if artigo['URL_PDF']:
        url = artigo['URL_PDF'].replace('view','download')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            pdf_path = BytesIO(response.content)
            references_section, referencias_extraidas = extract_references_from_pdf(pdf_path)
            
            # Exibindo as referências extraídas
            if referencias_extraidas:
                artigo['Referencias'] = referencias_extraidas
        
            autores = []
            for i, ref in enumerate(referencias_extraidas):
                autores.extend(extract_author_names(ref))
                    
            return autores
        else:
            print("Erro ao coletar seção de referências.")
            return None