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
                // Do something with the results.
                document.querySelector(`.${formName}.callout`).innerHTML = result.message
                const tableBody = document.querySelector(`.${formName}TableBody`)
                const newRow = buildRow(formName, JSON.parse(result.record)[0])
                tableBody.prepend(newRow)
            }
        })
    }
}

function buildRow(model, record){
    const newRow = document.createElement("tr")
    switch (model) {
        case "transaction":
            newRow.innerHTML = `
                <td>${record.fields.date}</td>
                <td>${record.fields.isIncome ? "to" : "From"}</td>
                <td>${record.fields.account.name}</td>
                <td>${record.fields.amount}</td>
            `
        case "account":
            newRow.innerHTML =  `
                <td>
                    <a href="${record.pk}">
                        ${record.fields.name}
                    </a>
                </td>
                <td>${record.fields.description}</td>
                <td>${record.fields.startingBalance}</td>
            `
        default:
            //do nothing
    }

    return newRow;
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
            // Do something with the results.
            console.log(result)
        }
    })
}