FROM python:3.7
MAINTAINER maciex

#konieczne biblioteki do odpalenia skryptu
COPY requirements.txt .

#do tych folderów roboczo kopiowane będą wersje jezykowe
#instalacja wymaganych papiektów
RUN pip install --no-cache-dir -r requirements.txt && apt-get -y update && apt-get install -y libsndfile1

WORKDIR /root

#jeżeli zmienisz fokus.py to trzeba budować od nowa
COPY fokus.py . 
#uwaga delikatne - usuwać po wykorzystaniu
COPY scienceAgata-67f0c7478515.json .

COPY __init__.py .
COPY main2_linux.py .

CMD python fokus.py
