import pandas as pd
import matplotlib.pyplot as plt

# Função para carregar os datasets
def carregar_dados():
    # Insira o caminho do arquivo CSV contendo os dados de vendas
    vendas_df = pd.read_csv("dados/olist_sellers_dataset.csv")

    # Retornar o DataFrame das vendas
    return vendas_df

# Função para realizar a análise de volume de vendas por categoria
def analise_volume_vendas_por_cidade(vendas_df):
    # Agrupar as vendas por cidade e contar o número de ocorrências
    volume_vendas_por_cidade = vendas_df['seller_state'].value_counts().reset_index()
    volume_vendas_por_cidade.columns = ['seller_state', 'seller_zip_code_prefix']

    # Ordenar as cidades por volume de vendas
    volume_vendas_por_cidade = volume_vendas_por_cidade.sort_values(by='seller_zip_code_prefix', ascending=False)

    # Plotar o gráfico de barras horizontais para visualizar o volume de vendas por cidade
    plt.figure(figsize=(10, 6))
    plt.barh(volume_vendas_por_cidade['seller_state'], volume_vendas_por_cidade['seller_zip_code_prefix'])
    plt.title('Volume de Vendas por Estado')
    plt.xlabel('Volume de Vendas')
    plt.ylabel('Estado')
    plt.tight_layout()
    plt.show()

# Função principal para executar o ETL e a análise exploratória
def main():
    # Extração dos dados
    vendas_df = carregar_dados()

    # Transformação e Análise de Volume de Vendas por Cidade
    analise_volume_vendas_por_cidade(vendas_df)

if __name__ == "__main__":
    main()
