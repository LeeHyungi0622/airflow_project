FROM python:3.7-slim

COPY ./api /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["uvicorn", "api:main", "--host", "0.0.0.0", "--port", "80"]