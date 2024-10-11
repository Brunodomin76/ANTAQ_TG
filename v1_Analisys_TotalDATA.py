import pandas as pd
import numpy as np
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#diretórios com dados de entrada
ANTAQ = "C:/Users/Usuário/Desktop/"
ANO = "2015"

#abre o arquivo de atracação
file1 = ANTAQ+ANO+'atracacao.csv'
df1 = pd.read_csv(file1, low_memory=False, sep=';', encoding= 'UTF-8', decimal= ",")

#checagem de estrutura dos dados
df1.info()

#visualização dos dados
df1.head(3)
df1 = df1.dropna(subset=['Data Atracação', 'Data Chegada', 'Data Desatracação', 'Data Início Operação', 'Data Término Operação'])

#define formato de tempo para as datas de operação
df1["Data Chegada"] = pd.to_datetime(df1['Data Chegada'], format='%d/%m/%Y %H:%M:%S')
df1["Data Atracação"] = pd.to_datetime(df1['Data Atracação'], format='%d/%m/%Y %H:%M:%S')
df1["Data Início Operação"] = pd.to_datetime(df1['Data Início Operação'], format='%d/%m/%Y %H:%M:%S')
df1["Data Término Operação"] = pd.to_datetime(df1['Data Término Operação'], format='%d/%m/%Y %H:%M:%S')
df1["Data Desatracação"] = pd.to_datetime(df1['Data Desatracação'], format='%d/%m/%Y %H:%M:%S')

#calcula tempos do navio no porto (em horas)
df1['Espera_Atracação'] = (df1['Data Atracação'] - df1['Data Chegada']).dt.total_seconds() / 3600
df1['Espera_Operação'] = (df1['Data Início Operação'] - df1['Data Atracação']).dt.total_seconds() / 3600
df1['Operação'] = (df1['Data Término Operação'] - df1['Data Início Operação']).dt.total_seconds() / 3600
df1['Espera_Desatracação'] = (df1['Data Desatracação'] - df1['Data Término Operação']).dt.total_seconds() / 3600

#abre o arquivo de cargas
file2 = ANTAQ+ANO+'carga.csv'
df2 = pd.read_csv(file2, low_memory=False, sep=";", encoding= 'UTF-8', decimal= ',')

#checagem se existem valores duplicados para as alterçaões
duplicados = df2.duplicated(subset=['IDAtracacao'], keep=False)
if duplicados.any():
    print('Existem valores duplicados')
    print (df2[duplicados])
else:
    print("Coluna com valores únicos")

#remover caso duplicados
df2.drop(df2[duplicados].index, inplace=True)

#Integra as duas bases de dados
dados_antaq =pd.merge(df1,df2, left_on='IDAtracacao', right_on="IDAtracacao", how='inner')

#Calcula prancha operacional (t/h)
dados_antaq['t/h'] = dados_antaq['VLPesoCargaBruta'] / dados_antaq['Operação']

#escolhe colunas de interesse para o projeto

colunas_interesse = ['IDAtracacao', 'CDMercadoria', 'Complexo Portuário', 'Tipo de Navegação da Atracação', 'Espera_Atracação', 'Espera_Operação', 'Operação', 'Espera_Desatracação',
                     'Natureza da Carga', 'VLPesoCargaBruta', 't/h', 'Mes', 'Ano', 'STSH4', 'STSH2', 'Sentido', 'Terminal']

#salva df em csv
dados_antaq[colunas_interesse].to_csv(ANTAQ + ANO + 'ANTAQ.csv', sep=';', index=False, decimal=',', encoding='utf-8')
