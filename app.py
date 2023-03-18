from flask import Flask, render_template, request, redirect, url_for
from eventDetails import Event
from database.curd import FireBase
from random import randint
import smtplib, ssl
from dataclasses import asdict

app = Flask(__name__)
firebase = FireBase()

posts = [
    {
        "club_name": "Codezilla",
        "event_name": "Hackathon",
        "event_details": "Coding competion",
        "register_before": "30/01/2023"
    },
    {
        "club_name": "Codezilla",
        "event_name": "Hackathon",
        "event_details": "Coding competion",
        "register_before": "30/01/2023"
    }
]

"""dummyEvent = Event(
    "Codezilla",
    ["Abhilash", "RA2111003020423", "7358482354"],
    ["Abhilash", "RA2111003020423", "7358482354"],
    "image",
    "Hackathon",
    "Coding Competion",
    "02/02/2023",
    "05/02/2023",
    "5:00",
    "Auditorium",
    "No OD sry!"
)"""

@app.route("/")
@app.route("/liveEvents")
def liveEvents():
    #firebase.addEvent(dummyEvent)
    print(type(firebase.getEvents()))
    return render_template("liveEvents.html", events=firebase.getEvents())

@app.route('/addEvent', methods=["GET","POST"])
def getEvent():
    if request.method == "POST":
        #image = request.form.get("poster", False)
        eventDetails = Event(
            club_name = request.form["club_name"],
            poster = "no image",
            event_name = request.form["event_name"],
            event_details = request.form["event_details"],
            register_before = request.form["register_before"],
            event_date = request.form["event_date"],
            event_time = request.form["event_time"],
            venue = request.form["venue"],
            od_details = request.form["od"]
            )
        #firebase.addEvent(eventDetails)
        print("\n---------------------------------------------------------")
        print(asdict(eventDetails))
        print("\n---------------------------------------------------------")
        return redirect(url_for('deletePin', event = asdict(eventDetails)))
    return render_template("getEvent.html")

@app.route('/eventDetails')
def eventDetails():
    event = firebase.getEvent("2")
    return render_template("eventDetails.html", event=event)

@app.route('/deletePin', methods=["GET","POST"])
def deletePin():
    pin = randint(1111, 9999)
    if request.method == "POST":
        event = request.args.get("event")
        firebase.addEvent(eval(event), pin)
        return redirect(url_for('liveEvents'))
        
    return render_template("deletePin.html", pin=pin)

if __name__ == "__main__":
    app.run(debug=True)
