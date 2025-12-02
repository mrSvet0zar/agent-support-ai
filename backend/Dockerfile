FROM python:3.11-slim AS builder

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

# Copier les dépendances installées
COPY --from=builder /install /usr/local

# Copier le code du backend
COPY ./app ./app

# Variables d’environnement recommandées
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Lancer l'API en production via Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
