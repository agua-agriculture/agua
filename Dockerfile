FROM python3.10

WORKDIR /

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . ./

CMD [ "python3", "-m", "agua.py" ]