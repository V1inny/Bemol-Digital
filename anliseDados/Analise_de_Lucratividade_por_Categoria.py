import pandas as pd
import matplotlib.pyplot as plt

# Leitura dos dados
products = pd.read_csv('dados/olist_products_dataset.csv')
order_items = pd.read_csv('dados/olist_order_items_dataset.csv')
order_payments = pd.read_csv('dados/olist_order_payments_dataset.csv')

# Mesclando os dados
merged_data = pd.merge(order_items, products, on='product_id')
merged_data = pd.merge(merged_data, order_payments, on='order_id')

# Considerando a receita total como o valor pago pelo cliente
merged_data['receita_total'] = merged_data.groupby('order_id')['payment_value'].transform('sum')

# Considerando o custo como o preço do produto (sem frete)
merged_data['custo'] = merged_data['price']

# Calculando o lucro como receita total menos custo e menos frete
merged_data['lucro'] = merged_data['receita_total'] - merged_data['custo'] - merged_data['freight_value']

# Calculando a lucratividade por categoria de produto
lucro_por_categoria = merged_data.groupby('product_category_name')['lucro'].sum()

# Visualização de dados
plt.figure(figsize=(14, 8))
bars = lucro_por_categoria.plot(kind='bar', color='skyblue')
plt.xlabel('Categoria de Produto')
plt.ylabel('Lucro')
plt.title('Lucratividade por Categoria de Produto')
plt.xticks(rotation=45)

# Adicionando os valores em cada coluna
for idx, value in enumerate(lucro_por_categoria):
    plt.text(idx, value, f'{value:.2f}', ha='center', va='bottom')

plt.show()
