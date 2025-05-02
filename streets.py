import pymysql
import json
import requests
import os
import concurrent.futures
import time
from typing import List
from configuration.config import DB_HOST, DB_USER, DB_PASS, DB_NAME

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def getStates() -> List[dict]:
    result = []
    sql = "SELECT id, abbreviation FROM state"
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = list(cursor.fetchall())
    return result

def getCities(stateId:int) -> List[dict]:
    result = []
    sql = "SELECT id, ibge_id, name, state_id FROM city WHERE state_id = %s"
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(sql, (stateId,))
        result = list(cursor.fetchall())
    return result

def formatName(feature: dict) -> str:
    if (not 'NM_TIP_LOG' in feature) and (not 'NM_TIT_LOG' in feature) and (not 'NM_LOG' in feature):
        return None
    nameParts = [feature['NM_TIT_LOG'], feature['NM_LOG']]
    streetName = " ".join(list(filter(lambda nm: nm != None, nameParts)))
    return streetName

def getCompleteAddress(uf:str, cityName:str, streetName:str, count=0) -> List[dict]:
    url = f"https://viacep.com.br/ws/{uf}/{cityName}/{streetName}/json/"
    status = None
    completeAddress = None
    while status != 200:
        data = requests.get(url, timeout=60)
        print(url, data.status_code)
        if count == 15 or data.status_code != 200:
            wait = 60
            print(f'AGUARDANDO {wait} SEG...')
            time.sleep(wait)
            print(f'RECOMECANDO')
        else:
            completeAddress = data.json()
            break
    return completeAddress

def getStreetFromJson(fileName: str) -> List[dict]:
    with open(fileName, 'r') as jsonFile:
        data = json.load(jsonFile)
        features = data['features']
        streets = [formatName(feature['properties']) for feature in features]
        return list(set(filter(lambda s: s!= None, streets)))

def saveDistricts(cityId: int, districtNames: list) -> List[dict]:
    if not districtNames:
        return []
    
    sql_select = f"SELECT name FROM district WHERE city_id = %s AND name IN ({', '.join(['%s'] * len(districtNames))})"
    connection = get_connection()
    params = [cityId] + districtNames
    with connection.cursor() as cursor:
        cursor.execute(sql_select, params)
        existing = set(row['name'] for row in cursor.fetchall())
        new_districts = [name for name in districtNames if name not in existing]
        if not new_districts:
            return []
        sql_insert = "INSERT INTO district (name, city_id) VALUES (%s, %s)"
        data = [(name, cityId) for name in new_districts]
        cursor.executemany(sql_insert, data)
        connection.commit()

        sql = "SELECT id, name FROM district WHERE city_id = %s"
        cursor.execute(sql, (cityId,))
        return list(cursor.fetchall())

def saveStreets(districtId: int, streetNames: list) -> List[dict]:
    if not streetNames:
        return []

    sql_select = f"SELECT name FROM street WHERE district_id = %s AND name IN ({', '.join(['%s'] * len(streetNames))})"
    connection = get_connection()
    params = [districtId] + streetNames

    with connection.cursor() as cursor:
        cursor.execute(sql_select, params)
        existing = set(row['name'] for row in cursor.fetchall())
        new_streets = [name for name in streetNames if name not in existing]
        if not new_streets:
            return []
        sql_insert = "INSERT INTO street (name, district_id) VALUES (%s, %s)"
        data = [(name, districtId) for name in new_streets]
        cursor.executemany(sql_insert, data)
        connection.commit()

        sql = "SELECT id, name FROM street WHERE district_id = %s"
        cursor.execute(sql, (districtId,))
        return list(cursor.fetchall())

def handleSaveStreets(addressList:list) -> None:
    if len(addressList) == 0:
        return
    districts = list(set([addrs['district'] for addrs in addressList]))
    cityId = addressList[0]['cityId']
    print("SALVANDO DADOS DA CIDADE: " + cityId)
    savedDistricts = saveDistricts(cityId, districts)
    for savedDistrict in savedDistricts:
        districtId = savedDistrict['id']
        streets = list(
            map(lambda addrs: addrs['street'], filter(lambda addrs: addrs['district'] == savedDistrict['name']))
        )
        saveStreets(districtId, streets)
    print("BAIRROS E RUAS DA CIDADE " + cityId + " SALVOS COM SUCESSO")

def handleStreets(state:dict, city:dict, streets:list) -> List[dict]:
    citiesData = []
    count = 0
    for street in streets:
        completeAddressList = getCompleteAddress(state['abbreviation'], city['name'], street, count)
        citiesData += list(map(lambda addrs: {
            'stateId': state['id'], 
            'cityId': city['id'], 
            'street': street, 
            'district': addrs['bairro']
        }, completeAddressList))
        count += 1
    return handleSaveStreets(citiesData)

def cityProcess(state: dict) -> None:
    cities = getCities(state['id'])
    for city in cities:
        fileName = f"./streets_json/{state['abbreviation']}/{city['ibge_id']}_faces_de_logradouros_2022.json"
        streets = getStreetFromJson(fileName)
        handleStreets(state, city, streets)

def statesProcess(statesList: list) -> None:
    for state in statesList:
        print('INICIANDO PROCESSO EM ' + state['abbreviation'])
        cityProcess(state)
        print('PROCESSO ' + state['abbreviation'] + 'FINALIZADO')

def getDistricutedStates(states:list) -> List[List[dict]]:
    ufMatrix = [
        ["SP", "AM", "RO"],                    
        ["MG"],                                
        ["RS", "GO", "DF", "RR", "AP"],        
        ["BA", "SC", "AC", "ES"],              
        ["PR", "PE", "MA", "PA", "CE"],        
    ]
    distributedStates = []
    for ufList in ufMatrix:
        distributedStates.append([state for state in states if state['abbreviation'] in ufList])
    return distributedStates

if __name__ == '__main__':
    states = getStates()
    distributedStates = getDistricutedStates(states)
    numThreads = len(distributedStates)
    with concurrent.futures.ThreadPoolExecutor(max_workers=numThreads) as executor:
        resultados = list(executor.map(statesProcess, distributedStates))