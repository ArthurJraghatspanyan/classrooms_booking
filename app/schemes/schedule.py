from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field, model_validator, field_validator

from app.schemes.student import GroupName
from app.custom_exceptions.custom_errors import TimeError, DataMissingError, LengthError

class RoomName(str, Enum):
  ada_lovelace = "Ada Lovelace"
  alan_turing = "Alan Turing"
  calling_room = "Calling Room"
  claude_shannon = "Claude Shannon"
  darth_vader = "Darth Vader"
  donald_knuth = "Donald Knuth"
  library = "Library"
  proxima = "Proxima"
  recording_room = "Recording Room"
  sirius = "Sirius"
  william_shockley = "William Shockley"

class RoomType(str, Enum):
  classroom = "Classroom"
  meeting_room = "Meeting Room"
  others = "Others"

class Activity(str, Enum):
  lecture = "Lecture"
  practice = "Practice"
  exam = "Exam"
  teamwork = "Teamwork"
  other = "Other"

class AdminDecisionType(str, Enum):
  confirmation = "Confirm"
  rejection = "Reject"

class RoomBase(BaseModel):
  room_type: RoomType = Field(default=RoomType.classroom)
  room_name: RoomName = Field(default=RoomName.ada_lovelace)
  capacity: int = Field(..., gt=0, le=60)
  start: datetime = Field(...)
  end: datetime = Field(...)
  group: GroupName = Field(default=GroupName.python_odyssey)
  activity: Activity = Field(default=Activity.lecture)

  @field_validator('capacity', mode='before')
  @classmethod
  def capacity_validation(cls, value):

    if not value:
      raise DataMissingError(content={"Message": "Capacity data is missing"})
    
    if not 0 <= value < 60:
      raise LengthError(content={"Message": "Length of capacity is incorrect"})
    
    return value

  @model_validator(mode='before')
  @classmethod
  def start_end_validation(cls, values):
    start = values.get('start')
    end = values.get('end')
    
    if not start or not end:
      raise DataMissingError(content={"Message": "Date start or | and end data is missing"})

    if start >= end:
      raise TimeError(content={"Message": "Start is above the end or same as the end"})

    return values

class RoomCancel(BaseModel):
  room_name: RoomName = Field(default=RoomName.ada_lovelace)
  start: datetime = Field(...)
  end: datetime = Field(...)

  @model_validator(mode='before')
  @classmethod
  def start_end_validation(cls, values):
    start = values.get('start')
    end = values.get('end')

    if not start or not end:
      raise DataMissingError(content={"Message": "Date start or | and end data is missing"})

    if start >= end:
      raise TimeError(content={"Message": "Start is above the end or same as the end"})

    return values

class Notification(BaseModel):
  username: str = Field(..., min_length=5)
  room_type: RoomType = Field(default=RoomType.classroom)
  room_name: RoomName = Field(default=RoomName.ada_lovelace)
  capacity: int = Field(..., gt=0, le=60)
  start: datetime = Field(...)
  end: datetime = Field(...)
  group: GroupName = Field(default=GroupName.python_odyssey)
  activity: Activity = Field(default=Activity.lecture)

  @field_validator('username', mode='before')
  @classmethod
  def username_validation(cls, value):
    if not value:
      raise DataMissingError(content={"Message": "Username data is missing"})
    if len(value) < 5:
      raise LengthError(content={"Message": "Username length must be greater than or equal 5"})

    return value
  
  @field_validator('capacity', mode='before')
  @classmethod
  def capacity_validation(cls, value):

    if not value:
      raise DataMissingError(content={"Message": "Capacity data is missing"})
    
    if not 0 <= value < 60:
      raise LengthError(content={"Message": "Length of capacity is incorrect"})
    
    return value

  @model_validator(mode='before')
  @classmethod
  def start_end_validation(cls, values):
    start = values.get('start')
    end = values.get('end')
    
    if not start or not end:
      raise DataMissingError(content={"Message": "Date start or | end end data is missing"})
    
    if start >= end:
      raise TimeError(content={"Message": "Incorrect start and time"})
    
    return values

class AdminDecision(BaseModel):
  decision: AdminDecisionType = Field(...)