# Criada arquivo utils.py para ser utilizado como (utilitários), onde realizamos o import de requests que instalamos
# no início. Importamos o randint que será utilizado para gerar ips dinamicos. Importamos o settings para buscar a API
# (chave) que está lá. Importamos a classe GeoIP2 e geoip2


import requests
from random import randint
from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.gis.geoip2 import geoip2

YELP_SEARCH_ENDPOINT = 'https://api.yelp.com/v3/businesses/search'  # Endereço da plataforma YELP que iremos utilizar


# para realizar as buscar utilizando nossos parametros


# Criando nossas funçoes
def yelp_search(keyword=None,
                location=None):  # Criada essa funçao busca no yelp keyword=Palavra chave e location=cidade
    headers = {"Authorization": "Bearer " + settings.YELP_API_KEY}  # Armazena o acesso a API(senha de acesso)

    if keyword and location:  # Se a chave e a localizacao forem passadas
        params = {'term': keyword, 'location': location}  # variável = termo:chave, localizacao:localizacao
    else:  # Caso contrário
        params = {'term': 'Pizzaria', 'location': 'Belo Horizonte'}  # Setamos parametros default

    r = requests.get(YELP_SEARCH_ENDPOINT, headers=headers, params=params)  # Aqui setamos uma requisiçao no YELP_SEARCH
    # _ENDPOINT passando o header e os params
    return r.json()  # Retorno da requisicao(r) em formato .json


def get_client_data():  #
    g = GeoIP2()  # Através desse objetos encontraremos valores
    ip = get_random_ip()  # Variável recebendo a funçao que cria ips dinamicamente
    try:  # Tenta
        return g.city(ip)  # Recebemos um ip e tentamos retornar a cidade desse ip
    except geoip2.errors.AddressNotFoundError:  # Caso nao encontremos a cidade fornecida através do ip retornamos o
        # erro: AddressNotFoundError e None
        return None


def get_random_ip():
    return '.'.join([str(randint(0, 255)) for x in range(4)])
# Retornamos uma string (número ip) com numero randomicos de (0 a 255) sendo (4) grupos separados por '.'
