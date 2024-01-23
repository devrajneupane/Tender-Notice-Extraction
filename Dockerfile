FROM python:3.10
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
# ENV TF_CPP_MIN_LOG_LEVEL 3
ENV DISPLAY :99
WORKDIR /usr/src/Tender-Notice-Extraction

# Install brave 🕵 , Chromedriver, tesseract-ocr and tessdata
RUN apt-get update && apt-get install -yqq wget unzip && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get install -y tesseract-ocr &&\
    apt-get update -y && apt-get install -y tesseract-ocr-nep &&\
    rm -rf /var/lib/apt/lists/*
    # apt-get clean
# RUN apt-get update -y && apt-get install -yqq apt-transport-https curl unzip\
#     && curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg \
#     && echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg arch=amd64] https://brave-browser-apt-release.s3.brave.com/ stable main" >> /etc/apt/sources.list.d/brave-browser-release.list \
#     && apt-get update -y && apt install -y brave-browser \
#     && wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip \
#     && unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ \
#     && apt-get install -y tesseract-ocr \
#     && apt-get update -y && apt-get install -y tesseract-ocr-nep \
#     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT [ "python", "source/main.py" ]
