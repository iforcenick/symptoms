FROM python:3.11.2

WORKDIR /app

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

COPY . .

RUN python3 migration.py

CMD ["python3", "main.py"]