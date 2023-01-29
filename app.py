from flask import Flask, render_template, request, redirect, url_for
from eventDetails import Event
from database.curd import FireBase
from json import dumps

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

dummyEvent = Event(
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
)

@app.route("/")
@app.route("/liveEvents")
def liveEvents():
    #firebase.addEvent(dummyEvent)
    print(firebase.getEvent()[1:])
    return render_template("liveEvents.html", events=firebase.getEvent()[1:])

@app.route('/addEvent', methods=["GET","POST"])
def addEvent():
    if request.method == "POST":
        eventDetails = Event(
            club_name = request.form["club_name"],
            student1 = [request.form["student1_name"], request.form["student1_regno"], request.form["student1_mobile"]],
            student2 = [request.form["student2_name"], request.form["student2_regno"], request.form["student2_mobile"]],
            poster = request.form["poster"],
            event_name = request.form["event_name"],
            event_details = request.form["event_details"],
            register_before = request.form["register_before"],
            event_date = request.form["event_date"],
            event_time = request.form["event_time"],
            venue = request.form["venue"],
            od_details = request.form["od"]
            )
        firebase.addEvent(eventDetails)
        return redirect(url_for('liveEvents'))
    return render_template("eventDetails.html")

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
