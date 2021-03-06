import requests
import logging
import json
import sys
import datetime as datetime
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
    #Cada 500 lineas leidas, se debe enviar la data
    data_chunk = []
    counter = 0
    success = 0
    failed = 0
    #Extraigo la data y cierro automaticamente el archivo
    with open(file, "r") as archivo:
        for linea in archivo:
            l = linea.split(' ')
            date = datetime.datetime.strptime(l[0], "%d-%b-%Y")
            hour = l[1] + 'Z'
            date = date.strftime('%Y-%m-%d') + 'T' + hour
            name = l[9]
            client_ip = l[6].split('#')[0]
            client_name = l[5].split('@')[1]
            
            data = {
                "timestamp": date,
                "name": name,
                "client_ip": client_ip,
                "client_name": client_name,
                "type": l[11]
            }
            data_chunk.append(data)
            counter = counter + 1
            data_file.append(data)
            if counter == 500:
                status = requestDNSQueries(data_chunk)
                if status == 200:
                    success = success + 1
                else:
                    failed = failed + 1
                total_lines += counter
                data_chunk = []
                counter = 0
        return data_file, total_lines, success, failed


if __name__ == "__main__":
    args = sys.argv[1:]
    total_queries, total_lines, success, failed = getDataFile(args[0])

    if total_queries:
        df = pd.DataFrame(total_queries, columns=["timestamp","name","client_ip","client_name", "type"])
        
        ips = df.groupby('client_ip', as_index=False).aggregate(Suma=('client_ip', 'count'))
        ips['porcentaje'] = ips['Suma'] * 100 / total_lines
        ips = ips.sort_values('Suma', ascending=False)

        host = df.groupby('name', as_index=False).aggregate(Suma=('name', 'count'))
        host['porcentaje'] = host['Suma'] * 100 / total_lines
        host = host.sort_values('Suma', ascending=False)

        print('Total Records: ' + str(total_lines))
        print('')
        print('Client IPs Rank')
        print('------------------- ----- -----')
        print(ips.head(5))
        print('------------------- ----- -----')
        print('')
        print('')
        print('Host Rank')
        print('------------------------------------------------------------')
        print(host.head(5))
        print('------------------------------------------------------------')
    
    else:
        logger.error("El archivo esta vacio o no tiene la cantidad de queries necesaria.")
    