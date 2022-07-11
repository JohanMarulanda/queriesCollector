import requests
import logging
import json

URL = "https://api.lumu.io"
LUMU_CLIENT_KEY = "d39a0f19-7278-4a64-a255-b7646d1ace80"
COLLECTOR_ID = "5ab55d08-ae72-4017-a41c-d9d735360288"

log = logging.getLogger('errors')

def requestDNSQueries(queries):
    url = URL + "/collectors/" + COLLECTOR_ID + "/dns/queries?key=" + LUMU_CLIENT_KEY
    headers = {'Content-Type': 'application/xml'}
    '''
    data = {
        "timestamp": "2021-01-06T14:37:02.228Z",
        "name": "www.example.com",
        "client_ip": "192.168.0.103",
        "client_name": "MACHINE-0987",
        "type": "A"
    }
    '''
    try:
        response = requests.post(url, headers=headers, data=json.dumps(queries))#data=json.dumps(data))
    except Exception as e:
        log.debug("DEBUG: Response Failed, check " + str(e))
    return response.status_code


if __name__ == "__main__":
    resultado = requestDNSQueries('jejeje')
    print("ESTE ES EL RESULTADOOO")
    print(resultado)