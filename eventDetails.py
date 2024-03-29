from dataclasses import dataclass

@dataclass(frozen=True, order=True)
class Event:
    club_name: str
    club_email: str
    poster: str
    event_name: str
    event_details: str
    register_before: str 
    event_date: str
    event_time: str
    venue: str
    od_details: str
    register_link: str
    contact: str
    insta: str
    website: str
    fb: str
    twitter: str
    id: str
    
if __name__ == '__main__':
    Event()