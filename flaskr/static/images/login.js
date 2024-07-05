/**
 * Java script functions for handling request/response
 */

// function to handle form events

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

            // debug log---remove later.
            console.log("Nishshanka----> ", data);

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
                if (data) {
                    //responseMessage.innerHTML = `<div class="message"><p>${data.data.message}</p></div>`;

                    if (data.data.status === 'success') {
                        window.location.href = data.data.redirect_url;
                    } else {
                        //alert(result.message);
                        login_form = document.getElementById('login_form');
                        login_form.reset();
                        responseMessage.innerHTML = `<div class="message"><p>${data.data.message}</p></div>`;
                    }
                }
            })
            .catch(error => {
                login_form = document.getElementById('login_form');
                login_form.reset();
                console.error('Error:', error);
                const responseMessage = document.getElementById('responseMessage');
                responseMessage.innerHTML = `<p>Error processing the response: ${error.message}</p>`;
            });
            
        });
    });
});

