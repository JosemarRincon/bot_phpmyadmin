from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from page_objects import PageObject
from localizadores.localizadores import Localizadores
import config


class Login(PageObject):

    def __init__(self, driver, credenciais):
        self.driver = driver
        self.driver.set_window_size(1920, 1080)
        self.url = Localizadores.login['url']
        self.username = Localizadores.login['username']
        self.password = Localizadores.login['password']
        self.submit = Localizadores.login['submit']

        print("\nPágina de Login")
        self.logar(driver, credenciais)

    def digitar_username(self, usuario):
        WebDriverWait(self.driver, config.timeout).until(ec.presence_of_element_located((By.NAME, self.username)))
        self.driver.find_element(By.NAME, self.username).send_keys(usuario)

    def digitar_password(self, senha):
        WebDriverWait(self.driver, config.timeout).until(ec.presence_of_element_located((By.NAME, self.password)))
        self.driver.find_element(By.NAME, self.password).send_keys(senha)

    def clicar_botao(self):
        WebDriverWait(self.driver, config.timeout).until(ec.presence_of_element_located((By.ID, self.submit)))
        self.driver.find_element(By.ID, self.submit).click()

    def logar(self, driver, credenciais):
        print("> Informando usuário e senha")
        driver.get(self.url)
        self.digitar_username(credenciais['usuario'])
        self.digitar_password(credenciais['senha'])
        self.clicar_botao()
        print("> Login Feito")
