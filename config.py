import os
from selenium import webdriver
timeout = 7  # 10 segundos

credenciais = {
    'usuario': os.environ['USUARIO'],
    'senha': os.environ['SENHA'],
    'access_key' : os.environ['MINIO_ACCESS_KEY'],
    'secret_key' : os.environ['MINIO_SECRET_ACCESS_KEY'],
    'url_minio' : os.environ['URL_MINIO']
}

options = webdriver.ChromeOptions();
prefs = {"download.default_directory": "/app/files"};
options.add_experimental_option("prefs", prefs);
options.add_argument('--remote-debugging-port=9222')
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument('--window-size=1920,1080')
options.add_argument("--disable-infobars");
options.add_argument("--disable-extensions");
options.add_argument("--disable-gpu");
options.add_argument("--disable-dev-shm-usage");


