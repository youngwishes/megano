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
        elif key == 'name':
            if value:
                cleaned_data['get_names'] = {'name': value}
        else:
            cleaned_data[key] = {key: True}

    return cleaned_data
