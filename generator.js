

class Generator{


 

    constructor(user, pass, url, grade){

        this.user = user;

        this.pass = pass;

        this.url = url;

        this.grade = grade;

    }


 

    toBinary(string) {

        const codeUnits = Uint16Array.from(

          { length: string.length },

          (element, index) => string.charCodeAt(index)

        );

        const charCodes = new Uint8Array(codeUnits.buffer);

     

        let result = "";

        charCodes.forEach((char) => {

          result += String.fromCharCode(char);

        });

        return result;

      }


 

    getImage() {

       

        var dataJson = { "userid": this.user, "pass": this.pass, "grade": this.grade};

        var imageRequest = new XMLHttpRequest();

        imageRequest.open("POST", this.url, false);

        imageRequest.setRequestHeader('Content-Type', 'application/json');

        imageRequest.send(JSON.stringify(dataJson));

        var base64Data = imageRequest.responseText

        console.log(base64Data);

        var image = new Image();

        image.src = 'data:image/png;base64,'+base64Data;

        document.body.appendChild(image);

    }

}


 

var current_ngrok_link = "https://idgenerator.ngrok.io/GenerateID"


 

function makeGenerator(){

  var id = document.getElementById("id").value;

  var grade = document.getElementById("grade").value;

  var pass = document.getElementById("pass").value;

  var newGen = new Generator(id, pass, current_ngrok_link, grade)

  newGen.getImage()

}



 
