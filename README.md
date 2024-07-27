# WEB-SCRAPING-B3

## Script de Extração de Dados da B3 e Upload para S3

Este script automatiza a extração de dados da página de listagem do IBOV da B3 e o upload do 
arquivo CSV resultante para um bucket S3.

Pode se observar que o código lista todos os arquivos e pastas dentro do bucket e depois deleta eles
para poder deixar ele sempre limpo, fazendo um novo upload sempre no diretório raiz, é possível modificar este 
comportamento alterando a lófica de deleções dentro do for.

### Pré-requisitos

* Python 3.x, utilizei o 3.12
* Bibliotecas Python:
    * pandas
    * os
    * time
    * BeautifulSoup4
    * datetime
    * dotenv
    * selenium
    * webdriver_manager
    * [Seu módulo de acesso ao S3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html) -  Você pode usar boto3 ou qualquer outra biblioteca que você preferir.
* Credenciais de acesso ao S3:
    * Configure as variáveis de ambiente necessárias (por exemplo, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`) em um arquivo `.env` na raiz do projeto.
* Driver do Chrome:
    * O script usa o driver do Chrome para automatizar o navegador. Certifique-se de que o driver está instalado em seu sistema. Você pode instalá-lo usando a biblioteca `webdriver_manager`.

### Instalação

1. Crie um novo ambiente virtual:
   ```bash
   python3 -m venv env
   source env/bin/activate 
   ```
2. Instale as bibliotecas necessárias:
   ```bash
   pip install -r requirements.txt
   ```

### Configuração

1. Crie um arquivo `.env` na raiz do projeto e adicione suas credenciais de acesso ao S3 e o nome do bucket:
   ```
   aws_access_key_id = your_aws_access_key_id
   aws_secret_access_key = your_aws_secret_access_key
   aws_session_token = your_aws_session_token
   bucket_name = your_bucket_name
   ```
2. Substitua `your_aws_access_key_id`, `your_aws_secret_access_key`, `your_aws_session_token` e `your_bucket_name` pelos seus próprios valores.

### Execução

1. Execute o script:
   ```bash
   python main.py 
   ```

### Funcionalidades

* O script abre a página de listagem do IBOV da B3.
* Seleciona o segmento "Setor de Atuação".
* Carrega todas as páginas de dados (até 120 páginas).
* Extrai os dados da tabela HTML e os armazena em um DataFrame Pandas.
* Adiciona a data atual aos dados.
* Salva os dados em um arquivo CSV com o nome "carteira-do-dia.csv".
* Lista os arquivos existentes no bucket S3 e deleta qualquer arquivo ou pasta.
* Faz o upload do arquivo CSV para o bucket S3.

### Observações

* A frequência de atualização dos dados na B3 pode variar.
* O script foi desenvolvido para o site da B3 na data de criação deste README. Eventuais mudanças no site podem requerer modificações no script.
* O script pode ser adaptado para extrair dados de outras páginas da B3 ou de outros sites.

### Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues, enviar pull requests ou fazer sugestões.

