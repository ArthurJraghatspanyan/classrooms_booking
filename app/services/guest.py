from quart import jsonify, request, session

from app.database.db_session import db
from app.config.settings import settings
from app.schemes.schedule import RoomName, RoomType
from app.schemes.student import StudentLogin, AdminLogin
from app.utils.api_and_secret import generate_api_key, generate_admin_key

class GuestService:
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
  async def student_login():
    data = await request.json
    if not data:
      return jsonify({"Message": "Data is missing"}), 400
    credentials = StudentLogin(**data)
    registered_student = await db.users.find_one({"username": credentials.username})
    if not registered_student:
      return jsonify({"Message": f"Student with {credentials.username} doesn't exist"}), 401
    if registered_student["secret_code"] != credentials.secret_code:
      return jsonify({"Message": "Invalid secret_code"}), 401
    api_key = await generate_api_key()
    session.update(api_key)

    return jsonify({"Message": "Logged in successfully"})
  
  @staticmethod
  async def admin_login():
    data = await request.json
    if not data:
      return jsonify({"Message": "Data is missing"}), 400
    admin_credentials = AdminLogin(**data)
    if admin_credentials.admin_password != settings.ADMIN_PASSWORD:
      return jsonify({"Message": "Invalid admin password"}), 401
    admin_key = await generate_admin_key()
    session.update(admin_key)

    return jsonify({"Message": "Logged in successfully"})