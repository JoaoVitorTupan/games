from locust import HttpUser, task, between
import random
import string

class CategoriaLoadTest(HttpUser):
    wait_time = between(1, 3) 

    def gerar_string_aleatoria(self, tamanho=8):
        letras = string.ascii_letters
        return ''.join(random.choice(letras) for i in range(tamanho))

    @task(3)
    def listar_categorias(self):
        self.client.get("/categorias", name="GET /categorias")

    @task(1)
    def criar_categoria(self):
        nome_unico = f"Categoria LoadTest {self.gerar_string_aleatoria()}"
        
        payload = {
            "nome": nome_unico,
            "descricao": "Categoria gerada automaticamente pelo teste de carga do Locust."
        }
        
        with self.client.post("/categorias", json=payload, name="POST /categorias", catch_response=True) as response:
            if response.status_code in [200, 201]:
                response.success()
            else:
                response.failure(f"Status: {response.status_code}")