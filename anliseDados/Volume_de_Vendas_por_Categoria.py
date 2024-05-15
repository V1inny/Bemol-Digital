import pandas as pd
import matplotlib.pyplot as plt

# Extração dos dados
order_items = pd.read_csv('dados/olist_order_items_dataset.csv')
products = pd.read_csv('dados/olist_products_dataset.csv')
product_category_translation = pd.read_csv('dados/product_category_name_translation.csv')
orders = pd.read_csv('dados/olist_orders_dataset.csv')

# Transformação dos dados
# Mesclar os dados dos itens de pedido, produtos e tradução de categoria de produto
merged_data = pd.merge(order_items, products, on='product_id')
merged_data = pd.merge(merged_data, product_category_translation, on='product_category_name')

# Mesclar os dados do pedido para obter a data de compra
merged_data = pd.merge(merged_data, orders[['order_id', 'order_purchase_timestamp']], on='order_id')

# Converter a coluna de data para o tipo datetime
merged_data['order_purchase_timestamp'] = pd.to_datetime(merged_data['order_purchase_timestamp'])

# Agrupar por categoria de produto e mês, calcular o volume de vendas mensalmente
monthly_sales_by_category = merged_data.groupby([merged_data['order_purchase_timestamp'].dt.to_period('M'), 'product_category_name_english']).size().unstack(fill_value=0)

# Encontrar a categoria com maior e menor volume total de vendas
total_sales_by_category = monthly_sales_by_category.sum().sort_values(ascending=False)
top_category = total_sales_by_category.idxmax()
bottom_category = total_sales_by_category.idxmin()

# Filtrar os dados para a categoria com maior volume de vendas
monthly_sales_top_category = monthly_sales_by_category[top_category]

# Filtrar os dados para a categoria com menor volume de vendas
monthly_sales_bottom_category = monthly_sales_by_category[bottom_category]

# Visualização de dados mensais para a categoria que mais vendeu
plt.figure(figsize=(14, 6))
plt.bar(monthly_sales_top_category.index.astype(str), monthly_sales_top_category, color='skyblue', label=top_category)
plt.xlabel('Mês')
plt.ylabel('Volume de Vendas')
plt.title(f'Volume de Vendas Mensal para a Categoria: {top_category}')
plt.xticks(rotation=45)
plt.legend()
plt.show()

# Visualização de dados mensais para a categoria que menos vendeu
plt.figure(figsize=(14, 6))
plt.bar(monthly_sales_bottom_category.index.astype(str), monthly_sales_bottom_category, color='lightcoral', label=bottom_category)
plt.xlabel('Mês')
plt.ylabel('Volume de Vendas')
plt.title(f'Volume de Vendas Mensal para a Categoria: {bottom_category}')
plt.xticks(rotation=45)
plt.legend()
plt.show()

# Agrupar por categoria de produto e trimestre, calcular o volume de vendas trimestralmente
quarterly_sales_by_category = merged_data.groupby([merged_data['order_purchase_timestamp'].dt.to_period('Q'), 'product_category_name_english']).size().unstack(fill_value=0)

# Filtrar os dados para a categoria com maior volume de vendas
quarterly_sales_top_category = quarterly_sales_by_category[top_category]

# Visualização de dados trimestrais para a categoria que mais vendeu
plt.figure(figsize=(14, 6))
plt.bar(quarterly_sales_top_category.index.astype(str), quarterly_sales_top_category, color='skyblue', label=top_category)
plt.xlabel('Trimestre')
plt.ylabel('Volume de Vendas')
plt.title(f'Volume de Vendas Trimestral para a Categoria: {top_category}')
plt.xticks(rotation=45)
plt.legend()
plt.show()

# Filtrar os dados para a categoria com menor volume de vendas
quarterly_sales_bottom_category = quarterly_sales_by_category[bottom_category]

# Visualização de dados trimestrais para a categoria que menos vendeu
plt.figure(figsize=(14, 6))
plt.bar(quarterly_sales_bottom_category.index.astype(str), quarterly_sales_bottom_category, color='lightcoral', label=bottom_category)
plt.xlabel('Trimestre')
plt.ylabel('Volume de Vendas')
plt.title(f'Volume de Vendas Trimestral para a Categoria: {bottom_category}')
plt.xticks(rotation=45)
plt.legend()
plt.show()
