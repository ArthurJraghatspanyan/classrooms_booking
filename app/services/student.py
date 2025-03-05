import json
import aiohttp
from quart import jsonify, request, websocket

from app.database.db_session import db
from app.config.settings import settings
from app.schemes.schedule import Notification
from app.models.schedule import Room, Schedule
from app.schemes.schedule import RoomType, RoomName
from app.utils.broadcast import broadcast_to_admins
from app.services.notifications import student_data_notifications

class StudentService:
  @staticmethod
  async def get_all_rooms():
    filtration = {}
    room_type = request.args.get("room_type")
    room_name = request.args.get("room_name")
    if room_type is not None:
      if chr(32) in room_type:
        return jsonify({"Message": "Clear spaces in query"}), 400
      if room_type not in RoomType.__members__:
        return jsonify({"Message": "Room type doesn't exist"}), 400
      filtration['room.room_type'] = room_type.replace(room_type, RoomType.__members__[room_type])
    if room_name is not None:
      if chr(32) in room_name:
        return jsonify({"Message": "Clear spaces in query"}), 400
      if room_name not in RoomName.__members__:
        return jsonify({"Message": "Room name doesn't exist"}), 400
      filtration['room.room_name'] = room_name.replace(room_name, RoomName.__members__[room_name])
    rooms = await db.schedule.find(filtration, {"_id": 0}).to_list(length=None)
    if not rooms:
      return jsonify({"Message": "No rooms available"}), 404

    return jsonify(rooms)

  @staticmethod
  async def student_socket_conn():
    while True:
      student_message = await websocket.receive()
      try:
        message_dict = json.loads(student_message)
        data = Notification(**message_dict)
        data.start = data.start.strftime("%Y-%m-%d %H:%M:%S")
        data.end = data.end.strftime("%Y-%m-%d %H:%M:%S")
        valid_username = await db.users.find_one({"username": data.username})
        if not valid_username:
          await websocket.send_json({"Message": "There is no user with current username"}), 400
          continue
        existing_room = await db.schedule.find_one({
          "room.room_name": data.room_name,
          "$or" : [
            {"start": {"$lt" : data.end}, "end": {"$gt" : data.start}}]
          })
        if existing_room:
          await websocket.send_json({"Message": "Room is already busy"}), 400
          continue
        room_mapping = {
          RoomName.calling_room: RoomType.others, RoomName.darth_vader: RoomType.meeting_room,
          RoomName.proxima: RoomType.meeting_room, RoomName.recording_room: RoomType.others,
          RoomName.sirius: RoomType.meeting_room}
        room_db = Schedule(
          room=Room(
          room_name=data.room_name, room_type=room_mapping.get(data.room_name, RoomType.classroom)),
          capacity=data.capacity, start=data.start, end=data.end,
          group=data.group, activity=data.activity)
        await broadcast_to_admins(f"There is a booking request: {room_db.to_dict()}")
        student_data_notifications.append(room_db.to_dict())
      except:
        await websocket.send_json({"Message": "Invalid arguments"}), 400
        continue

  @staticmethod
  async def send_notification():
    async with aiohttp.ClientSession() as client_session:
      async with client_session.post(
        "http://slack.com/api/chat.postMessage",
        headers={"Authorization": f"Bearer: {settings.SLACK_TOKEN}"},
        json={
          "channel": "#python-odyssey",
          "text": "Welcome to Classroom"
        }) as response:
        if response.status == 200:
          response_data = await response.json()
          if response_data.get("ok"):
            return jsonify({"Message": "Message sent successfully"})
          else:
            error_message = response_data.get("Message", "Unknown error")
            return jsonify({"Message": f"Slack API Error: {error_message}"}), 400
        else:
          error_response = await response.json()
          return jsonify({"Message": f"Failed to send message: {error_response}"}), 400