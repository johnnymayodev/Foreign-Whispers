FROM python:3.11-slim

WORKDIR /app

RUN pip install gunicorn

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "main:app", "-b", "0.0.0.0:5005", "--timeout", "500"]
