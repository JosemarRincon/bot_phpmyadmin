import os


class Localizadores:
    login = {
        'url': os.environ['URL_PHPMYADMIN'],
        'username': 'pma_username',
        'password': 'pma_password',
        'submit': 'input_go'
    }

    locations = {
        'bt_exportar': '/html/body/div[3]/div[2]/div/ul/li[5]/a',
        'bt_tipo_arquivo': 'plugins',
        'bt_radio_personalizar': 'radio_custom_export',
        'id_separar_files': 'checkbox_as_separate_files',
        'id_nome_exportacao': 'filename_template',
        'bt_check_colunas': 'checkbox_csv_columns',
        'bt_executar': '//*[@id="buttonGo"]'
    }
