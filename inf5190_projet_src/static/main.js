//-----------------------------------------------------------------------------
// CONSTANTS //
//-----------------------------------------------------------------------------

//-----------------------------------------------------------------------------
// FUNCTIONS //
//-----------------------------------------------------------------------------
/**
 * Async function that return the response of GET http request of an url
 *
 * @param url
 * @param fct
 */
function loadDoc(url, fct) {
    alert(OK)
    const arrondissement = document.getElementById("arrondissement").value
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            fct(this);
        }
    };
    xhr.open("GET", url + arrondissement, true);
    xhr.send();
}

/**
 * Call back funtion used to as purpose to get the result
 * of : /installations?arrondissements={arrondissement}
 *
 * @param xhr
 */
function getInstallationsForDistrict(xhr) {
    document.getElementById("result").innerHTML = xhr.responseText;
}

/**
 * Call back funtion used to as purpose to get the result
 * /installations?installation={installation}
 *
 * @param xhr
 */
function getInstallationsDataForSpecificInstallation(xhr) {
    document.getElementById("result").innerHTML = xhr.responseText;
}

//-----------------------------------------------------------------------------
// END OF FILE //
//-----------------------------------------------------------------------------