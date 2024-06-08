document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("productForm");
    const responseDiv = document.getElementById("response");
    const getMessageBtn = document.getElementById("getMessageBtn");
    const getTableBtn = document.getElementById("getTableBtn");
    const createProductBtn = document.getElementById("createProductBtn");
    const messageResponseDiv = document.getElementById("messageResponse");
    const tableResponseDiv = document.getElementById("tableResponse");

    createProductBtn.addEventListener("click", () => {
        // Mostrar el formulario para crear un producto
        form.style.display = "block";
    });

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const name = document.getElementById("name").value;
        const description = document.getElementById("description").value;

        const product = {
            name: name,
            description: description
        };

        try {
            const response = await fetch("http://localhost:8000/products/add", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: JSON.stringify(product)
            });

            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`);
            }

            const data = await response.json();
            responseDiv.innerHTML = `<p>Producto creado: ID ${data.id}, Nombre ${data.name}, Descripción ${data.description}</p>`;
        } catch (error) {
            responseDiv.innerHTML = `<p>Error creando el producto: ${error.message}</p>`;
        }
    });

    getMessageBtn.addEventListener("click", async () => {
        try {
            const response = await fetch("http://localhost:8000/hello_ud");

            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`);
            }

            const data = await response.text();
            messageResponseDiv.innerHTML = `<p>${data}</p>`;
        } catch (error) {
            messageResponseDiv.innerHTML = `<p>Error obteniendo el mensaje: ${error.message}</p>`;
        }
    });

    getTableBtn.addEventListener("click", async () => {
        try {
            const response = await fetch("http://localhost:8000/products");

            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`);
            }

            const data = await response.json();
            const tableHtml = `<table><tr><th>ID</th><th>Nombre</th><th>Descripción</th></tr>${data.map(product => `<tr><td>${product.id}</td><td>${product.name}</td><td>${product.description}</td></tr>`).join('')}</table>`;
            tableResponseDiv.innerHTML = tableHtml;
        } catch (error) {
            tableResponseDiv.innerHTML = `<p>Error obteniendo la tabla de productos: ${error.message}</p>`;
        }
    });
});