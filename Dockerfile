FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir komootgpx

COPY . .

ENV CACHE_DIR=/app/cache
RUN mkdir -p $CACHE_DIR

VOLUME ["/app/cache"]

CMD ["python", "bot.py"] 