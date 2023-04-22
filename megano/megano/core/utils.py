from django.core.cache import cache


def get_cleaned_data_from_post_data(post_data):
    """
    Названия ключей в очищенном словаре должны соответствовать названиям методам внутри класса ProductQuerySet
    Если поле имеет булевый тип, в качестве ключа необходимо присвоить название поля (key), в качестве значения
     - словарь вида { ключ: True }
    """
    cleaned_data = {}

    for key, value in post_data.items():
        if key == 'price':
            from_price, to_price = value.split(';')
            cleaned_data['price_range'] = {'price_from': int(from_price), 'price_to': int(to_price)}
            cache.set('price_from', from_price, 5)
            cache.set('price_to', to_price, 5)
        elif key == 'name':
            if value:
                cleaned_data['get_names'] = {'name': value}
            cache.set('name', value)
        else:
            cleaned_data[key] = {key: True}
            cache.set(key, value, 5)

    if not cleaned_data.get('in_stock'):
        cache.delete('in_stock')

    return cleaned_data
