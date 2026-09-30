FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# 先只複製依賴清單，依賴沒變時可重用建置快取
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

# 資料（資料庫與上傳檔案）放在 /data，由 volume 掛載，容器重建後不會消失
ENV DB_PATH=/data/mydata.db \
    STORAGE_DIR=/data/storage
VOLUME /data

EXPOSE 8000

CMD ["uv", "run", "--no-dev", "uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000"]
