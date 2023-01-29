from dataclasses import dataclass

@dataclass(frozen=True, order=True)
class Event:
    club_name: str
    student1: list[str]
    student2: list[str]
    poster: str
    event_name: str
    event_details: str
    register_before: str 
    event_date: str
    event_time: str
    venue: str
    od_details: str
    