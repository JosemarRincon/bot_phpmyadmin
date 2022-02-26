import os
import uuid

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from page_objects import PageObject
from localizadores.localizadores import Localizadores
import config
import time
from minio import Minio
import pandas as pd


class PhpMyAdmin(PageObject):

    def __init__(self, driver):
        self.driver = driver
        self.client = Minio(
            endpoint=config.credenciais['url_minio'], access_key=config.credenciais['access_key'],secret_key=config.credenciais['secret_key'],
            secure=False
        )

    def gerar_exportacao(self):
        print("> Gerando requisicao")
        wait = WebDriverWait(self.driver, config.timeout)

        wait.until(ec.visibility_of_element_located((By.XPATH, Localizadores.locations['bt_exportar'])))
        wait.until(ec.element_to_be_clickable((By.XPATH, Localizadores.locations['bt_exportar'])))
        self.driver.find_element(By.XPATH, (Localizadores.locations['bt_exportar'])).click()
        time.sleep(7)

        self.driver.find_element(By.ID, Localizadores.locations['bt_tipo_arquivo']).send_keys("JSON")
        self.driver.find_element(By.ID, Localizadores.locations['bt_radio_personalizar']).click();

        # wait.until(ec.visibility_of_element_located((By.ID, Localizadores.locations['bt_check_colunas'])))
        # wait.until(ec.element_to_be_clickable((By.ID, Localizadores.locations['bt_check_colunas'])))
        elemento = self.driver.find_element(By.XPATH, Localizadores.locations['bt_executar'])

        self.scroll_to_view(elemento)

        # self.driver.find_element(By.ID, Localizadores.locations['id_nome_exportacao']).send_keys("db_teste")
        # self.driver.find_element(By.ID, Localizadores.locations['id_separar_files']).click();
        # self.driver.find_element(By.ID, Localizadores.locations['bt_check_colunas']).click();

        wait.until(ec.element_to_be_clickable((By.XPATH, Localizadores.locations['bt_executar'])))
        self.driver.find_element(By.XPATH, Localizadores.locations['bt_executar']).click();

        print("> exportacao Gerada com sucesso em /app/files ")



    def scroll_to_view(self, element):
        x = element.location['x']
        y = element.location['y']
        scroll_by_coord = 'window.scrollTo(%s,%s);' % (x, y)
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", element)

    def carrega_json(self):
        import json
        # load data using Python JSON module
        with open('/app/files/localhost.json', 'r') as f:
            dados = json.loads(f.read())
        df = pd.json_normalize(dados)
        return df

    def processa_arquivo(self):
        self.nome_bucket = "teste"
        self.nome_prefixo = "db_teste"
        import uuid
        df = self.carrega_json()
        df_tabelas = df[df.type == 'table']
        lista_tabelas = list(df_tabelas['name'])
        self.deleta_minio()# deletas os arquivos do bucktet do minio
        for nome_tabela in lista_tabelas:
            tabela_tmp = df[df.name == nome_tabela]
            lista = list(tabela_tmp.data)
            df_dados = pd.json_normalize(lista[0])

            nome_arquivo = uuid.uuid4()
            arquivo_destino = '/{}/{}/{}.parquet'.format(self.nome_prefixo,nome_tabela,nome_arquivo)
            arquivo_origem = '/app/files/{}.parquet'.format(nome_tabela)
            df_dados.to_parquet(arquivo_origem)
            #enviar arquivo para minio
            self.envia_minio(arquivo_origem,arquivo_destino)
            os.remove('/app/files/{}.parquet'.format(nome_tabela))


        os.remove('/app/files/{}.json'.format('localhost'))
        print("Arquivos enviados para o minio")

    def envia_minio(self, arquivo_origem, arquivo_destino):
        result = self.client.fput_object(
            self.nome_bucket, arquivo_destino,
            arquivo_origem
        )
        print(
            "criado {0} objeto; etag: {1}, versao-id: {2}".format(
                result.object_name, result.etag, result.version_id,
            ))

    def deleta_minio(self):
        from minio.deleteobjects import DeleteObject
        arquivos_deletar = [arquivo.object_name for arquivo in
                            self.client.list_objects(bucket_name=self.nome_bucket, prefix='/{}/'.format(self.nome_prefixo), recursive=True)]
        errors = self.client.remove_objects(bucket_name=self.nome_bucket,
                                       delete_object_list=[DeleteObject(arquivo) for arquivo in arquivos_deletar])
        for error in errors:
            print('error occured when deleting object', error)
        


