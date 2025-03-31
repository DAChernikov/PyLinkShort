import asyncio
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from .api import auth, links
from .core.cache import get_url_from_cache, set_url_to_cache
from .core.database import engine, Base, get_db
from .models.link import Link
from .services.analytics import update_link_stats

app = FastAPI(title="URL Shortener API", version="1.0")

# Создаем таблицы, если они еще не созданы
Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(links.router, prefix="/api/links", tags=["links"])

@app.get("/{short_code}", include_in_schema=False)
async def redirect_short_url(short_code: str):
    db = next(get_db())
    original_url = get_url_from_cache(short_code)
    if not original_url:
        link = db.query(Link).filter(Link.short_code == short_code).first()
        if not link:
            raise HTTPException(status_code=404, detail="Ссылка не найдена")
        if link.expires_at and link.expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=410, detail="Ссылка устарела")
        original_url = link.original_url
        set_url_to_cache(short_code, original_url, ttl=3600)
    asyncio.create_task(update_link_stats(short_code))
    return RedirectResponse(url=original_url, status_code=302)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)