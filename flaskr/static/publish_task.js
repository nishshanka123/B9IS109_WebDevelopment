/** Javascript for adding new tasks */

function generateForm() {
    // Get the number of fields from the input
    const numberOfFields = document.getElementById('no_of_fields').value;

    // Get the container where the form fields will be added
    const dynamicFormContainer = document.getElementById('dynamic_form');

    // Clear any existing fields
    dynamicFormContainer.innerHTML = '';

    // Generate new fields based on the number specified
    for (let i = 1; i <= numberOfFields; i++) {
        // Create a label for the field
        const label = document.createElement('label');
        label.setAttribute('for', `field_${i}`);
        label.innerText = `Type & Name for Field ${i}:`;

        // Create the input field
        const input = document.createElement('input');
        input.id = `field_${i}`;
        input.name = `field_${i}`;

        // Create the select box for data type
        const dataTypeSelect = document.createElement('select');
        dataTypeSelect.id = `data_type_${i}`;
        dataTypeSelect.name = `data_type_${i}`;
        const dataTypes = ['text', 'number', 'email', 'date'];
        dataTypes.forEach(type => {
            const option = document.createElement('option');
            option.value = type;
            option.text = type.charAt(0).toUpperCase() + type.slice(1);
            dataTypeSelect.appendChild(option);
        });

        // Add an event listener to change the input type based on select box value
        //dataTypeSelect.addEventListener('change', function() {
        //    input.type = this.value;
        //});

        // Append the label, select box, and input directly to the form container
        dynamicFormContainer.appendChild(label);
        dynamicFormContainer.appendChild(dataTypeSelect);
        dynamicFormContainer.appendChild(input);
        dynamicFormContainer.appendChild(document.createElement('br')); // Adding a line break for better formatting
    }
}

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
                    responseMessage.innerHTML = `<div class="message"><p>${data.data.message}</p></div>`;
                    form.reset();  // Reset the form after successful submission
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