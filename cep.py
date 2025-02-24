from typing import List
import requests
import threading
import json
from config import postgresSpecificConfig as db

class Cep:
    def __init__(self, start:str, end:str):
        self.start = start
        self.end = end


class Address:
    def __init__(self, addres:dict):
        self.cep = addres["cep"]
        self.logradouro = addres["logradouro"]
        self.complemento = addres["complemento"]
        self.unidade = addres["unidade"]
        self.bairro = addres["bairro"]
        self.localidade = addres["localidade"]
        self.uf = addres["uf"]
        self.estado = addres["estado"]
        self.regiao = addres["regiao"]
        self.ibge = addres["ibge"]
        self.gia = addres["gia"]
        self.ddd = addres["ddd"]
        self.siafi = addres["siafi"]
    
    def getDict(self):
        return {
            "logradouro": self.logradouro,
            "bairro": self.bairro,
            "localidade": self.localidade,
            "uf": self.uf,
            "estado": self.estado,
            "regiao": self.regiao,
        }

def fetch_all_as_dict(cursor):
    """ Converte resultados de cursor.fetchall() em uma lista de dicionários """
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def insertState(addressList: List["Address"]) -> None:
    conn = db.conn
    cursor = conn.cursor()
    states = set()

    for address in addressList:
        states.add((address.estado, address.uf))

    if states:
        insert_query = "INSERT INTO state (name, code) VALUES (%s, %s) ON CONFLICT (code) DO NOTHING"
        cursor.executemany(insert_query, states)
    
    conn.commit()
    cursor.close()

def insertCities(addressList: List["Address"]) -> None:
    conn = db.conn
    cursor = conn.cursor()

    cursor.execute("SELECT id, code FROM state")
    states_dict = {state["code"]: state["id"] for state in fetch_all_as_dict(cursor)}

    cityTuples = set()
    for address in addressList:
        state_id = states_dict.get(address.uf)
        if state_id:
            cityTuples.add((address.localidade, state_id))

    if cityTuples:
        insert_query = "INSERT INTO city (name, state_id) VALUES (%s, %s) ON CONFLICT (name, state_id) DO NOTHING"
        cursor.executemany(insert_query, cityTuples)

    conn.commit()
    cursor.close()

def insertDistricts(addressList: List["Address"]) -> None:
    conn = db.conn
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM city")
    cities_dict = {city["name"]: city["id"] for city in fetch_all_as_dict(cursor)}

    districtsTuples = set()
    for address in addressList:
        city_id = cities_dict.get(address.localidade)
        if city_id:
            districtsTuples.add((address.bairro, city_id))

    if districtsTuples:
        insert_query = "INSERT INTO district (name, city_id) VALUES (%s, %s) ON CONFLICT (name, city_id) DO NOTHING"
        cursor.executemany(insert_query, districtsTuples)

    conn.commit()
    cursor.close()

def insertStreets(addressList: List["Address"]) -> None:
    conn = db.conn
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM district")
    districts_dict = {district["name"]: district["id"] for district in fetch_all_as_dict(cursor)}

    streetTuples = set()
    for address in addressList:
        district_id = districts_dict.get(address.bairro)
        if district_id:
            streetTuples.add((address.logradouro, district_id))

    if streetTuples:
        insert_query = "INSERT INTO street (name, district_id) VALUES (%s, %s) ON CONFLICT (name, district_id) DO NOTHING"
        cursor.executemany(insert_query, streetTuples)

    conn.commit()
    cursor.close()

def dbSave(addressList: List["Address"]) -> None:
    insertState(addressList)
    insertCities(addressList)
    insertDistricts(addressList)
    insertStreets(addressList)

def handleWeirdCase(cep: Cep, firstPart:int, lastPart:int) -> str:
    startSplited = cep.start.split('-')
    if cep.start[0] == '0' and len(startSplited[0]) > len(f"{firstPart}"):
        firstPart = f"{firstPart:05}"
    if len(startSplited[1]) > len(f"{lastPart}"):
        lastPart = f"{lastPart:03}"
    return f"{firstPart}{lastPart}"

def extractInfo(title:str, cep: Cep) -> list:
    print(f"Extraido dados da regiao {title}")
    startSplited = cep.start.split('-')
    startFirstPart = int(startSplited[0])
    startLastPart = int(startSplited[1])
    endSplited = cep.end.split('-')
    endFirstPart = int(endSplited[0])
    endLastPart = int(endSplited[1])
    currentCep = ''

    results = []
    savedValues = {"values": [], "lastCep": None}
    try:
        savedValues = open('savedCeps.json')
    except:
        pass

    for firstPart in range(startFirstPart, endFirstPart + 1):
        for lastPart in range(startLastPart, endLastPart + 1):
            currentCep = handleWeirdCase(cep, firstPart, lastPart)
            if savedValues["lastCep"] and savedValues["lastCep"] == currentCep:
                continue
            url = f"https://viacep.com.br/ws/{currentCep}/json/"
            print(f"CEP: {currentCep}")
            count = 1
            while True:
                response = requests.get(url)
                print(f"---> TENTATIVA {count}, {response.json()}")
                if response.status_code == 200:
                    data = response.json()
                    try:
                        address = Address(data)
                        results.append(address)
                    except:
                        pass
                    break
                if response.status_code == 504:
                    print("SALVANDO RESULTADOS")
                    saveJson(results, currentCep)
                count += 1
    print(f"Regiao {title} finalizada")
    return results

def saveJson(colectedData: List["Address"], lastCep:str) -> None:
    if(len(colectedData) == 0):
        print("LISTA VAZIA, NENHUM RESULTADO SALVO!")
        return
    fileName = 'savedCeps.json'
    dataToSave = [d.getDict() for d in colectedData]
    currentSavedData = {"values": [], "lastCep": ""}
    try:
        currentSavedData = openJson(fileName)
    except:
        pass
    currentSavedData["values"] += dataToSave
    currentSavedData["lastCep"] = lastCep

    with open(fileName, 'w', encoding='utf-8') as file:
        json.dump(currentSavedData + dataToSave, file, indent=4, ensure_ascii=False)

def openJson(fileName:str) -> dict:
    try:
        with open(fileName, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Erro: O arquivo '{"ceps.json"}' não foi encontrado.")
    except json.JSONDecodeError:
        print(f"Erro: O arquivo '{"ceps.json"}' não contém um JSON válido.")


def run() -> None:
    southest = Cep("01000-000", "39999-999")
    northest = Cep("40000-000", "65999-999")
    north = Cep("66000-000", "77999-999")
    westCenter = Cep("70000-000", "79999-999")
    south = Cep("80000-000", "99999-999")

    southestThread = threading.Thread(target=extractInfo, args=('southest', southest))
    northestThread = threading.Thread(target=extractInfo, args=('northest', northest))
    northThread = threading.Thread(target=extractInfo, args=('north', north))
    westCenterThread = threading.Thread(target=extractInfo, args=('westCenter', westCenter))
    southThread = threading.Thread(target=extractInfo, args=('south', south))

extractInfo('southest', Cep("01000-000", "39999-999"))