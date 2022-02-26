# Importar bibliotecas
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import config
from paginas.php_myadmin import PhpMyAdmin
from paginas.login import Login

def processar():
    print(" --- Processo iniciado   ---")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=config.options)  # Instanciar navegador
    Login(driver, config.credenciais)  # Fazer login
    phpmyadmin_exportar = PhpMyAdmin(driver)
    phpmyadmin_exportar.gerar_exportacao()
    time.sleep(7)  # Aguardar download do arquivo
    driver.quit()  # Fechar navegador
    phpmyadmin_exportar.processa_arquivo()

    print(" --- Processo finalizado ---")

if __name__ == '__main__':
    processar()
