var btn = document.getElementById("submit").addEventListener("click", displayData);

// var btn = document.getElementById("submit").onclick = displayData();

function displayData() {
    var method = $("input[id='InputName']").val();
    var sql = $("textarea[id='InputMessage']").val();
    var xmlHttp = new XMLHttpRequest();
    var url = "/" + method + "?query=" + sql;
    // var y = document.getElementById("result").innerHTML = method + sql + "JavaScript";
    xmlHttp.open("GET", url, true);
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            document.getElementById("result").innerHTML = "JavaScript" + "JavaScript";
            var responseText = xmlHttp.responseText;
            var obj = JSON.parse(responseText);
            var i = 0;
            while (i < 0) {
                i = i + 1;
            }
            var data = JSON.stringify(obj['query_time']);
            document.getElementById("result").innerHTML = data + "JavaScript";
        }
        // alert(JSON.stringify(data));
        console.log(xmlHttp.responseText);
    };
    xmlHttp.send(null);
}
