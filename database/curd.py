import firebase_admin
from firebase_admin import credentials, db, storage
from eventDetails import Event
import datetime

class FireBase:
    def __init__(self) -> None:
        cred = credentials.Certificate("database\\firebase_sdk.json")
        firebase_admin.initialize_app(
            cred,
            {
                "databaseURL": "https://eventhub-be9ba-default-rtdb.asia-southeast1.firebasedatabase.app/",
                "storageBucket": "eventhub-be9ba.appspot.com"
                }
            )
        self.eventDatabase = db.reference("Events")
        self.bucket = storage.bucket()
        
    def generatePosterUrl(self, upload_file):
        blob = self.bucket.blob(upload_file.filename)
        blob.upload_from_string(
            upload_file.read(),
            content_type=upload_file.content_type
        )
        
        return blob.generate_signed_url(expiration=datetime.timedelta(hours=1), method='GET')
        
    def addEvent(self, eventDetails: dict, eventId: int):
        self.eventDatabase.child(f"{eventId}").set(eventDetails)   
        return "Event added"   
    
    def getEvents(self):
        return self.eventDatabase.get()
        
    def getEvent(self, id):
        return self.eventDatabase.child(id).get()
    
    def deleteEvetn(self, id):
        self.eventDatabase.child(id).delete()
        return "Event Deleted"

if __name__ == "__main__":
    FireBase()