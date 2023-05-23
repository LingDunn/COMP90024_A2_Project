FROM python:3.8

WORKDIR /home/ubuntu/flask-app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8001

COPY . .

CMD ["python", "app.py"]
