import pandas as pd
import matplotlib.pyplot as plt

# Extração dos dados
customers = pd.read_csv('dados/olist_customers_dataset.csv')
geolocation = pd.read_csv('dados/olist_geolocation_dataset.csv')
order_items = pd.read_csv('dados/olist_order_items_dataset.csv')
order_payments = pd.read_csv('dados/olist_order_payments_dataset.csv')
order_reviews = pd.read_csv('dados/olist_order_reviews_dataset.csv')
orders = pd.read_csv('dados/olist_orders_dataset.csv')
products = pd.read_csv('dados/olist_products_dataset.csv')
sellers = pd.read_csv('dados/olist_sellers_dataset.csv')
product_category_translation = pd.read_csv('dados/product_category_name_translation.csv')

# Transformação dos dados
# Vamos juntar as tabelas orders, order_items e products para obter informações completas sobre os produtos vendidos
merged_orders = pd.merge(pd.merge(orders, order_items, on='order_id'), products, on='product_id')

# Agrupar por categoria de produto e calcular o volume de vendas
sales_by_category = merged_orders.groupby('product_category_name').size().reset_index(name='volume_de_vendas')

# Ordenar por volume de vendas descendente para destacar as categorias mais vendidas
sales_by_category = sales_by_category.sort_values(by='volume_de_vendas', ascending=False)

# Visualização de dados
# Criando uma lista de cores para cada categoria
cores = ['red', 'blue', 'green', 'orange', 'purple', 'yellow', 'cyan', 'magenta', 'lime', 'pink']

# Visualização de dados com cores personalizadas
plt.figure(figsize=(10, 6))
bars = plt.barh(sales_by_category['product_category_name'], sales_by_category['volume_de_vendas'], color=cores)

# Calculando e adicionando as porcentagens em relação ao total
total_vendas = sum(sales_by_category['volume_de_vendas'])
for bar in bars:
    yval = bar.get_width()
    porcentagem = (yval / total_vendas) * 100
    plt.text(yval, bar.get_y() + bar.get_height()/2, f'{porcentagem:.2f}%', va='center', ha='left', fontsize=10, color='black')

plt.xlabel('Volume de Vendas')
plt.ylabel('Categoria de Produto')
plt.title('Volume de Vendas por Categoria de Produto')
plt.gca().invert_yaxis()
plt.show()
