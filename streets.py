import pymysql
import json
import requests
import os
import time
from configuration.config import DB_HOST, DB_USER, DB_PASS, DB_NAME

connection = pymysql.connect(host=DB_HOST,
                             user=DB_USER,
                             password=DB_PASS,
                             database=DB_NAME,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def getStates():
    result = []
    sql = "SELECT id, abbreviation FROM state"
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = list(cursor.fetchall())
    return result

def getCities(stateId:int):
    result = []
    sql = "SELECT id, ibge_id, name, state_id FROM city WHERE state_id = %s"
    with connection.cursor() as cursor:
        cursor.execute(sql, (stateId,))
        result = list(cursor.fetchall())
    return result

def formatName(feature: dict):
    if (not 'NM_TIP_LOG' in feature) and (not 'NM_TIT_LOG' in feature) and (not 'NM_LOG' in feature):
        return None
    nameParts = [feature['NM_TIP_LOG'], feature['NM_TIT_LOG'], feature['NM_LOG']]
    streetName = " ".join(list(filter(lambda nm: nm != None, nameParts)))
    return streetName

def getDistrict(uf:str, cityName:str, streetName:str):
    url = f"https://viacep.com.br/ws/{uf}/{cityName}/{streetName}/json/"
    print(url)
    status = None
    district = None
    while status != 200:
        data = requests.get(url)
        district = data.json()
        status = data.status_code
        if status != 200:
            print('AGUARDANDO 10 SEG...')
            time.sleep(10)
    return district[0]['bairro']

def getStreetFromJson(fileName: str) -> list:
    with open(fileName, 'r') as jsonFile:
        data = json.load(jsonFile)
        features = data['features']
        streets = [formatName(feature['properties']) for feature in features]
        return list(filter(lambda s: s!= None, streets))

def saveDistricts(cityId: int, districtNames: list):
    if not districtNames:
        return []
    
    sql_select = f"SELECT name FROM district WHERE city_id = %s AND name IN ({', '.join(['%s'] * len(districtNames))})"
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

def saveStreets(districtId: int, streetNames: list):
    if not streetNames:
        return []

    sql_select = f"SELECT name FROM street WHERE district_id = %s AND name IN ({', '.join(['%s'] * len(streetNames))})"
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

def handleSave(cityId:int, currentCity: list):
    districts = list(filter(lambda add: add!='', set(map(lambda add: add['district'], currentCity))))
    districts = saveDistricts(cityId, districts)
    for district in districts:
        streets = list(filter(lambda add: add['district'] == district['name'], currentCity))
        streetNames = list(map(lambda add: add['street'], streets))
        saveStreets(district['id'], streetNames)

def saveReadData(stateId, cityId, fileName='readData.json'):
    dados = {
        "stateId": stateId,
        "cityId": cityId
    }

    try:
        if os.path.exists(fileName):
            with open(fileName, 'r', encoding='utf-8') as file:
                content = json.load(file)
                content.update(dados)
        else:
            content = dados
        with open(fileName, 'w', encoding='utf-8') as file:
            json.dump(content, file, ensure_ascii=False, indent=4)
        print(f"Arquivo '{fileName}' atualizado com sucesso.")

    except Exception as e:
        print(f"Ocorreu um erro ao salvar os IDs: {e}")

def readMemoryCard():
    pass

if __name__ == '__main__':
    currentStateId = None
    currentCityId = None
    states = getStates(currentStateId)
    currentCity = []
    for state in states:
        currentStateId = state['id']
        cities = getCities(state['id'])
        for city in cities:
            currentCityId = city['id']
            fileName = f"./streets_json/{state['abbreviation']}/{city['ibge_id']}_faces_de_logradouros_2022.json"
            streets = getStreetFromJson(fileName)
            group = [{'stateId': state['id'], 'cityId': city['id'], 'street': street, 'district': getDistrict(state['abbreviation'], city['name'], street)} for street in streets]
            currentCity.append(group)
        
        handleSave(currentCityId, currentCity)
        currentCity = []
    print('PROCESSO FINALIZADO')


