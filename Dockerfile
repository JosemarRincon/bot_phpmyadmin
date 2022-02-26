# Usar como base imagem com python:3.8
FROM python:3.8
RUN apt-get update \
    && apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 \
    libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation  libnss3 lsb-release xdg-utils

#download and install chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install \
    && pip install --upgrade pip

# Copiar todos os arquivos para o container
COPY . /app
# Instalar dependências
RUN pip --default-timeout=30 install -r app/requirements.txt
COPY . /app
# Configurar /app como diretório de trabalho
WORKDIR /app

CMD ["python","-u","app.py"]