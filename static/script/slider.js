var slider = document.getElementById("range1");
var output = document.getElementById("range1_value");
output.innerHTML = slider.value;

slider.oninput = function () {
    output.innerHTML = slider.value;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
        }
    };
    xhttp.open("GET", "/set_speed?speed=" + slider.value, true);
    xhttp.send("/set_speed?speed=" + slider.value, true);
}