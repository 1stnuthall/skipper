FROM python:3.13.3-alpine

WORKDIR /app

COPY ./src .

RUN pip install -r requirements.txt

EXPOSE 3000

CMD ["python", "main.py"]
