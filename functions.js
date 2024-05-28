/**
 * Calls the message service to retrieve a message from the server.
 * Renders the JSON response on the page.
 */
async function callMessage() {
    try {
        const response = await fetch('http://0.0.0.0:8000/hello_ud');
        if (response.ok) {
            const data = await response.json();
            renderJSON(data);
        } else {
            throw new Error('Error getting data: ' + response.statusText);
        }
    } catch (error) {
        console.error('Call to callMessage failed:', error);
    }
}
/**
 * Calls the web service to retrieve product data from the server.
 * Renders the JSON response on the page.
 */
async function callWebService() {
    try {
        const response = await fetch('http://localhost:8000/products');
        if (!response.ok) {
            throw new Error('Error getting data: ' + response.statusText);
        }
        const data = await response.json();
        
        renderJSON(data);
    } catch (error) {
        console.error('Call to callWebService failed:', error);
    }
}

/**
 * Renders JSON data on the page.
 * @param {Object} data - JSON data to render.
 */
function renderJSON(data) {
    const resultElement = document.getElementById('result');
    if (resultElement) {
        // Check if data is an array before iterating over it
        if (Array.isArray(data)) {
            // Make a table
            let table = '<table>';
            table += '<tr><th>ID</th><th>Name</th><th>Description</th></tr>';

            // Iterate over data and add rows to table
            data.forEach(item => {
                table += `<tr><td>${item.id}</td><td>${item.name}</td><td>${item.description}</td></tr>`;
            });

            table += '</table>';

            // Assign the table to the 'result' element
            resultElement.innerHTML = table;
        } else {
            // If the data is not an array, display it as is in the 'result' element
            resultElement.innerText = data;
        }
    } else {
        console.error('Element with ID "result" not found on the page.');
    }
}

