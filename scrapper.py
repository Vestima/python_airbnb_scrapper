import pyairbnb
import json

import re

url = "https://www.airbnb.com.br/rooms/1237002517062243971?source_impression_id=p3_1744229201_P3PvElFs4XXB45f3&check_in=2025-04-11&guests=2&adults=2&check_out=2025-04-14"
url2 = "https://www.airbnb.com.br/rooms/1237002517062243971?source_impression_id=p3_1744229201_P3PvElFs4XXB45f3"

PATTERN = r'^(https:\/\/www\.airbnb\.com\.br\/rooms\/\d+)(?:.*?check_in=([\d]{4}-[\d]{2}-[\d]{2}))?(?:.*?check_out=([\d]{4}-[\d]{2}-[\d]{2}))?'

def get_data_from_url(url):
    match = re.search(PATTERN, url)
    if match:
        room_url = match.group(1)
        check_in = match.group(2)
        check_out = match.group(3)
    else:
        raise Exception("URL INVALIDO")

    try:
        proxy_url = ""  
        data, price_input, cookies = pyairbnb.get_metadata_from_url(room_url, proxy_url)
        product_id = price_input["product_id"]
        api_key = price_input["api_key"]
        currency = "BRL"

        price = pyairbnb.get_price(product_id, price_input["impression_id"], api_key, currency, cookies,
                    check_in, check_out, proxy_url)

        price_value = 'NaN'
        try:
            price_value = price['main']['discountedPrice']
        except Exception as e:
            pass
    
        try:
            price_value = price['details']['Total before taxes']
        except Exception as e:
            pass
        price_value = price_value if price_value else 'NaN'

        return {
            'title': data['sub_description']['title'],
            'price' :  price_value,
            'images' : data['images'][:2],
            'rating' : data['rating']
        }
    except Exception as e:
        raise Exception(f'ERRO NO SCRAPPER: {e}')

