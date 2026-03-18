FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV ENV=dev
ENV HOST=0.0.0.0
ENV PORT=8000

CMD ["uvicorn", "main:app"]