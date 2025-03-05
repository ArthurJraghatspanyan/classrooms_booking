import json
from quart import jsonify, request, websocket

from app.models.student import Student
from app.database.db_session import db
from app.utils.auth import get_current_admin
from app.models.schedule import Schedule, Room
from app.utils.broadcast import broadcast_to_students
from app.schemes.student import StudentBase, StudentDelete
from app.utils.api_and_secret import generate_secret_code
from app.services.notifications import student_data_notifications
from app.schemes.schedule import AdminDecision, AdminDecisionType
from app.schemes.schedule import RoomBase, RoomCancel, RoomName, RoomType

class AdminService:
  @staticmethod
  async def get_students():
    users = await db.users.find().to_list(length=None)
    if not users:
      return jsonify({"Message": "Students not found"}), 404
    for item in users:
      item['_id'] = str(item['_id'])

    return jsonify(users)

  @staticmethod
  async def create_student():
    is_admin = await get_current_admin()
    if not is_admin:
      return jsonify({"Message": "You don't have access"}), 403
    data = await request.json
    if not data:
      return jsonify({"Message": "Data is missing"}), 400
    student_schema = StudentBase(**data)
    existing_user = await db.users.find_one({"username": student_schema.username})
    if existing_user:
      return jsonify({"Message": "Student already exists"}), 400
    secret_code = await generate_secret_code()
    user_db = Student(**student_schema.model_dump(), secret_code = secret_code)
    await db.users.insert_one(user_db.to_dict())

    return jsonify({"Message": "Student created successfully"}), 201

  @staticmethod
  async def delete_student():
    is_admin = await get_current_admin()
    if not is_admin:
      return jsonify({"Message": "You don't have access"}), 403
    data = await request.json
    if not data:
      return jsonify({"Message": "Data is missing"}), 400
    student_delete_schema = StudentDelete(**data)
    user = await db.users.find_one({"username": student_delete_schema.username})
    if not user:
      return ({"Message": "User doesn't exist"}), 400
    await db.users.delete_one({"_id": user["_id"]})

    return jsonify({"Message": "User successfully deleted"}), 200

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
  async def booking_room():
    is_admin = await get_current_admin()
    if not is_admin:
      return jsonify({"Message": "You don't have access"}), 403
    data = await request.json
    if not data:
      return jsonify({"Message": "Data is missing"}), 400
    room_schema = RoomBase(**data)
    room_schema.start = room_schema.start.strftime("%Y-%m-%d %H:%M:%S")
    room_schema.end = room_schema.end.strftime("%Y-%m-%d %H:%M:%S")
    room_mapping = {
      RoomName.calling_room: RoomType.others, RoomName.darth_vader: RoomType.meeting_room,
      RoomName.proxima: RoomType.meeting_room, RoomName.recording_room: RoomType.others,
      RoomName.sirius: RoomType.meeting_room}
    existing_room = await db.schedule.find_one({
      "room.room_name": room_schema.room_name,
      "$or" : [
        {"start": {"$lt" : room_schema.end}, "end": {"$gt" : room_schema.start}}]
      })
    if existing_room:
      return jsonify({"Message": "Room is already busy"}), 400
    room_db = Schedule(
      room=Room(
      room_name=room_schema.room_name, room_type=room_mapping.get(room_schema.room_name, RoomType.classroom)),
      capacity=room_schema.capacity, start=room_schema.start, end=room_schema.end,
      group=room_schema.group, activity=room_schema.activity)
    await db.schedule.insert_one(room_db.to_dict())

    return jsonify(room_db.to_dict()), 201

  @staticmethod
  async def cancel_room():
    is_admin = await get_current_admin()
    if not is_admin:
      return jsonify({"Message": "You don't have access"}), 403
    data = await request.json
    if not data:
      return jsonify({"Message": "Data is missing"}), 400
    room_cancel_schema = RoomCancel(**data)
    room = await db.schedule.find_one({
      "room.room_name": room_cancel_schema.room_name,
      "room.room_type": room_cancel_schema.room_type,
      "start": room_cancel_schema.start
      })
    if not room:
      return jsonify({"Message": "Room doesn't exist"}), 404
    await db.schedule.delete_one(room)

    return jsonify({"Message": "Room schedule successfully cancelled"})
  
  @staticmethod
  async def admin_socket_conn():
    while True:
      message = await websocket.receive()
      try:
        message_dict = json.loads(message)
        decision_data = AdminDecision(**message_dict)
        booking_data = student_data_notifications
        if decision_data.decision == AdminDecisionType.rejection:
          await broadcast_to_students("Rejected")
          continue
        elif decision_data.decision == AdminDecisionType.confirmation:
          await broadcast_to_students("Confirmed")
          for details in booking_data:
            await db.schedule.insert_one(details)
            break
          student_data_notifications.clear()
      except:
        await websocket.send_json({"Message": "Invalid arguments"}), 400
        continue