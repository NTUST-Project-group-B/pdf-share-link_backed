from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from domain.models import click_limit_reached, link_expired, link_not_found
from server.config import CORS_ORIGINS, PAGE_HTML_PATH
from server.dependencies import get_link_service
from service.link_service import link_service

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = CORS_ORIGINS,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@app.get("/")
async def root() -> FileResponse:
    return FileResponse(PAGE_HTML_PATH)

@app.post("/upload")
async def upload_pdf(
    file : UploadFile,
    request : Request,
    service : link_service = Depends(get_link_service),
) -> dict[str, str]:
    new_link = service.create_share_link(file.filename, file.file)
    return {"url": f"{request.base_url}download/{new_link.token}"}

@app.get("/download/{token}")
async def download_pdf(
    token : str,
    service : link_service = Depends(get_link_service),
) -> FileResponse:
    try:
        found, file_path = service.resolve_download(token)
    except link_not_found as exc:
        raise HTTPException(status_code=404, detail="token not found") from exc
    except link_expired as exc:
        raise HTTPException(status_code=410, detail="link expired") from exc
    except click_limit_reached as exc:
        raise HTTPException(status_code=403, detail="click limit reached") from exc

    return FileResponse(
        path = file_path,
        media_type = "application/pdf",
        headers = {"Content-Disposition": f'inline; filename="{found.original_filename}"'},
    )
