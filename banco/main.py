import uvicorn
from fastapi import FastAPI
from database.database import engine
from database.models import Base
from .routes import router

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Crear la aplicación FastAPI
app = FastAPI()

# Incluir las rutas
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("banco.main:app", host="0.0.0.0", port=8000, reload=True)