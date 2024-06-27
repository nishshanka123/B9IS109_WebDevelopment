/**
 * Java script functions for handling request/response
 */

// function to handle form events

document.addEventListener('DOMContentLoaded', function () {
    // Select all forms
    const forms = document.querySelectorAll('form');

    // Add event listener to each form
    forms.forEach(form => {
        form.addEventListener('submit', function (event) {
            // stop executing default form action event.
            event.preventDefault();

            // get the form data to serialize the request
            // Serialize form data
            const formData = new FormData(form);
            const data = {};
            formData.forEach((value, key) => {
                data[key] = value;
            });

            // debug log---remove later.
            console.log("Nishshanka----> ", data);

            // check with a debug log for form data
            //for (const [name, value] of formData) {
            //    console.log(`${name}: ${value}`);
            //}

            // Example: Send data via Fetch API
            fetch(form.action, {
                method: form.method,
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                // Handle the response data
                console.log(data);
                const responseMessage = document.getElementById('responseMessage');
                if (data.message) {
                    responseMessage.innerHTML = `<p>${data.message}</p>`;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                const responseMessage = document.getElementById('responseMessage');
                responseMessage.innerHTML = `<p>Error processing the response: ${error.message}</p>`;
            });
            
        });
    });
});

