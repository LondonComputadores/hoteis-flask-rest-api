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
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}


class Hotel(Resource):
    """
        Classe com Construtor como atributos de classe que utiliza o reqparser
        para analisar as requisições e garantir que somente o que é necessário
        será aceito. 
    """
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str ,required=True, help="This field 'nome' cannot be Blank")
    argumentos.add_argument('estrelas', type=float, required=True, help="This field 'estrelas' cannot be Blank")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found!'}, 404

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": f"Hotel id {hotel_id} already exists."}, 400

        dados = Hotel.atributos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save the hotel.'}, 500
        return hotel.json(), 201

    def put(self, hotel_id):
        dados = Hotel.atributos.parse_args() 
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save the hotel.'}, 500
        return hotel.json(), 201

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An internal error ocurred trying to delete the hotel.'}, 500
            return {'message': 'Hotel deleted.'}
        return {'message': 'Hotel not found.'}, 404