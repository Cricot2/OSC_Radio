var slider = document.getElementById("range1");
var output = document.getElementById("range1_value");
output.innerHTML = slider.value;

slider.oninput = function () {
    output.innerHTML = slider.value;
    var xhttp = new XMLHttpRequest();

    xhttp.open("GET", "/set_volume?volume=" + slider.value, true);
    xhttp.send("/set_volume?volume=" + slider.value, true);
}