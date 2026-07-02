from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
import json
import os

API_KEY = "motomods2024"

app = FastAPI(
    title="MotoMods API",
    description="API para gestión de modificaciones de motocicletas",
    version="1.0.0"
)

DATA_FILE = "modificaciones.json"


class Modificacion(BaseModel):
    id: int
    nombre: str
    categoria: str
    marca: str
    modelo_moto: str
    precio: float
    stock: int
    descripcion: str = ""


class ModificacionParcial(BaseModel):
    nombre: Optional[str] = None
    categoria: Optional[str] = None
    marca: Optional[str] = None
    modelo_moto: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None
    descripcion: Optional[str] = None


def cargar_modificaciones():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        contenido = f.read()
        if not contenido.strip():
            return {}
        return json.loads(contenido)


def guardar_modificaciones(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


@app.get("/")
def raiz():
    return {
        "mensaje": "Bienvenido a MotoMods API",
        "documentacion": "/docs"
    }


@app.get("/modificaciones")
def listar_modificaciones(
    page: int = Query(1, ge=1, description="Número de página"),
    size: int = Query(10, ge=1, le=100, description="Elementos por página"),
    categoria: Optional[str] = Query(None, description="Filtrar por categoría"),
    marca: Optional[str] = Query(None, description="Filtrar por marca")
):
    data = cargar_modificaciones()
    lista = list(data.values())

    if categoria:
        lista = [m for m in lista if m["categoria"].lower() == categoria.lower()]
    if marca:
        lista = [m for m in lista if m["marca"].lower() == marca.lower()]

    total = len(lista)
    inicio = (page - 1) * size
    fin = inicio + size
    resultados = lista[inicio:fin]

    return {
        "total": total,
        "page": page,
        "size": size,
        "resultados": resultados
    }


@app.get("/modificaciones/{mod_id}")
def obtener_modificacion(mod_id: int):
    data = cargar_modificaciones()
    id_str = str(mod_id)
    if id_str not in data:
        raise HTTPException(status_code=404, detail="Modificación no encontrada")
    return data[id_str]
