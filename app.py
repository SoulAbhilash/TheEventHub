# in - built libraries
from dataclasses import asdict
from random import randint

# installed
from flask import Flask, jsonify, redirect, render_template, request, url_for, session
import logging
from logging.handlers import RotatingFileHandler

# My classes
from database.curd import FireBase
from emails.emailManger import EmailManger
from eventDetails import Event

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key_here'
firebase = FireBase()
emailManager = EmailManger()

app.logger.setLevel(logging.DEBUG)

# Add a rotating file handler to log to a file
handler = RotatingFileHandler('myapp.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)

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
@app.route("/liveEvents", methods=["GET", "POST"])
def liveEvents():
    live_events = firebase.getEvents()
    if request.method == "POST":
        id = request.form.get('cardId')
        delete = firebase.deleteEvetn(id)
        print(delete)
        return redirect(url_for('liveEvents', events=live_events))
    return render_template("liveEvents.html", events=live_events)


@app.route('/addEvent', methods=["GET", "POST"])
def addEvent():
    eventCreated = False
    session['event_created'] = False
    if request.method == "POST":
        eventCreated = True
        poster_file = request.files["poster"]
        imgUrl = firebase.generatePosterUrl(upload_file= poster_file)
        id = str(randint(1111, 9999))
        eventDetails = Event(
            club_name=request.form["club_name"],
            club_email=request.form["club_email"],
            poster=imgUrl,
            event_name=request.form["event_name"],
            event_details=request.form["event_details"],
            register_before=request.form["register_before"],
            event_date=request.form["event_date"],
            event_time=request.form["event_time"],
            venue=request.form["venue"],
            od_details=request.form["od"],
            register_link=request.form["register_link"],
            contact=request.form["contact"],
            insta=request.form["insta"],
            website=request.form["web"],
            fb=request.form["fb"],
            twitter=request.form["twitter"],
            id = id
        )
        
        firebase.addEvent( asdict(eventDetails), id) 
        return redirect(
            url_for(
                'eventCreated',
                pin=id,
                eventCreated=eventCreated,
                email=eventDetails.club_email,
                eventDetails=asdict(eventDetails)
            )
        )
    return render_template("getEvent.html")


@app.route('/eventDetails/<id>', methods=["GET", "POST"])
def eventDetails(id):
    event = firebase.getEvent(id)
    return render_template("eventDetails.html", event=event)


@app.route('/eventCreated', methods=["GET", "POST"])
def eventCreated():
    if(request.args.get("eventCreated") and (not session.get('event_created', False))):
        
        session['event_created'] = True
        pin = request.args.get("pin")
        eventDetails = eval(request.args.get("eventDetails"))
        
        emailManager.sendSucessfullMail(
            reciever=eventDetails["club_email"],
            deleteCode=pin,
            userName=eventDetails["club_name"]
        )
        return render_template("eventCreated.html", pin=pin)
    return redirect(url_for("liveEvents"))


@app.route('/resendCode', methods=["GET", 'POST'])
def resendCode():
    id = request.form.get('cardId')
    details = firebase.getEvent(id)
    emailManager.resendCodeRequest(
        reciever=details["club_email"],
        deleteCode=id,
        userName=details["club_name"]
    )
    return jsonify({'message': 'Code resent successfully'})

@app.route('/editEvent', methods=['GET', 'POST'])
def editEvent():
    id = request.form.get('cardId')
    details = firebase.getEvent(str(id))
    print(id , details['id'])
    if str(details['id']) == str(id):
        print("hi")
        return render_template("editEvent.html", event = details)
    return jsonify({'message': 'Code resent successfully'})

if __name__ == "__main__":
    app.run(debug=True)
