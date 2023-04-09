import mercadopago
sdk = mercadopago.SDK("TEST-4368628010042942-091321-1562c33b6967e86a81c960dfe9b260f8-1165943682")
from random import choice


def Create_payment():
    preference_data = {
        "items": [
            {
                "title": "Assinatura +1 mes bot-sala",
                "quantity": 1,
                'id': str([choice('w s x 0 i d o - = ! 8 2 0 8 d x - = ! d j d a f 0 9 2 7 3 = - y e x ! d m s *'.split(' ')) for x in range(20)]),
                "unit_price": 49.90
            }
        ]
    }


    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]

    preference_id = preference['id']
    collector_id = preference['collector_id']
    print(preference)



'''p_r = sdk.preference().get('1165943682-24303b91-2888-4c3b-863d-3a3a2442c0e8')
print(p_r['response'])'''



def get_peyment(collector_id):
    result = sdk.payment().search()
    result = result['response']['results']
    for c in result:
        if c['additional_info']['items'][0]['id'] == collector_id:
            return c['status'] == 'approved'

# get_peyment(1165943682)

from datetime import datetime, timedelta

a = datetime.now()

b = datetime.strptime('2022-09-30'.replace('-', ' '), '%Y %m %d')

print(a - b)