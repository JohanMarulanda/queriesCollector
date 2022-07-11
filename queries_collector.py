import requests
import logging
import json
import sys
import pandas as pd


URL = "https://api.lumu.io"
LUMU_CLIENT_KEY = "d39a0f19-7278-4a64-a255-b7646d1ace80"
COLLECTOR_ID = "5ab55d08-ae72-4017-a41c-d9d735360288"

Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(filename = "errors.log",
                    filemode = "w",
                    format = Log_Format, 
                    level = logging.ERROR)

logger = logging.getLogger()

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
        logger.ERROR("ERROR: Response Failed, check " + str(e))
    return response.status_code


def getDataFile(file):
    #Variales usadas para almacenar las queries a enviar y el numero de lineas leidas
    data_file = []
    total_lines = 0
    #Extraigo la data y cierro automaticamente el archivo
    with open(file, "r") as archivo:
        for linea in archivo:
            l = linea.split(' ')
            date = l[0]
            name = l[9]
            ip = l[6].split('#')[0]
            name = l[5].split('@')[1]
            
            data = {
                "timestamp": date,
                "name": name,
                "client_ip": ip,
                "client_name": name,
                "type": l[11]
            }
            data_file.append(data)
            total_lines = total_lines + 1
        print("ESTA ES LA DATA QUE VOY A RETORNAR")
        print(data_file)
        print(total_lines)
        return data_file, total_lines


if __name__ == "__main__":
    args = sys.argv[1:]
    total_queries, total_lines = getDataFile(args[0])

    if total_queries and total_lines>=5:
        requestDNSQueries(total_queries)
    else:
        logger.error("El archivo esta vacio!")




   


