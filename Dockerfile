FROM python:3.12.5-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY templates templates
COPY app.py .
COPY run.sh .


ENV ENGINE_URL=http://127.0.0.1:6878

CMD ["./run.sh"]
