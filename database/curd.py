import firebase_admin
from firebase_admin import credentials, db
from eventDetails import Event
from dataclasses import asdict

class FireBase:
    def __init__(self) -> None:
        cred = credentials.Certificate("database\\firebase_sdk.json")
        firebase_admin.initialize_app(
            cred,
            {"databaseURL": "https://eventhub-be9ba-default-rtdb.asia-southeast1.firebasedatabase.app/"}
            )
        self.database = db.reference()
        
    def addEvent(self, eventDetails: Event):
        event_count = self.database.child("LiveEvents").get() 
        update_event_count = event_count + 1
        self.database.update(
            {"LiveEvents": update_event_count}
        )
        self.database.child(f"Events/{update_event_count}").set(asdict(eventDetails))       
    
    def getEvent(self):
        return self.database.child("Events").get()