# pdf-share-link 後端

上傳 PDF，換取一個有效期 7 天、最多能點 10 次的分享連結。FastAPI + PostgreSQL，以 Docker Compose 部署。

## 架構

```
domain/    規則（過期、點擊次數）與例外，不依賴任何工具
service/   用例：上傳換連結、用 token 換檔案
db/        資料庫接口 interface.py + 實作（postgres_repository.py、sqlite_repository.py）
api/       檔案儲存接口 interface.py + 實作（local_storage.py）
server/    FastAPI 路由、設定、依賴注入（決定現在用哪個實作）
```

service 只認識 `db/interface.py` 與 `api/interface.py`，換資料庫或儲存只需改 `server/dependencies.py`。

## 一行指令啟動

需要 Docker 與 Docker Compose。

```bash
cp .env.example .env      # 至少修改 POSTGRES_PASSWORD
docker compose up --build -d
```

啟動後開 `http://主機IP:8000` 即可上傳。停止：`docker compose down`（資料保留）；連資料一起清除：`docker compose down -v`。

## 環境變數（.env）

| 變數 | 說明 | 預設 |
|---|---|---|
| BACKEND_PORT | 對外埠號 | 8000 |
| POSTGRES_USER / POSTGRES_PASSWORD / POSTGRES_DB | Postgres 帳密與資料庫名 | app / change-me / pdfshare |
| CORS_ORIGINS | 允許呼叫的前端網址（逗號分隔），`*` 為全部 | * |

## API

- `POST /upload`：表單欄位 `file`，回傳 `{"url": ".../download/<token>"}`
- `GET /download/{token}`：200 回傳 PDF；404 token 不存在；410 已過期；403 點擊次數用完

## 本機開發（不用 Docker）

不設定 `DATABASE_URL` 時會退回 SQLite，資料存在 `mydata.db`：

```bash
uv sync
uv run uvicorn server.app:app --reload
```
