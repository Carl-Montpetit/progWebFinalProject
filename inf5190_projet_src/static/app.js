function sendRequest() {
    let xhttp = new XMLHttpRequest()
    // let result = document.getElementById('result')
    const arrondissement = document.getElementById("district").value
    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === XMLHttpRequest.DONE && xhttp.status === 200) {
            alert(xhttp.responseText)
        } else {
            alert("Error, there's no result for that district!")
        }
    }
    xhttp.open('GET', '/installations?arrondissement=' + arrondissement, true)
    xhttp.send()
}

document.getElementById("district-form").addEventListener("onSubmit", sendRequest)
