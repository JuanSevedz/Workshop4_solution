"""
Imports necessary libraries and modules for setting up a FastAPI application with SQLAlchemy integration.

Imports:
- uvicorn: ASGI server to run FastAPI application.
- FastAPI: Framework for building APIs with Python.
- HTTPException: Exception to raise for HTTP errors.
- Response: Class to represent an HTTP response.
- CORSMiddleware: Middleware for enabling Cross-Origin Resource Sharing (CORS).
- StaticFiles: Middleware for serving static files.
- Column, Integer, String, MetaData, Table: SQLAlchemy components for defining database schema.
- create_engine: Function to create a SQLAlchemy database engine.
- SQLAlchemyError: Base class for exceptions raised by SQLAlchemy.
- sessionmaker: Function to create a new session class with a given sessionmaker configuration.
"""
import os
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Response
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, Session, declarative_base,Query
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Cargar variables de entorno
load_dotenv()

# Inicializar la aplicación FastAPI
app = FastAPI()

# Crear la conexión a la base de datos
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_URL')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(DATABASE_URL)

# Crear la sesión de SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarar la base de datos y la tabla
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

Base.metadata.create_all(bind=engine)

# Modelos Pydantic para validar los datos de entrada y respuesta
class ProductCreate(BaseModel):
    name: str
    description: str

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str

class Config:
    from_attributes = True  # Cambia 'orm_mode' a 'from_attributes'


# Configurar middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes de cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados HTTP
)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta para crear un nuevo producto
@app.post("/products/add", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Creates a new product.
    """
    try:
        db_product = Product(name=product.name, description=product.description)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating product") from e

# Define route for the favicon
@app.get("/favicon.ico")
async def get_favicon():
    """
    Returns the favicon.
    """
    return Response(content=b"", media_type="image/x-icon")
# Main route, only to verify the program working.
@app.get("/")
async def root():
    """
    Returns a welcome message.
    """
    return {"message": "Welcome to my FastAPI application!"}


# Ruta para obtener un mensaje de bienvenida
@app.get("/hello_ud")
def hello_ud():
    """
    Returns a welcome message specific to UD.
    """
    return "Welcome to UD!"
# Ruta para obtener todos los productos
@app.get("/products", response_model=list[ProductResponse]) 
def get_products(db: Session = Depends(get_db)):
    """
    Returns all products.
    """
    products_query = db.query(Product).order_by(Product.id)  # Ordenar por ID
    products = products_query.all()
    return products

# Ejecutar la aplicación usando Uvicorn
if __name__ == "__main__":
    print("Starting Uvicorn server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)