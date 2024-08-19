document.addEventListener("DOMContentLoaded", () => {
    const forms = [
        "transaction",
        "account"
    ];

    forms.forEach(formName => {
        try{
            document.querySelector(`.${formName}Form button`).addEventListener("click", event => {
                return formHandling(event, formName);
            })
        } catch {
            // We expect some items to not be found
        }
    })
})

function formHandling(event, formName){
    // Get the form data
    event.preventDefault();
    
    const formData = {};
    document.querySelectorAll(`.${formName}Data`).forEach(data => {
        formData[data.name] = data.value;
    })
    
    // Get the token
    const csrfToken = document.querySelector(`.${formName}Form input[name="csrfmiddlewaretoken"]`).value
    
    // Post to server
    fetch(`/${formName}s/`, {
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/json"
        },
        method: "POST",
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    })
}