import requests
import json

url = 'https://fakestoreapi.com/products/categories'
response = requests.get(url).json()
print(response)
flag = False
product_categoria = input("Выберите и введите категорию товара: ")

url1 = 'https://fakestoreapi.com/products'
response = requests.get(url1).json()

for item in response:
    if item['category'] == product_categoria:
        print(item)
        print(json.dumps(item, indent=4))
        #print(f'Номер: {item['id']} Наименование: {item['title']} Категория: {item['category']}')
        flag = True
        
if not flag:
    print(f'Такой категории товара нет')