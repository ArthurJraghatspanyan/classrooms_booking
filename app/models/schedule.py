from mongoengine import Document, EnumField, EmbeddedDocument, EmbeddedDocumentField, IntField, DateTimeField

from app.schemes.student import GroupName
from app.schemes.schedule import RoomName, RoomType, Activity

class Room(EmbeddedDocument):
  room_type = EnumField(RoomType, required=True)
  room_name = EnumField(RoomName, required=True)

class Schedule(Document):
  room = EmbeddedDocumentField(Room)
  capacity = IntField(required=True)
  start = DateTimeField(required=True)
  end = DateTimeField(required=True)
  group = EnumField(GroupName, required=True)
  activity = EnumField(Activity, required=True)

  def to_dict(self):
    return {
      "room": {
        "room_type": self.room.room_type,
        "room_name": self.room.room_name,
      },
      "capacity": self.capacity,
      "start": self.start,
      "end": self.end,
      "group": self.group,
      "activity": self.activity
    }