var btn = document.getElementById("submit").addEventListener("click", displayData);

// var btn = document.getElementById("submit").onclick = displayData();
function loading() {
    document.getElementById("result").innerHTML = "Loading...";
    document.getElementById("time_elapsed").innerHTML = "Loading...";
}
function displayData() {
    var method = $("input[id='InputName']").val();
    var sql = $("textarea[id='InputMessage']").val();
    var xmlHttp = new XMLHttpRequest();
    var url = "/" + method + "?query=" + sql;

    document.getElementById('whatis').scrollIntoView();
    loading();
    xmlHttp.open("GET", url, true);
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            var responseText = xmlHttp.responseText;
            var obj = JSON.parse(responseText);
            var data = "Result: " + "\n";
            for (var o in obj['result']) {
                data += obj['result'][o] + "\n";
            }
            var time = JSON.stringify(obj['query_time']);
            document.getElementById("result").innerHTML = data;
            document.getElementById("time_elapsed").innerHTML = time + " ms";
        } else {
            var error = "Wrong Input";
            document.getElementById("result").innerHTML = error;
        }
        console.log(xmlHttp.responseText);
    };
    xmlHttp.send(null);
}
