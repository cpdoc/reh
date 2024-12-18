import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

bd_autores_genero_ano = pd.DataFrame()

for edicao in edicoes_reh:
    for artigo in edicao['Artigos']:
        for autor in artigo['Autores Referencias']:
            bd_autores_genero_ano = bd_autores_genero_ano._append({'Ano':edicao['Ano'],
                                                                   'Autor':autor['Nome'],
                                                                   'Genero':autor['Genero']},
                                                                   ignore_index=True)

dados_agrupados = bd_autores_genero_ano.groupby(["Ano", "Genero"]).size().reset_index(name="Quantidade")

# Plotando o gráfico
plt.figure(figsize=(10, 6))
sns.lineplot(
    data=dados_agrupados,
    x="Ano",
    y="Quantidade",
    hue="Genero",
    marker="o"
)
plt.title("Distribuição dos Gêneros ao Longo do Tempo", fontsize=16)
plt.xlabel("Ano", fontsize=12)
plt.ylabel("Quantidade", fontsize=12)
plt.legend(title="Gênero")
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()
