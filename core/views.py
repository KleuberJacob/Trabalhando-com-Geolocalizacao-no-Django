from django.shortcuts import render
from django.views.generic import View

from .utils import yelp_search, get_client_data


class IndexView(View):

    def get(self, request, *args, **kwargs):
        items = []  # Criada uma lista que receberá nossos dados

        city = None

        while not city:  # Enquanto nao houver cidade
            ret = get_client_data()  # Iremos buscar os dados do cliente utilizando a funcao criada que recebe um IP
            # e retorna uma cidade
            if ret:  # Se houver cidade(city/ret), pois caso o ip seja inválido pode ser retornado None
                city = ret['city']  # Armazenando dentro da variável city o retorno de ret como [city]

        q = request.GET.get('key', None)  # Se (key=keywords=Palavra Chave) nao for passado nada o default é None
        # (Porém é obrigatório passar já que a city já virá por padrao ou seja nunca será None)
        loc = request.GET.get('loc', None)  # Se (loc=localidade) nao for passado nada o default é None
        location = city  # Passo a localidade como a cidade descoberta pelo IP ou passada pelo usuário em loc

        context = {  # Criada variável de contexto(dados que serao apresentados), onde especificamos que
            'city': city,  # cidade é a cidade que descobrimos acima seja passada pelo usuário ou através do IP descober
            'busca': False,  # Usuário realizou busca? Nao=Falso
        }

        if loc:  # Se o usuario infomou uma localidade(loc) ou seja nao veio vazia, entao ela passa a ser utilizada
            location = loc
        if q:  # Se a query(q=busca) for passada ou seja os parametros da funcao (keyword, location) foram
            # passados corretamente
            items = yelp_search(keyword=q, location=location)  # Items(lista) vai receber na funcao de busca yelp_search
            # os parametros passados
            context = {  # O contexto apresentará os dados abaixo
                'items': items,
                'city': location,
                'busca': True,  # Usuário realizou busca? Sim=True, pois os parametros foram passados corretamente
            }
        return render(request, 'index.html', context)  # Retornamos o renderizaçao(requisicao, pagina'index',
        # apresentando os dados fornecidos pelo contexto
