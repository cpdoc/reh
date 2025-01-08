
# Documentação - FGV/CPDOC
## Historiografia Visual: Análise de Publicações da REH

**Pesquisador Responsável:**  
Daniel Bonatto Seco (<danielbonattoseco@hotmail.com>)

---

## Como executar o projeto

Siga os passos abaixo para configurar e executar o projeto:

1. Acesse o diretório do projeto:
   ```bash
   cd pasta-do-projeto
   ```

2. Instale as dependências listadas no arquivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute o arquivo principal do projeto:
   ```bash
   python main.py
   ```

Certifique-se de que você tenha o Python instalado e configurado corretamente em sua máquina antes de iniciar os passos acima.
```

## Estrutura de Dados

```json
{
    "Titulo": "string", // Título da edição
    "URL": "string", // URL da edição
    "Versao": "string", // Versão da edição
    "Numero": "string", // Número da edição
    "Ano": "string", // Ano de publicação
    "Meses": "string", // Período de meses coberto pela edição
    "Capa": "string", // URL da imagem da capa
    "Editores(as)": [ // Lista de editores(as)
        {
            "Nome": "string", // Nome do(a) editor(a)
            "Genero": "string" // Gênero do(a) editor(a)
        }
    ],
    "Editores(as) Convidados(as)": [ // Lista de editores(as) convidados(as)
        {
            "Nome": "string", // Nome do(a) editor(a) convidado(a)
            "Genero": "string" // Gênero do(a) editor(a) convidado(a)
        }
    ],
    "Conselho Consultivo": [ // Lista de membros do conselho consultivo
        {
            "Nome": "string", // Nome do membro
            "Genero": "string" // Gênero do membro
        }
    ],
    "Secretários(as)": [ // Lista de secretários(as)
        {
            "Nome": "string", // Nome do(a) secretário(a)
            "Genero": "string" // Gênero do(a) secretário(a)
        }
    ],
    "Editoração Eletrônica/Capa": "string", // Responsável pela editoração/capa
    "Revisão": "string", // Responsável pela revisão
    "Pareceristas ad hoc": [ // Lista de pareceristas
        {
            "Nome": "string", // Nome do(a) parecerista
            "Genero": "string" // Gênero do(a) parecerista
        }
    ],
    "Artigos": [ // Lista de artigos na edição
        {
            "Titulo": "string", // Título do artigo
            "Subtitulo": "string", // Subtítulo do artigo
            "Autores(as)": [ // Lista de autores(as)
                {
                    "Nome": "string", // Nome do(a) autor(a)
                    "Afiliacao": "string", // Afiliação do(a) autor(a)
                    "Genero": "string" // Gênero do(a) autor(a)
                }
            ],
            "Palavras chave": ["string"], // Lista de palavras-chave
            "Resumo": "string", // Resumo do artigo
            "Data Publicacao": "string", // Data de publicação
            "Edicao": "string", // Edição do artigo
            "URL": "string", // URL do artigo
            "URL_PDF": "string", // URL do PDF do artigo
            "Referencias": ["string"], // Lista de referências
            "Autores Referencias": [ // Lista de autores nas referências
                {
                    "Nome": "string", // Nome do autor(a) nas referências
                    "Genero": "string" // Gênero do autor(a) nas referências
                }
            ]
        }
    ]
}
```

# Resumo do Andamento - Escopo de Trabalho

| **Atividade**                                   | **Metodologia**                                                                                   | **Status**               |
|------------------------------------------------|--------------------------------------------------------------------------------------------------|--------------------------|
| **Coleta e conversão dos PDFs publicados**     | *Crawling + Webscraping - [Beautifulsoup](https://pypi.org/project/beautifulsoup4/)*                                             | **Concluído**            |
| **Identificação automatizada de referências e autores referenciados** | *REGEX + Optical Character Recognition - OCR ([pdf2image](https://pypi.org/project/pdf2image/) + [pytesseract](https://pypi.org/project/pytesseract/))*                                                                                         | **Concluído**            |
| **Estruturação de metadados da revista** (ano, volume, número, dossiê temático, nome e informações dos autores, título, palavras-chave) | *Webscraping - [Beautifulsoup](https://pypi.org/project/beautifulsoup4/)* | **Concluído** |
| **Inferência de gênero dos autores dos artigos e dos autores referenciados** | *[gender-guesser](https://pypi.org/project/gender-guesser/)*           | **Concluído**            |
| **Inferência de região das instituições**      | *Inteligência Artificial (LLMs)*                                                                | **A realizar**           |
| **Identificação de Temas**                     | *Topic Modelling - [NLTK](https://www.nltk.org/) + [Spacy](https://spacy.io/) +  [LDA](https://radimrehurek.com/gensim/models/ldamodel.html)* | **Concluído**           |
| **Gráfico interativo - temas**                 | *[pyLDAvis](https://github.com/bmabey/pyLDAvis)*                                                                               | **Concluído**           |
| **Grafo interativo - citações**                | *[NetworkX](https://networkx.org/) + [Gephi](https://gephi.org/) + [SigmaJS](https://www.sigmajs.org/)*                                                                      | **Concluído**           |
| **Grafo interativo - coautoria de artigos**    | *[NetworkX](https://networkx.org/) + [Gephi](https://gephi.org/) + [SigmaJS](https://www.sigmajs.org/)*                                                                      | **Concluído**           |
| **Gráfico estático - quantidade de homens e mulheres citados ao longo do tempo** | *Python + [Seaborn](https://seaborn.pydata.org/)*                                                                              | **Concluído**           |
| **Gráfico estático - regiões dos autores e autoras da REH** | *Python + [Seaborn](https://seaborn.pydata.org/)*                                                                              | **A realizar**           |
| **Gráfico estático - quantidade de homens e mulheres autores na REH** | *Python + [Seaborn](https://seaborn.pydata.org/)*                                                                              | **Concluído**           |

