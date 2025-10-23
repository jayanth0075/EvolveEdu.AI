# Multi-stage build for EvolveEdu.AI

# Backend stage
FROM python:3.10-slim as backend

WORKDIR /app

COPY evolveedu-ai/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY evolveedu-ai/backend/ .

EXPOSE 8000

CMD ["gunicorn", "evolveedu.wsgi:application", "--bind", "0.0.0.0:8000"]

# Frontend stage
FROM node:18-alpine as frontend

WORKDIR /app

COPY evolveedu-ai/frontend/package.json evolveedu-ai/frontend/package-lock.json ./

RUN npm ci

COPY evolveedu-ai/frontend/ .

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
