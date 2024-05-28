// Función para manejar el clic del botón para /hello_ud
function handleHelloUd() {
    fetch('/hello_ud') // Realizar una solicitud GET a la ruta /hello_ud
        .then(response => response.text()) // Convertir la respuesta a texto
        .then(data => {
            alert(data); // Mostrar la respuesta en una alerta
        })
        .catch(error => {
            console.error('Error:', error); // Manejar errores
        });
}

// Función para manejar el clic del botón para /products
function handleProducts() {
    fetch('/products') // Realizar una solicitud GET a la ruta /products
        .then(response => response.json()) // Convertir la respuesta a JSON
        .then(data => {
            // Mostrar los productos en la consola
            console.log('Products:', data);
            // Aquí podrías agregar código para mostrar los productos en tu página HTML
        })
        .catch(error => {
            console.error('Error:', error); // Manejar errores
        });
}
