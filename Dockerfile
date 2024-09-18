FROM python:3.12.5-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

#install tailwind
RUN curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/download/v3.4.10/tailwindcss-linux-x64 && \ 
    chmod +x tailwindcss-linux-x64 && \
    mv tailwindcss-linux-x64 tailwindcss

#install fontawasome
RUN curl -sLO https://use.fontawesome.com/releases/v6.6.0/fontawesome-free-6.6.0-web.zip && \
    unzip fontawesome-free-6.6.0-web.zip && \
    mkdir static && \
    mv fontawesome-free-6.6.0-web static/fontawesome && \
    rm fontawesome-free-6.6.0-web.zip

#install clipboard.js
RUN curl -sLO https://github.com/zenorocha/clipboard.js/archive/refs/tags/v2.0.11.zip && \
    unzip v2.0.11.zip && \
    mv clipboard.js-2.0.11 static/clipboard && \
    rm v2.0.11.zip


COPY run.sh .
COPY tailwind.config.js .
COPY tailwind.input.css .
COPY static static
COPY app.py .
COPY templates templates


RUN ./tailwindcss -i tailwind.input.css -o ./static/css/tailwind.css -c tailwind.config.js --minify


ENV ENGINE_URL=http://127.0.0.1:6878

CMD ["./run.sh"]
