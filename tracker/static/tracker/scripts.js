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
    // stop the submit button and prep an element as a error message as needed
    event.preventDefault();
    errorMessage = document.createElement("span");
    errorMessage.className = "formError";
    document.querySelectorAll(".formError").forEach(e => e.remove())

    // Validate form data before the post
    const formData = {};
    document.querySelectorAll(`.${formName}Data`).forEach(data => {
        if(data.required && !data.value){
            errorMessage.innerHTML = "Required";
            data.after(errorMessage.cloneNode(true));
        } else {
            formData[data.name] = data.value;
        }
    })
    
    if(document.querySelectorAll(".formError").length == 0){
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
            // return unhandled errors a single console log
            if(result.error){
                console.log(result.error)
            } else {
                // Do something with the results.
                document.querySelector(`.${formName}.callout`).innerHTML = result.message
                const tableBody = document.querySelector(`.${formName}TableBody`)
                const newRow = document.createElement("tr")
                newRow.innerHTML = buildRow(formName, JSON.parse(result.record)[0])
                tableBody.prepend(newRow)
            }
        })
    }
}

function buildRow(model, record){
    switch (model) {
        case "transaction":
            // Nothing
        case "account":
            return `
                <td>${record.fields.name}</td>
                <td>${record.fields.description}</td>
                <td>${record.fields.startingBalance}</td>
            `
        default:
            //do nothing
    }

}