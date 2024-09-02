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

    try{
        document.querySelectorAll(".transactionDelete").forEach(element => {
            element.addEventListener("click", () => {
                return deleteTransaction(element.dataset.transactionid);
            })
        })
    } catch {
        // We expect this to be empty sometimes
    }
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
        // validate required fields before post
        if(data.required && !data.value){
            errorMessage.innerHTML = "Required";
            data.after(errorMessage.cloneNode(true));
        } else {
            // required fields filled in. Send data. Check for bool values
            if(data.type === "checkbox"){
                formData[data.name] = data.checked;
            } else {
                formData[data.name] = data.value;
            }
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
                // refresh the page
                document.location.reload()
            }
        })
    }
}

function deleteTransaction(transactionId){
    const csrfToken = document.querySelector(`.transactionTableBody input[name="csrfmiddlewaretoken"]`).value
    // Delete from server
    fetch(`/transactions/${transactionId}/`, {
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/json"
        },
        method: "DELETE",
    })
    .then(response => response.json())
    .then(result => {
        // return unhandled errors a single console log
        if(result.error){
            console.log(result.error)
        } else {
            // refresh the page
            document.location.reload()
        }
    })
}