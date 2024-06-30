document.addEventListener('DOMContentLoaded', function () {
    console.log("TEST----> ");
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
            
            // Example: Send data via Fetch API
            fetch(form.action, {
                method: form.method,
                body: formData
            })            
            .then(response => response.json())
            .then(data => {
                // Handle the response data
                console.log(data);
                //console.log({data.message});
                const responseMessage = document.getElementById('responseMessage');
                var content_container = document.getElementById('content-container');
                content_container.innerHTML = '';
                if (data) {
                    responseMessage.innerHTML = `<div class="message"><p>${data.data.message}</p></div>`;
                    form.reset();  // Reset the form after successful submission
                }
            })
            .catch(error => {
                console.error('Error:', error);
                var content_container = document.getElementById('content-container');
                content_container.innerHTML = '';

                const responseMessage = document.getElementById('responseMessage');
                responseMessage.innerHTML = `<p>Error processing the response: ${error.message}</p>`;
            });
            
        });
    });
});