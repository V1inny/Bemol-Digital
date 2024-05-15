import pandas as pd
import matplotlib.pyplot as plt

# Leitura dos dados
order_reviews = pd.read_csv('dados/olist_order_reviews_dataset.csv')
order_items = pd.read_csv('dados/olist_order_items_dataset.csv')
products = pd.read_csv('dados/olist_products_dataset.csv')

# Mesclando os dados usando 'order_id' e 'product_id'
merged_data = pd.merge(order_reviews, order_items, on='order_id', how='inner')
merged_data = pd.merge(merged_data, products, on='product_id', how='left')

# Transformação dos dados
# Agrupar por 'product_category_name' e calcular a média das avaliações
media_avaliacoes_por_categoria = merged_data.groupby('product_category_name')['review_score'].mean().reset_index()

# Selecionar os 5 produtos com melhores avaliações por categoria
melhores_produtos_por_categoria = media_avaliacoes_por_categoria.nlargest(5, 'review_score')

# Selecionar os 5 produtos com piores avaliações por categoria
piores_produtos_por_categoria = media_avaliacoes_por_categoria.nsmallest(5, 'review_score')

# Visualização de dados
plt.figure(figsize=(10, 6))

# Plot dos melhores produtos por categoria
bars_melhores = plt.barh(melhores_produtos_por_categoria['product_category_name'], melhores_produtos_por_categoria['review_score'], color='green', label='Melhores Avaliações')

# Adicionando os valores das avaliações nos gráficos
for bar in bars_melhores:
    plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, f'{bar.get_width():.2f}', ha='left', va='center', color='black')

# Plot dos piores produtos por categoria
bars_piores = plt.barh(piores_produtos_por_categoria['product_category_name'], piores_produtos_por_categoria['review_score'], color='red', label='Piores Avaliações')

# Adicionando os valores das avaliações nos gráficos
for bar in bars_piores:
    plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, f'{bar.get_width():.2f}', ha='left', va='center', color='black')

plt.xlabel('Avaliação Média')
plt.ylabel('Categoria de Produto')
plt.title('Melhores e Piores Avaliações de Produtos por Categoria')
plt.legend()
plt.gca().invert_yaxis()  # Inverte o eixo y para exibir as avaliações mais altas no topo
plt.show()
