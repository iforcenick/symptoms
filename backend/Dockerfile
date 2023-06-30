FROM python:3.11.2

WORKDIR /app

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "migration.py"] && ["python3", "main.py"]