FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN pip install -r req.txt

CMD ["gunicorn", "webapp.wsgi:application", "--bind", "0.0.0.0:8000"]
