import os
import pandas as pd

def process_txt_files(year, folder):
    carga_path = os.path.join(folder, f"{year}Carga.txt")
    atracacao_path = os.path.join(folder, f"{year}Atracacao.txt")
    
    if os.path.exists(carga_path) and os.path.exists(atracacao_path):
        df_carga = pd.read_csv(carga_path, delimiter=";", decimal=',', low_memory=False)
        df_atracacao = pd.read_csv(atracacao_path, delimiter=";", decimal=',', low_memory=False)
        
        df_carga_filtrado = df_carga[df_carga['CDMercadoria'] == '1201']
        carga_data = df_carga_filtrado[['IDAtracacao', 'VLPesoCargaBruta', 'Origem']]

        # Filtragem e cruzamento
        df_atracacao_filtrado = df_atracacao[['IDAtracacao', 'IDBerco']]
        df_merged = pd.merge(carga_data, df_atracacao_filtrado, on='IDAtracacao', how='inner')
        
        # Agrupamento e cálculo das métricas
        ranking = (df_merged.groupby('Origem')
                   .agg(VLPesoCargaBruta_Total=('VLPesoCargaBruta', 'sum'),
                        IDBerco_Qtd=('IDBerco', 'nunique'),
                        Atracacao_Qtd=('IDAtracacao', 'count'))
                   .reset_index()
                   .sort_values(by='VLPesoCargaBruta_Total', ascending=False))
        
        print("Ranking de Origens:")
        print(ranking)


        script_dir = os.path.dirname(os.path.abspath(__file__))
        ranking_csv_path = os.path.join(script_dir, f"Rank de {year}.csv")
        
        ranking.to_csv(ranking_csv_path, index=False, sep=';', encoding='utf-8-sig')
        print(f"Ranking salvo em: {ranking_csv_path}")
        
        # Retornar o ranking
        return ranking