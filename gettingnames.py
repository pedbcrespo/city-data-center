import pymysql
from typing import List, Dict
from configuration.dev_configuration import host, user, password, database, DEEP_SEEK_API_KEY
from openai import OpenAI
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DistrictManager:
    def __init__(self):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        self.client = OpenAI(
            api_key=DEEP_SEEK_API_KEY,
            base_url='https://api.deepseek.com'
        )

    def __del__(self):
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()

    def get_states(self) -> List[Dict]:
        """Obtém todos os estados do banco de dados"""
        query = "SELECT id, name FROM state"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except pymysql.Error as e:
            logger.error(f"Erro ao buscar estados: {e}")
            return []

    def get_cities_from_state(self, state_id: int) -> List[Dict]:
        """Obtém cidades de um estado específico"""
        query = "SELECT id, name FROM city WHERE state_id = %s"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (state_id,))
                return cursor.fetchall()
        except pymysql.Error as e:
            logger.error(f"Erro ao buscar cidades do estado {state_id}: {e}")
            return []

    def save_districts(self, city_id: int, districts: List[str]) -> bool:
        """Salva bairros no banco de dados"""
        query = "INSERT INTO district (name, city_id) VALUES (%s, %s)"
        values = [(district.strip(), city_id) for district in districts if district.strip()]
        
        if not values:
            return False
            
        try:
            with self.connection.cursor() as cursor:
                cursor.executemany(query, values)
            self.connection.commit()
            return True
        except pymysql.Error as e:
            logger.error(f"Erro ao salvar bairros: {e}")
            self.connection.rollback()
            return False

    def get_districts_from_api(self, city_name: str, state_name: str) -> List[str]:
        """Obtém bairros da API da DeepSeek"""
        question = (
            f"Liste os nomes dos bairros da cidade de {city_name}, "
            f"localizada no estado {state_name}, Brasil. "
            "Forneça apenas os nomes dos bairros, um por linha, "
            "sem numeração ou comentários adicionais."
        )
        
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "Você é um assistente que fornece apenas nomes de bairros, um por linha, sem comentários."},
                    {"role": "user", "content": question},
                ],
                stream=False,
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            return [line.strip() for line in content.split('\n') if line.strip()]
        except Exception as e:
            logger.error(f"Erro na API para {city_name}/{state_name}: {e}")
            return []

    def process_all_districts(self):
        """Processa todos os estados e cidades para obter bairros"""
        states = self.get_states()
        for state in states:
            cities = self.get_cities_from_state(state['id'])
            for city in cities:
                logger.info(f"Processando {city['name']}/{state['name']}...")
                
                districts = self.get_districts_from_api(city['name'], state['name'])
                if districts:
                    success = self.save_districts(city['id'], districts)
                    if success:
                        logger.info(f"Salvos {len(districts)} bairros para {city['name']}")
                    else:
                        logger.error(f"Falha ao salvar bairros para {city['name']}")
                else:
                    logger.warning(f"Nenhum bairro encontrado para {city['name']}")

if __name__ == "__main__":
    manager = DistrictManager()
    manager.process_all_districts()