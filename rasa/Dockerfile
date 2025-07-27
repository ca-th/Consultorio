# FROM rasa/rasa:3.x.x-full (SUBSTITUA 3.x.x pela sua versão exata do Rasa!)
FROM rasa/rasa:3.6.0-21

WORKDIR /app

COPY . /app

EXPOSE 5005

CMD ["rasa", "run", "--enable-api", "--port", "5005", "--debug", "--model", "models/20250726-231142-instant-dynamic.tar.gz"]
