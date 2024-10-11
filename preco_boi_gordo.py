from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import json
import time

# Caminho completo para o GeckoDriver
gecko_driver_path = r'C:\cardim sistemas\geckodriver.exe'  # Certifique-se de substituir pelo caminho correto

# Caminho para o executável do Firefox
firefox_binary_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'

# Configura as opções do Firefox, incluindo o caminho para o binário
options = Options()
options.binary_location = firefox_binary_path

# Configura o serviço do WebDriver com o caminho do GeckoDriver
service = Service(gecko_driver_path)

# Inicializa o WebDriver para Firefox usando o serviço configurado e as opções
driver = webdriver.Firefox(service=service, options=options)

# URL da página que queremos acessar
url = 'https://www.melhorcambio.com/boi-hoje'

# Abre a página usando o Selenium
driver.get(url)

# Espera alguns segundos para garantir que a página carregue completamente
time.sleep(5)

# Encontra o campo de input específico usando seu ID
try:
    elemento_valor = driver.find_element(By.ID, 'comercial')
    valor = elemento_valor.get_attribute('value')  # Obtém o valor do atributo 'value'

    # Salva o valor extraído em um arquivo JSON
    data = {'valor': valor}
    with open('valor_boi_hoje.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print('Dados salvos com sucesso em valor_boi_hoje.json')
finally:
    # Fecha o navegador
    driver.quit()
