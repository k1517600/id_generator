# imports
import json
import time
import os

from PyPDF2 import PdfReader

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import PIL
from PIL import Image, ImageDraw, ImageFont
from flask import Response
import base64
from io import BytesIO

from selenium.webdriver.chrome.service import Service

from threading import Thread

katy_cloud_url = "https://login.katyisd.org/app/katyisd_mykatycloud_1/exk1dttjo5AcJmPwc697/sso/saml"

app = Flask(__name__)

CORS(app)

global google


@app.route("/api", methods=["POST"])
@cross_origin()
def api():
    prompt: str = request.json["prompt"]
    if prompt.count("hi") > 0:
        return Response("Hello")


@app.route("/ping", methods=['GET'])
@cross_origin()
def ping():
    return Response("Pong", 200)


@app.route("/GenerateID", methods=['POST'])
@cross_origin()
def get_id_picture():
    request_json = request.json
    has_user_and_pass = request_json["userid"] and request_json["pass"] and request_json["grade"]
    if not has_user_and_pass:
        return Response("you didn't give me the stuff you silly", status=400)

    user = request_json["userid"]
    password = request_json["pass"]
    grade = request_json["grade"]
    # START THE GOOGLE STUFF!!!!

    global google

    options = webdriver.ChromeOptions()
    options.headless = False
    app_state = {
        "recentDestinations": [
            {
                "id": "Save as PDF",
                "origin": "local"
            }
        ],
        "selectedDestinationId": "Save as PDF",
        "version": 2
    }

    if not os.path.exists(user + "_id"):
        os.mkdir("./" + user + "_id")

    profile = {'printing.print_preview_sticky_settings.appState': json.dumps(app_state),
               "download.default_directory": "C:\\Users\\ileik\\PycharmProjects\\IDGenerator\\" + user + "_id",
               "savefile.default_directory": "C:\\Users\\ileik\\PycharmProjects\\IDGenerator\\" + user + "_id",
               "download.directory_upgrade": True, }
    options.add_experimental_option('prefs', profile)
    options.add_argument('--kiosk-printing')
    google = webdriver.Chrome(service=Service(), options=options)
    google.get("https://login.katyisd.org/app/katyisd_mykatycloud_1/exk1dttjo5AcJmPwc697/sso/saml")
    google.implicitly_wait(5)

    username_field = google.find_element(By.ID, "input27")

    password_field = google.find_element(By.ID, "input35")
    next_button = google.find_element(By.CLASS_NAME, "button-primary")

    password_field.send_keys(password)

    username_field.send_keys(user)
    next_button.click()

    google.implicitly_wait(5)

    time.sleep(5)

    is_jhs_student = True
    name_holder = None
    try:
        name_holder = google.find_element(By.XPATH, "// span[contains(text(),\
'JHS')]")
    except Exception as e:
        print(e)
        is_jhs_student = False

    name_array = name_holder.text.replace(',', "").split()
    last_name = name_array[0]
    first_name = name_array[1]
    if not is_jhs_student:
        return Response("Only Jordan High School students have access to this service.", status=403)

    google.get("https://swinternalbiapps.katyisd.org/StudentIdBadge/Default.aspx".format(username=user, password=password))

    google.implicitly_wait(5)

    google.execute_script("document.title = '" + user + "_id'")
    google.execute_script("window.print()")
    time.sleep(5)
    # google.quit()

    id_badge = PdfReader(user + "_id/StudentIDBadge.pdf")
    for page in id_badge.pages:
        for image in page.images:
            with open(user + "_id/student_picture.jpg", "wb") as fp:
                fp.write(image.data)

    base_img = Image.open("ID_Template.png")

    try:
        pfp = Image.open(user + "_id/student_picture.jpg")
        pfp = pfp.resize((212, 265), PIL.Image.LANCZOS)
        base_img.paste(pfp, (186, 14))
    except FileNotFoundError:
        return Response("Your picture couldn't be found. You possibly have poor HTTP authentication, make sure your "
                        "username and password on MyKaty are synced", status=500)
    barcode_component = Image.new("RGBA", (320, 36), "white")
    base_img_draw = ImageDraw.Draw(barcode_component)
    barcode_font = ImageFont.truetype("./C39P12_3.ttf", 30)
    base_img_draw.text((0, 0), "*" + user + "*", font=barcode_font, fill=(0, 0, 0))
    barcode_component = barcode_component.resize((450, 60), PIL.Image.LANCZOS)
    base_img.paste(barcode_component, (20, 570))

    name_font = ImageFont.truetype("./angsa.ttf", 100)
    bold_font = ImageFont.truetype("./angsab.ttf", 64)
    # drawing all the little text stuff tee hee

    draw_text(base_img, font=name_font, color=(0, 0, 0), text=first_name.upper(), pos=(80, 312), size=(296, 71), center=False)
    draw_text(base_img, font=name_font, color=(0, 0, 0), text=last_name.upper(), pos=(80, 370), size=(296, 71), center=False)
    draw_text(base_img, font=bold_font, color=(0, 0, 0), text=str(grade), pos=(200, 438), center=False)
    draw_text(base_img, font=bold_font, color=(0, 0, 0), text=user.upper(), pos=(0, 640), center=True)

    # save image to file for sendoff

    buffered = BytesIO()
    base_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())

    Thread(target=delete_info(user)).start()

    return Response(response=img_str, status=200)


def draw_text(base_img: Image, font: ImageFont, color: tuple, text: str, pos: tuple, size: tuple = None, center=True):
    text_img = Image.new("RGBA", (800, 600), "white")
    text_draw = ImageDraw.Draw(text_img)
    text_size = text_draw.textbbox(xy=(0, 0), text=text, font=font)
    text_draw.text(xy=(0, 0), text=text, font=font, fill=color)
    text_img = text_img.crop(text_size)
    if size:
        multiplier = size[0] / text_img.size[0]
        if multiplier * text_img.size[1] > 54:
            print("Scaling by Y")
            multiplier = 54 / text_img.size[1]

        text_img = text_img.resize((round(multiplier * text_img.size[0]), round(multiplier * text_img.size[1])))

    if center:
        x_pos = int((460 - text_size[2]) / 2)
        y_pos = pos[1]
        base_img.paste(text_img, box=(x_pos, y_pos))
    else:
        base_img.paste(text_img, box=(pos[0], pos[1]))


def delete_info(id: str):
    os.remove(path="C:\\Users\ileik\PycharmProjects\IDGenerator\\"+id+"_id\student_picture.jpg")
    os.remove(path="C:\\Users\ileik\PycharmProjects\IDGenerator\\" + id + "_id\StudentIDBadge.pdf")
    os.rmdir(path="C:\\Users\ileik\PycharmProjects\IDGenerator\\" + id + "_id")

app.debug = True
app.run()
