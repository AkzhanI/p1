from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

import logic

app = FastAPI()


def get_db():
    conn = logic.get_conn()
    try:
        yield conn
    finally:
        conn.close()


class CategoryIn(BaseModel):
    name: str
    rules: dict[str, str]


class XpIn(BaseModel):
    category: str
    xp: int


@app.get("/categories")
def get_categories(conn=Depends(get_db)):
    return logic.load_categories(conn)


@app.post("/categories", status_code=201)
def create_category(data: CategoryIn, conn=Depends(get_db)):
    try:
        created = logic.add_category(conn, data.name, data.rules)
    except KeyError:
        raise HTTPException(status_code=422, detail="В rules нужны ключи 2, 5, 7 и 10")
    if not created:
        raise HTTPException(status_code=409, detail="Категория уже существует")
    return {"name": data.name}


@app.delete("/categories/{name}")
def delete_category(name: str, conn=Depends(get_db)):
    if name not in logic.load_categories(conn):
        raise HTTPException(status_code=404, detail="Категория не найдена")
    logic.delete_category(conn, name)
    return {"deleted": name}


@app.post("/xp", status_code=201)
def add_xp(data: XpIn, conn=Depends(get_db)):
    try:
        logic.add_xp(conn, data.category, data.xp)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"category": data.category, "xp": data.xp}


@app.get("/stats")
def get_stats(conn=Depends(get_db)):
    total_xp, level, categories_xp = logic.calculate_stats(conn)
    return {
        "total_xp": total_xp,
        "level": level,
        "categories_xp": categories_xp,
    }

from fastapi.staticfiles import StaticFiles

app.mount("/", StaticFiles(directory="static", html=True), name="static")