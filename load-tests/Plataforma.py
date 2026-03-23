from locust import HttpUser, task, between
from faker import Faker
import random
import xml.etree.ElementTree as ET 

fake = Faker('pt_BR')

class PlataformaTeste(HttpUser):
    wait_time = between(1, 3)
    TOKEN = "Token"
    def on_start(self):
        self.headers = {
            "Authorization": f"Bearer {self.TOKEN}",
            "Content-Type": "application/xml",
            "Accept": "application/xml"
        }
    @task
    def fluxo_criar_e_consultar(self):
        nome_faker = f"{fake.company()} {random.randint(1, 999999)}"
        fabricante_faker = fake.company()
        
        xml_payload = f"""
        <plataforma>
            <nome>{nome_faker}</nome>
            <fabricante>{fabricante_faker}</fabricante>
        </plataforma>
        """
        with self.client.post("/plataformas", data=xml_payload, headers=self.headers, name="1. POST /plataformas", catch_response=True) as response_post:
            
            if response_post.status_code == 201:
                response_post.success()

                try:
                    root = ET.fromstring(response_post.text)
                    elemento_id = root.find('id')
                    
                    if elemento_id is not None and elemento_id.text:
                        id_gerado = elemento_id.text
                        with self.client.get(f"/plataformas/{id_gerado}", headers=self.headers, name="2. GET /plataformas/{id}", catch_response=True) as response_get:
                            if response_get.status_code == 200:
                                response_get.success()
                            else:
                                response_get.failure(f"Falha no GET: Status {response_get.status_code}")
                    else:
                        response_post.failure("Sucesso no POST, mas não achamos a tag <id> no XML de retorno!")
                except ET.ParseError:
                    response_post.failure("Erro ao tentar ler o XML de resposta do POST.")
            elif response_post.status_code == 409:
                response_post.success() 
            else:
                response_post.failure(f"Erro inesperado no POST: Status {response_post.status_code}")