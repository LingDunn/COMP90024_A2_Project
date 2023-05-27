FROM python:3.8

WORKDIR /home/ubuntu/flask-app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

COPY . .

CMD ["python", "server.py"]
