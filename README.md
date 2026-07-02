# MotoMods API

MotoMods API es una API RESTful desarrollada con FastAPI para administrar modificaciones de motocicletas.

## Funcionalidades

- Registrar modificaciones.
- Consultar todas las modificaciones.
- Buscar una modificación por ID.
- Filtrar por categoría.
- Filtrar por marca.
- Paginación mediante page y size.
- Actualizar registros completos (PUT).
- Actualizar parcialmente (PATCH).
- Eliminar modificaciones (DELETE).
- Persistencia de datos utilizando un archivo JSON.
- Protección mediante API Key en los métodos de escritura.

## Tecnologías

- Python
- FastAPI
- Uvicorn
- Pydantic
- JSON

## Ejecución

Instalar las dependencias:

```bash
pip install -r requirements.txt