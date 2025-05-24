#!/bin/sh

echo "Aguardando MySQL..."
until nc -z "$DB_HOST" 3306; do
  echo "Esperando MySQL ($DB_HOST:3306)..."
  sleep 2
done
echo "MySQL pronto!"

echo "Aguardando MongoDB..."
until nc -z "$MONGO_HOST" "$MONGO_PORT"; do
  echo "Esperando MongoDB ($MONGO_HOST:$MONGO_PORT)..."
  sleep 2
done
echo "MongoDB pronto!"

# Inicia o Gunicorn
echo "Iniciando Gunicorn..."
exec gunicorn app:app --bind 0.0.0.0:8000 --workers 4
