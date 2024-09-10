FROM python:3.12.5-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/download/v3.4.10/tailwindcss-linux-x64 && \ 
    chmod +x tailwindcss-linux-x64 && \
    mv tailwindcss-linux-x64 tailwindcss

COPY run.sh .
COPY app.py .
COPY tailwind.config.js .
COPY tailwind.input.css .
COPY static static
COPY templates templates

RUN ./tailwindcss -i tailwind.input.css -o ./static/css/tailwind.css -c tailwind.config.js --minify


ENV ENGINE_URL=http://127.0.0.1:6878

CMD ["./run.sh"]
