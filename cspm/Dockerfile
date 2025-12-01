FROM python:3.10-slim

WORKDIR /app

COPY scanner.py .

RUN pip install boto3

CMD ["python3", "scanner.py"]

