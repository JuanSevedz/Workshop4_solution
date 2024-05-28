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
import uvicorn
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

# Create the connection to the database
engine = create_engine('postgresql://postgres:Sarita2023@localhost:5432/postgres')

# Create the SQLAlchemy session
Session = sessionmaker(bind=engine)
session = Session()

# Define the metadata and the table
metadata = MetaData()
products = Table('products', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('name', String),
                 Column('description', String))

# Initialize the FastAPI application
app = FastAPI()

# Define route for the favicon
@app.get("/favicon.ico")
async def get_favicon():
    """
    Returns the favicon.
    """
    return Response(content=b"", media_type="image/x-icon")

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows requests from any origin
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Main route, only to verify the program working.
@app.get("/")
async def root():
    """
    Returns a welcome message.
    """
    return {"message": "Welcome to my FastAPI application!"}

# Hello route
@app.get("/hello_ud")
def hello_ud():
    """
    Returns a welcome message specific to UD.
    """
    return "Welcome to UD!"

# Route to get all products
@app.get("/products")
def get_products():
    """
    Returns all products.
    """
    try:
        query = products.select()
        result = session.execute(query)
        products_list = result.fetchall()
        # Convert results to JSON format
        return [{"id": row.id, "name": row.name, "description": row.description} for row in products_list]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Error retrieving products")from e

# Route to create a new product
@app.post("/products")
def create_product(name: str, description: str):
    """
    Creates a new product.
    """
    try:
        query = products.insert().values(name=name, description=description)
        session.execute(query)
        session.commit()
        return {"message": "Product created successfully"}
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Error creating product") from e

# Run the application using Uvicorn
if __name__ == "__main__":
    print("Starting Uvicorn server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
