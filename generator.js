

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

        try{
          imageRequest.send(JSON.stringify(dataJson));
        }
        catch{
          var text = document.createElement("p")
          var textNode = document.createTextNode("Uh-oh, looks like we had some troubles with the fetching process. Check the troubleshooting area above.")
          text.appendChild(textNode)
          document.body.appendChild(text)
        }

        var base64Data = imageRequest.responseText

        console.log(base64Data);

        var image = new Image();

        image.src = 'data:image/png;base64,'+base64Data;

        document.body.appendChild(image);

    }

}


 

var current_ngrok_link = "https://rested-grown-imp.ngrok-free.app/GenerateID"


 

function makeGenerator(){

  var id = document.getElementById("id").value;

  var grade = document.getElementById("grade").value;

  var pass = document.getElementById("pass").value;

  var newGen = new Generator(id, pass, current_ngrok_link, grade)

  newGen.getImage()

}



 
