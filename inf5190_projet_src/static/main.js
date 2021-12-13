function onSubmitDistrict() {
    const arrondissement = document.getElementById("arrondissement").value
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                alert(xhr.responseText)
            } else {
                console.log("Error, there's was an error with the server!")
            }
        }
    }
    xhr.open("GET", '/installations?arrondissement=' + arrondissement, true);
    xhr.send();
}

function onSelectInstallation() {
    const installation = document.getElementById("select-installation").value
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === XMLHttpRequest.DONE) {
            if (xhttp.status === 200) {
                alert(xhttp.responseText)
            } else {
                console.log("Error, there's was an error with the server!")
            }
        }
    }
    xhttp.open("GET", '/installations?installation=' + installation, true);
    xhttp.send();
}
document.getElementById("arrondissement-btn").addEventListener("click", onSubmitDistrict)
