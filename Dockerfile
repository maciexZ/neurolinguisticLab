FROM python:3.7
MAINTAINER maciex

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 

WORKDIR /root

#script
COPY fokus.py . 
#google api key
COPY ######.json .

COPY __init__.py .
COPY toolsNeurolinguistic.py .

CMD python fokus.py
