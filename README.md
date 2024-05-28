# Workshop4_solution

## FastAPI Application with SQLAlchemy Integration

This is a simple FastAPI application integrated with SQLAlchemy ORM for database interaction.

## Description

This application provides endpoints to manage products stored in a PostgreSQL database. It utilizes FastAPI for building APIs and SQLAlchemy ORM for interacting with the database.

## Features

- Hello UD!!
- View all products
- Create new products

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/JuanSevedz/Workshop4_solution.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the FastAPI application using Uvicorn:

    ```bash
    uvicorn main:app --reload
    ```

2. Access the API documentation in your browser:

    ```
    http://localhost:8000/docs
    ```

## Endpoints

- **GET /products:** Retrieve all products.
- **POST /products:** Create a new product.

## Configuration

Make sure to configure your database connection in the `main.py` file:

```python
engine = create_engine('postgresql://username:password@host:port/database_name')
