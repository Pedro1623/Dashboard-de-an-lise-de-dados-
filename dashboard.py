import pandas as pd # pd e o apelido padrao
import matplotlib.pyplot as plt # plt e o apelido padrao

def contar_presença(linha):
    return (linha.astype(str).str.upper() == "P").sum() # O (linha == "P") compara e gera True/False, e o .sum() já entra em seguida somando esse resultado

def contar_faltas(linha):
    return (linha.astype(str).str.upper() == "F").sum() # O (linha == "P") compara e gera True/False, e o .sum() já entra em seguida somando esse resultado

def dias_sem_aula(linha):
    return (linha.astype(str).str.upper() == "X").sum() # O (linha == "X") compara e gera True/False, e o .sum() já entra em seguida somando esse resultado

# ler o arquivo Excel
df = pd.read_csv(r"Arquivo excel", encoding = "utf-8", sep = ";", skiprows = 4) # O "r" faz o Python ignorar as barras invertidas do caminho do Windows
df = df.rename(columns = {"Unnamed: 1": "Nome"})
df = df.dropna(subset = ["Nome"]) # remove só as linhas onde a coluna Nome está vazia

meses = ["jan", "fev", "mar", "abr", "mai", "jun",
         "jul", "ago", "set", "out", "nov", "dez"]

for mes in meses:
    colunas_mes = df.columns[df.columns.str.endswith(f"{mes}")]
    df[f"Faltas_{mes}"] = df[colunas_mes].apply(contar_faltas, axis=1)

colunas = df.columns[2:] # Salvar só as colunas de datas

totais = {}

for mes in meses:
    totais[mes] = df[f"Faltas_{mes}"].sum() # Determina o mês que teve mais faltas

print(totais)

df["Presença"] = df[colunas].apply(contar_presença, axis = 1) # (axis = 1 significa 'por linha' ou 'por coluna')

df["Falta"] = df[colunas].apply(contar_faltas, axis = 1) # (axis = 1 significa 'por linha' ou 'por coluna')

df["Sem aula"] = df[colunas].apply(dias_sem_aula, axis = 1) # (axis = 1 significa 'por linha' ou 'por coluna')

total_de_aulas = df["Presença"] + df["Falta"]
df["percentual"] = (df["Presença"] / total_de_aulas) * 100

# print(df[["Presença", "futuros", "Sem aula"]].to_string())

mes_mais_faltas = max(totais, key=totais.get)
print("Mês com mais faltas:", mes_mais_faltas)
print("Total de faltas:", totais[mes_mais_faltas])

# Personalizar cada cor individualmente

cores = ["#003399", "#FFCC00", "#CC0000"]

plt.barh(df["Nome"], df["percentual"], color = cores[0]) # Cria uma barra com o percentual de presença e o nome do aluno

plt.title("percentual do aluno") # O título

for nome, valor in zip(df["Nome"], df["percentual"]):
    plt.text(valor, nome, f"{valor:.1f}%") # zip junta duas listas e percorre as duas ao mesmo tempo, par a par.

plt.show()

plt.barh(totais.keys(), totais.values(), color = cores[2])  # Cria uma barra com o percentual de presença e o nome do aluno

plt.title("Total de faltas")

plt.show()

# Criando gráfico de pizza usando looping, um gráfico para cada aluno