import pandas as pd
import os
import time

from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

from aws.aws_services import handle_s3

# carrega variaveis de ambiente de arquivo .env
load_dotenv()

url = 'https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br'

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get(url)

time.sleep(1)

# Encontre o elemento <select> pelo seu ID
select_element = driver.find_element(By.ID, "segment")

select = Select(select_element)
select.select_by_visible_text("Setor de Atuação")

# Rolar até o final da página
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Aguardar o elemento estar presente e visível
wait = WebDriverWait(driver, 20)  # Aumentar o tempo de espera
dropdown = wait.until(
    EC.visibility_of_element_located((By.XPATH, "//select[@id='selectPage']")))  # Clicar no dropdown para abri-lo

# Clica no dropdown
dropdown.click()

# Aguardar a opção '120' estar visível
option_120 = wait.until(EC.visibility_of_element_located((By.XPATH, "//select[@id='selectPage']/option[text()='120']")))

# Selecionar a opção '120'
option_120.click()

time.sleep(3)

# Encontrar a tabela
table = driver.find_element(By.CSS_SELECTOR, "table.table-responsive-sm.table-responsive-md")

# Obter o HTML da tabela
html_table = table.get_attribute('innerHTML')

# Analisar o HTML com BeautifulSoup
soup = BeautifulSoup(html_table, 'html.parser')

# Extrair os nomes das colunas
column_names = [th.text.strip() for th in soup.find_all('th')]

# Extrair os dados da tabela
rows = soup.find_all('tr')
data = []
for row in rows:
    cells = row.find_all('td')
    row_data = [cell.text.strip() for cell in cells]
    data.append(row_data)

driver.quit()

column_names.remove('%Setor')

# Criar o DataFrame
df = pd.DataFrame(data, columns=column_names)

df.columns = ['setor', 'codigo', 'acao', 'tipo', 'qtd_teorica', 'part', 'part_acum']

data_atual = datetime.today().strftime('%Y-%m-%d')
df['data'] = data_atual

df = df.iloc[2:]

df = df.iloc[:-2]

df.reset_index(drop=True, inplace=True)

arquivo = f'carteira-do-dia.csv'

df.to_csv(arquivo, sep=';', index=False)

# lista todos os arquivos e pastas do bucket
lista_bucket = handle_s3(
    file_name=None,
    bucket=os.getenv('bucket_name'),
    access_key=os.getenv('aws_access_key_id'),
    secret_key=os.getenv('aws_secret_access_key'),
    aws_session_token=os.getenv('aws_session_token'),
    action='list',
    object_name=None,
    prefix=''
)

# cada arquivo e pasta será removido para deixar o bucket limpo
for item in lista_bucket:
    print(item)

    if '.' in item['Key']:
        handle_s3(
            file_name=None,
            bucket=os.getenv('bucket'),
            access_key=os.getenv('aws_access_key_id'),
            secret_key=os.getenv('aws_secret_access_key'),
            aws_session_token=os.getenv('aws_session_token'),
            action='delete',
            object_name=item['Key'],
            prefix=None
        )
    else:
        handle_s3(
            file_name=None,
            bucket=os.getenv('bucket'),
            access_key=os.getenv('aws_access_key_id'),
            secret_key=os.getenv('aws_secret_access_key'),
            aws_session_token=os.getenv('aws_session_token'),
            action='delete',
            object_name=item['Key'],
            prefix=None
        )

# faz upload de um novo arquivo
handle_s3(
    file_name=arquivo,
    bucket=os.getenv('bucket'),
    access_key=os.getenv('aws_access_key_id'),
    secret_key=os.getenv('aws_secret_access_key'),
    aws_session_token=os.getenv('aws_session_token'),
    action='upload',
    object_name=None,
    prefix=None
)
