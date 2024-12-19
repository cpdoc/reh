
# Documentação - FGV/CPDOC
## Historiografia Visual: Análise de Publicações da REH

**Pesquisador Responsável:**  
Daniel Bonatto Seco (<danielbonattoseco@hotmail.com>)

---

## Estrutura de Dados

```json
{
    "**Titulo**": "string", /* *Título da edição* */
    "**URL**": "string", /* *URL da edição* */
    "**Versao**": "string", /* *Versão da edição* */
    "**Numero**": "string", /* *Número da edição* */
    "**Ano**": "string", /* *Ano de publicação* */
    "**Meses**": "string", /* *Período de meses coberto pela edição* */
    "**Capa**": "string", /* *URL da imagem da capa* */
    "**Editores(as)**": [ /* *Lista de editores(as)* */
        {
            "**Nome**": "string", /* *Nome do(a) editor(a)* */
            "**Genero**": "string" /* *Gênero do(a) editor(a)* */
        }
    ],
    "**Editores(as) Convidados(as)**": [ /* *Lista de editores(as) convidados(as)* */
        {
            "**Nome**": "string", /* *Nome do(a) editor(a) convidado(a)* */
            "**Genero**": "string" /* *Gênero do(a) editor(a) convidado(a)* */
        }
    ],
    "**Conselho Consultivo**": [ /* *Lista de membros do conselho consultivo* */
        {
            "**Nome**": "string", /* *Nome do membro* */
            "**Genero**": "string" /* *Gênero do membro* */
        }
    ],
    "**Secretários(as)**": [ /* *Lista de secretários(as)* */
        {
            "**Nome**": "string", /* *Nome do(a) secretário(a)* */
            "**Genero**": "string" /* *Gênero do(a) secretário(a)* */
        }
    ],
    "**Editoração Eletrônica/Capa**": "string", /* *Responsável pela editoração/capa* */
    "**Revisão**": "string", /* *Responsável pela revisão* */
    "**Pareceristas ad hoc**": [ /* *Lista de pareceristas* */
        {
            "**Nome**": "string", /* *Nome do(a) parecerista* */
            "**Genero**": "string" /* *Gênero do(a) parecerista* */
        }
    ],
    "**Artigos**": [ /* *Lista de artigos na edição* */
        {
            "**Titulo**": "string", /* *Título do artigo* */
            "**Subtitulo**": "string", /* *Subtítulo do artigo* */
            "**Autores(as)**": [ /* *Lista de autores(as)* */
                {
                    "**Nome**": "string", /* *Nome do(a) autor(a)* */
                    "**Afiliacao**": "string", /* *Afiliação do(a) autor(a)* */
                    "**Genero**": "string" /* *Gênero do(a) autor(a)* */
                }
            ],
            "**Palavras chave**": ["string"], /* *Lista de palavras-chave* */
            "**Resumo**": "string", /* *Resumo do artigo* */
            "**Data Publicacao**": "string", /* *Data de publicação* */
            "**Edicao**": "string", /* *Edição do artigo* */
            "**URL**": "string", /* *URL do artigo* */
            "**URL_PDF**": "string", /* *URL do PDF do artigo* */
            "**Referencias**": ["string"], /* *Lista de referências* */
            "**Autores Referencias**": [ /* *Lista de autores nas referências* */
                {
                    "**Nome**": "string", /* *Nome do autor(a) nas referências* */
                    "**Genero**": "string" /* *Gênero do autor(a) nas referências* */
                }
            ]
        }
    ]
}
```
