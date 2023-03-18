import firebase_admin
from firebase_admin import credentials, db, storage
from eventDetails import Event

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
        
    def addEvent(self, eventDetails: dict, eventId: int):
        #self.__storeImage(eventDetails.poster)
        # print("----------------------------------------------------")
        # print(eventDetails)
        self.eventDatabase.child(f"{eventId}").set(eventDetails)      
    
    def getEvents(self):
        print("\n[Getting Events]")
        print(self.eventDatabase.get())
        return self.eventDatabase.get()
    
    # def __storeImage(self, filepath):
    #     blob = self.bucket.blob(filepath)
    #     blob.upload_from_filename(filepath)
        
    def getEvent(self, id):
        return self.eventDatabase.child("Events").child(id).get()