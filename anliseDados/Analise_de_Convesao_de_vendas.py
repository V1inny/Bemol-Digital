import pandas as pd
import matplotlib.pyplot as plt

# Leitura dos dados
orders = pd.read_csv('dados/olist_orders_dataset.csv')
order_items = pd.read_csv('dados/olist_order_items_dataset.csv')
customers = pd.read_csv('dados/olist_customers_dataset.csv')

# Criando um dataset hipotético de marketing (substitua com dados reais quando disponível)
# Assumindo que cada cliente veio de uma fonte de tráfego específica
traffic_sources = ['organic', 'paid', 'social', 'email', 'referral']

# Adicionando uma coluna 'traffic_source' ao dataset de clientes
customers['traffic_source'] = [traffic_sources[i % len(traffic_sources)] for i in range(len(customers))]

# Mesclando os dados de pedidos com os dados de clientes
merged_data = pd.merge(orders, customers, on='customer_id')

# Calculando o número de pedidos por fonte de tráfego
orders_by_traffic_source = merged_data.groupby('traffic_source')['order_id'].nunique().reset_index()
orders_by_traffic_source.columns = ['traffic_source', 'order_count']

# Assumindo que temos um total de visitas por fonte de tráfego (dados fictícios)
visits_by_traffic_source = pd.DataFrame({
    'traffic_source': ['organic', 'paid', 'social', 'email', 'referral'],
    'visit_count': [10000, 8000, 5000, 2000, 3000]  # Exemplo de número de visitas por fonte de tráfego
})

# Mesclando os dados de visitas com os dados de pedidos
conversion_data = pd.merge(orders_by_traffic_source, visits_by_traffic_source, on='traffic_source')

# Calculando a taxa de conversão
conversion_data['conversion_rate'] = (conversion_data['order_count'] / conversion_data['visit_count']) * 100

# Visualização dos dados
plt.figure(figsize=(10, 6))
plt.bar(conversion_data['traffic_source'], conversion_data['conversion_rate'], color='skyblue')
for i, value in enumerate(conversion_data['conversion_rate']):
    plt.text(i, value + 0.5, f'{value:.2f}%', ha='center')
plt.xlabel('Fonte de Tráfego')
plt.ylabel('Taxa de Conversão (%)')
plt.title('Taxa de Conversão de Vendas por Fonte de Tráfego')
plt.show()
