import uvicorn
from fastapi import FastAPI, Response, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

# Crear la conexión a la base de datos
engine = create_engine('postgresql://postgres:Sarita2023@localhost:5432/postgres')

# Crear la sesión de SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

# Definir la metadata y la tabla
metadata = MetaData()
products = Table('products', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('name', String),
                 Column('description', String))

# Inicializar la aplicación FastAPI
app = FastAPI()



# Definir ruta para el favicon
@app.get("/favicon.ico")
async def get_favicon():
    return Response(content=b"", media_type="image/x-icon")

# Ruta principal
@app.get("/")
async def root():
    return {"message": "Welcome to my FastAPI application!"}

# Ruta de ejemplo
@app.get("/hello_ud")
def hello_ud():
    return "Welcome to UD!"


# Ruta para obtener todos los productos
@app.get("/products")
def get_products():
    try:
        query = products.select()
        result = session.execute(query)
        products_list = result.fetchall()
        # Convertir los resultados a un formato JSON
        return [{"id": row.id, "name": row.name, "description": row.description} for row in products_list]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Error al obtener productos")



# Ruta para crear un nuevo producto
@app.post("/products")
def create_product(name: str, description: str):
    try:
        query = products.insert().values(name=name, description=description)
        session.execute(query)
        session.commit()
        return {"message": "Product created successfully"}
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Error al crear producto")

# Ejecutar la aplicación usando Uvicorn
if __name__ == "__main__":
    print("Starting Uvicorn server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
