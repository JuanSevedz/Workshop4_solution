// Función para llamar al servicio de mensaje
async function callMessage() {
    try {
        const response = await fetch('http://0.0.0.0:8000/hello_ud');
        if (response.ok) {
            const data = await response.json();
            renderJSON(data);
        } else {
            throw new Error('Error al obtener los datos: ' + response.statusText);
        }
    } catch (error) {
        console.error('Error en la llamada a callMessage:', error);
    }
}

// Función para llamar al servicio web y renderizar la tabla
async function callWebService() {
    try {
        const response = await fetch('http://localhost:8000/products');
        if (!response.ok) {
            throw new Error('Error al obtener los datos: ' + response.statusText);
        }
        const data = await response.json();
        
        renderJSON(data);
    } catch (error) {
        console.error('Error en la llamada a callWebService:', error);
    }
}

// Función para renderizar el contenido JSON en la página
// Función para renderizar el contenido JSON en forma de tabla en la página
function renderJSON(data) {
    const resultElement = document.getElementById('result');
    if (resultElement) {
        // Verificar si los datos son una matriz antes de iterar sobre ellos
        if (Array.isArray(data)) {
            // Crear la tabla
            let table = '<table>';
            table += '<tr><th>ID</th><th>Name</th><th>Description</th></tr>';

            // Iterar sobre los datos y agregar filas a la tabla
            data.forEach(item => {
                table += `<tr><td>${item.id}</td><td>${item.name}</td><td>${item.description}</td></tr>`;
            });

            table += '</table>';

            // Asignar la tabla al elemento result
            resultElement.innerHTML = table;
        } else {
            // Si los datos no son una matriz, mostrarlos como están en el elemento result
            resultElement.innerText = data;
        }
    } else {
        console.error('Elemento con ID "result" no encontrado en la página.');
    }
}

