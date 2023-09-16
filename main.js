var stopLoadingAnimation = null

function startLoadingAnimation() {
    console.log("mrrow :3");
    document.getElementById("finalbutton").value = "Loading";
    var textAnimation = setInterval(updateText, 1000);
    stopLoadingAnimation = function() {
        // no memory leaks for you!!!!
        clearInterval(textAnimation);
    }

}



function updateText() {
    if (document.getElementById("finalbutton").value == "Loading...")
        document.getElementById("finalbutton").value = "Loading";
    else
        document.getElementById("finalbutton").value += ".";
}

function generateID() {
    startLoadingAnimation()
    var id = document.getElementById("username").value;
    var pass = document.getElementById("password").value;
    var grade = document.getElementById("grade").value;
    
    var json = {"userid": id, "pass": pass, "grade": grade};

    var request = new XMLHttpRequest();

    request.addEventListener("load", (event) => {
        data = request.responseText
        var a = document.createElement('a');
        stopLoadingAnimation();
        document.getElementById("finalbutton").value = "Generated!";
        a.href = "data:image/png;base64,"+data;
        a.download = id + "_IDBadge"
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
    })

    request.addEventListener("error", (event) => {
        stopLoadingAnimation();
        document.getElementById("finalbutton").value = "Error " + request.status;
    })

    console.log(json)

    request.open("POST", "https://crisp-termite-actively.ngrok-free.app/GenerateID")

    request.setRequestHeader('Content-Type', 'application/json');
    request.send(JSON.stringify(json))
}