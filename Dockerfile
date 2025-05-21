# 1-bosqich: builder image
FROM python:3.13-slim as builder

WORKDIR /app

COPY requirements.txt .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# 2-bosqich: final image
FROM python:3.13-slim

WORKDIR /app

# builder'dan wheel fayllarni va requirements.txt'ni olib kelamiz
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# wheel fayllardan o‘rnatamiz
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt

# Sizning bot faylingizni konteynerga nusxalaymiz
COPY . .

# Botni ishga tushuramiz
CMD ["python", "-u", "bot.py"]
