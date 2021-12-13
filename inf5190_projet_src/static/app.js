function onSubmitDistrict() {
    let xhttp = new XMLHttpRequest()
    const arrondissement = document.getElementById("arrondissement").value
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


function onSubmitDistrict() {
    const arrondissement = document.getElementById("arrondissement").value
    let result = document.getElementById('result')
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                result.innerHTML = xhr.responseText
            } else {
                console.log('Erreur avec le serveur')
            }
        }
    }
    xhr.open("GET", '/installations?arrondissement=' + arrondissement, true);
    xhr.send();
}

document.getElementById("district-btn").addEventListener("onclick", onSubmitDistrict)