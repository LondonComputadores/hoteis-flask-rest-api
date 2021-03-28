from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hoteis = [
    {
        'hotel_id': 'alpha',
        'nome': 'Alpha Hotel',
        'estrelas': 4.3,
        'diaria': 420.34,
        'cidade': 'Rio de Janeiro'
    },
    {
        'hotel_id': 'bravo',
        'nome': 'Bravo Hotel',
        'estrelas': 3.7,
        'diaria': 380.34,
        'cidade': 'Florianopolis'
    },
    {
        'hotel_id': 'espelunca',
        'nome': 'Espelunca Hotel',
        'estrelas': 2.5,
        'diaria': 120.34,
        'cidade': 'Sao Paulo'
    },
]

class Hoteis(Resource):
    def get(self):
        return {'hoteis': hoteis}


class Hotel(Resource):
    """
        Classe com Construtor como atributos de classe que utiliza o reqparser
        para analisar as requisições e garantir que somente o que é necessário
        será aceito. 
    """
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None

    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel
        return {'message': 'Hotel not found!'}, 404

    def post(self, hotel_id):

        # dados = Hotel.argumentos.parse_args()
        # novo_hotel = {
        #     'hotel_id': hotel_id,
        #     'nome': dados['nome'],
        #     'estrelas': dados['estrelas'],
        #     'diaria': dados['diaria'],
        #     'cidade': dados['cidade']
        # } All of this code here refactored become only this:
        # novo_hotel = { 'hotel_id': hotel_id, **dados }

        # bloco de refatoração que substitui o bloco acima comentado
        dados = Hotel.atributos.parse_args()
        hotel_objeto = HotelModel(hotel_id, **dados)
        novo_hotel = hotel_objeto.json()

        # continuação de ambos ou qualquer um dos blocos acima na classe post
        hoteis.append(novo_hotel)
        return novo_hotel, 201

    def put(self, hotel_id):
        dados = Hotel.atributos.parse_args()
        # novo_hotel = { 'hotel_id': hotel_id, **dados } #substituído por...:
        hotel_objeto = HotelModel(hotel_id, **dados)     #...essa e...
        novo_hotel = hotel_objeto.json()                 #...essa linha tbm como no post 
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            hotel.update(novo_hotel)
            return novo_hotel, 200
        hoteis.append(novo_hotel)
        return novo_hotel, 201  #201 == created/criado com sucesso

    def delete(self, hotel_id):
        """
            Usar global para que o python não confunda a variável hotel abaixo
            com o list comprehend como uma nova variável e não a já existente.
        """
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return {'message': 'Hotel deleted.'}