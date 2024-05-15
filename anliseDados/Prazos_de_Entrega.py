import pandas as pd
import matplotlib.pyplot as plt

# Leitura dos dados
orders = pd.read_csv('dados/olist_orders_dataset.csv')
order_items = pd.read_csv('dados/olist_order_items_dataset.csv')
products = pd.read_csv('dados/olist_products_dataset.csv')
customers = pd.read_csv('dados/olist_customers_dataset.csv')
sellers = pd.read_csv('dados/olist_sellers_dataset.csv')
category_translation = pd.read_csv('dados/product_category_name_translation.csv')

# Convertendo as colunas de data para o tipo datetime
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['order_approved_at'] = pd.to_datetime(orders['order_approved_at'])
orders['order_delivered_carrier_date'] = pd.to_datetime(orders['order_delivered_carrier_date'])
orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])

# Calculando o tempo de entrega em dias e atrasos
orders['delivery_time'] = (orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']).dt.days
orders['delay'] = (orders['order_delivered_customer_date'] - orders['order_estimated_delivery_date']).dt.days

# Tempo médio de entrega
mean_delivery_time = orders['delivery_time'].mean()
print(f"Tempo médio de entrega: {mean_delivery_time:.2f} dias")

# Analisando atrasos
delays = orders[orders['delay'] > 0]
mean_delay_time = delays['delay'].mean()
print(f"Tempo médio de atraso: {mean_delay_time:.2f} dias")

# Mesclando os dados
merged_data = pd.merge(order_items, orders, on='order_id')
merged_data = pd.merge(merged_data, products, on='product_id')
merged_data = pd.merge(merged_data, customers[['customer_id', 'customer_zip_code_prefix']], on='customer_id')
merged_data = pd.merge(merged_data, sellers[['seller_id', 'seller_zip_code_prefix']], on='seller_id')
merged_data = pd.merge(merged_data, category_translation, on='product_category_name', how='left')

# Contagem de atrasos por categoria de produto
product_delays = merged_data[merged_data['delay'] > 0].groupby('product_category_name_english')['delay'].count().reset_index()
product_delays.columns = ['product_category_name', 'delay_count']

# Visualização de dados
plt.figure(figsize=(14, 8))
plt.hist(orders['delivery_time'], bins=30, color='skyblue', edgecolor='black')
plt.axvline(mean_delivery_time, color='red', linestyle='dashed', linewidth=1)
plt.xlabel('Tempo de Entrega (dias)')
plt.ylabel('Frequência')
plt.title('Distribuição do Tempo de Entrega')
plt.show()

plt.figure(figsize=(14, 8))
plt.hist(delays['delay'], bins=30, color='lightcoral', edgecolor='black')
plt.axvline(mean_delay_time, color='blue', linestyle='dashed', linewidth=1)
plt.xlabel('Tempo de Atraso (dias)')
plt.ylabel('Frequência')
plt.title('Distribuição do Tempo de Atraso')
plt.show()

# Visualização dos atrasos por categoria de produto
plt.figure(figsize=(14, 8))
plt.bar(product_delays['product_category_name'], product_delays['delay_count'], color='orange', edgecolor='black')
plt.xlabel('Categoria de Produto')
plt.ylabel('Contagem de Atrasos')
plt.title('Atrasos por Categoria de Produto')
plt.xticks(rotation=45)
plt.show()
