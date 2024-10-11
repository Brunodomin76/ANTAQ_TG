import os
import zipfile
import requests
from datetime import datetime
from data_processing import process_txt_files

def download_file(url, save_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()  
    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def extract_txt_from_zip(zip_path, extract_to_folder):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.endswith('.txt'):
                zip_ref.extract(file, extract_to_folder)
                print(f"Arquivo TXT extraído: {file}")


def get_year_from_user():
    current_year = datetime.now().year
    print("Selecione um ano entre 2010 e o ano atual:")
    for year in range(2010, current_year + 1):
        print(f"{year}")

    while True:
        try:
            selected_year = int(input("Digite o ano selecionado: "))
            if 2010 <= selected_year <= current_year:
                return selected_year
            else:
                print(f"Por favor, selecione um ano entre 2010 e {current_year}.")
        except ValueError:
            print("Por favor, insira um número válido.")


def main():
    selected_year = get_year_from_user()
    current_year = datetime.now().year
    
    temp_folder = 'tmp'
    os.makedirs(temp_folder, exist_ok=True)

    urls = [
        f"https://web3.antaq.gov.br/ea/txt/{selected_year}Carga.zip",
        f"https://web3.antaq.gov.br/ea/txt/{selected_year}Atracacao.zip"
    ]
    

    carga_file_path = os.path.join(temp_folder, f"{selected_year}Carga.txt")
    atracacao_file_path = os.path.join(temp_folder, f"{selected_year}Atracacao.txt")
    
    files_exist = os.path.exists(carga_file_path) and os.path.exists(atracacao_file_path)
    
    if files_exist and selected_year != current_year:
        print("Arquivos TXT já existem e não são do ano atual. Usando arquivos existentes.")
    else:
        for i, url in enumerate(urls, start=1):
            zip_path = os.path.join(temp_folder, f"file{i}.zip")
            
            print(f"Baixando {url} para {zip_path}...")
            download_file(url, zip_path)
            
            print(f"Extraindo arquivos TXT de {zip_path}...")
            extract_txt_from_zip(zip_path, temp_folder)
            
            print(f"Removendo {zip_path}...")
            os.remove(zip_path)
    
    process_txt_files(selected_year, temp_folder)

if __name__ == "__main__":
    main()
