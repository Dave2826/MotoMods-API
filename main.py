# Importaciones
from fastapi import FastAPI, HTTPException, Query, Header
from pydantic import BaseModel
from typing import Optional
import json
import os

# Constante de API Key
API_KEY = "Viper2028"

# Inicializar FastAPI
app = FastAPI(
    title="MotoMods API",
    description="API para gestión de modificaciones de motocicletas",
    version="1.0.0"
)

# Archivo de persistencia
DATA_FILE = "modificaciones.json"


# Modelo 1 - Modificacion completa
class Modificacion(BaseModel):
    id: int
    nombre: str
    categoria: str
    marca: str
    modelo_moto: str
    precio: float
    stock: int
    descripcion: str = ""


# Modelo 2 - Modificacion parcial (para PATCH)
class ModificacionParcial(BaseModel):
    nombre: Optional[str] = None
    categoria: Optional[str] = None
    marca: Optional[str] = None
    modelo_moto: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None
    descripcion: Optional[str] = None


# Función 1 - Cargar datos desde el JSON
def cargar_modificaciones():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        contenido = f.read()
        if not contenido.strip():
            return {}
        return json.loads(contenido)


# Función 2 - Guardar datos en el JSON
def guardar_modificaciones(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# Endpoint 1 - Raíz
@app.get("/")
def raiz():
    return {
        "mensaje": "Bienvenido a MotoMods API",
        "documentacion": "/docs"
    }


# Endpoint 2 - Listar modificaciones
@app.get("/modificaciones")
def listar_modificaciones(
    page: int = Query(1, ge=1, description="Número de página"),
    size: int = Query(10, ge=1, le=100, description="Elementos por página"),
    categoria: Optional[str] = Query(None, description="Filtrar por categoría"),
    marca: Optional[str] = Query(None, description="Filtrar por marca")
):
    # Cargar datos
    data = cargar_modificaciones()
    lista = list(data.values())

    # Aplicar filtros
    if categoria:
        lista = [m for m in lista if m["categoria"].lower() == categoria.lower()]
    if marca:
        lista = [m for m in lista if m["marca"].lower() == marca.lower()]

    # Aplicar paginación
    total = len(lista)
    inicio = (page - 1) * size
    fin = inicio + size
    resultados = lista[inicio:fin]

    # Devolver respuesta
    return {
        "total": total,
        "page": page,
        "size": size,
        "resultados": resultados
    }


# Endpoint 3 - Obtener modificación por ID
@app.get("/modificaciones/{mod_id}")
def obtener_modificacion(mod_id: int):
    # Cargar datos
    data = cargar_modificaciones()
    id_str = str(mod_id)

    # Buscar modificación
    if id_str not in data:
        raise HTTPException(status_code=404, detail="Modificación no encontrada")

    # Devolver respuesta
    return data[id_str]


# Endpoint 4 - Crear modificación
@app.post("/modificaciones", status_code=201)
def crear_modificacion(mod: Modificacion, x_api_key: Optional[str] = Header(None)):
    # Validar API Key
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API Key inválida")

    # Cargar datos
    data = cargar_modificaciones()
    id_str = str(mod.id)

    # Validar ID duplicado
    if id_str in data:
        raise HTTPException(status_code=409, detail="El ID ya existe")

    # Guardar en JSON
    data[id_str] = mod.model_dump()
    guardar_modificaciones(data)

    # Devolver respuesta
    return mod.model_dump()


# Endpoint 5 - Reemplazar modificación (PUT)
@app.put("/modificaciones/{mod_id}")
def reemplazar_modificacion(mod_id: int, mod: Modificacion, x_api_key: Optional[str] = Header(None)):
    # Validar API Key
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API Key inválida")

    # Cargar datos
    data = cargar_modificaciones()
    id_str = str(mod_id)

    # Validar existencia
    if id_str not in data:
        raise HTTPException(status_code=404, detail="Modificación no encontrada")

    # Reemplazar y guardar
    data[id_str] = mod.model_dump()
    guardar_modificaciones(data)

    # Devolver respuesta
    return mod.model_dump()


# Endpoint 6 - Actualizar modificación parcial (PATCH)
@app.patch("/modificaciones/{mod_id}")
def actualizar_modificacion(mod_id: int, mod: ModificacionParcial, x_api_key: Optional[str] = Header(None)):
    # Validar API Key
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API Key inválida")

    # Cargar datos
    data = cargar_modificaciones()
    id_str = str(mod_id)

    # Validar existencia
    if id_str not in data:
        raise HTTPException(status_code=404, detail="Modificación no encontrada")

    # Obtener solo campos enviados y actualizar
    parches = mod.model_dump(exclude_unset=True)
    data[id_str].update(parches)

    # Guardar en JSON
    guardar_modificaciones(data)

    # Devolver respuesta
    return data[id_str]


# Endpoint 7 - Eliminar modificación
@app.delete("/modificaciones/{mod_id}")
def eliminar_modificacion(mod_id: int, x_api_key: Optional[str] = Header(None)):
    # Validar API Key
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API Key inválida")

    # Cargar datos
    data = cargar_modificaciones()
    id_str = str(mod_id)

    # Validar existencia
    if id_str not in data:
        raise HTTPException(status_code=404, detail="Modificación no encontrada")

    # Eliminar registro
    del data[id_str]

    # Guardar en JSON
    guardar_modificaciones(data)

    # Devolver respuesta
    return {"mensaje": "Modificación eliminada correctamente"}
