from quart import Blueprint, jsonify, session, websocket

from app.services.admin import AdminService
from app.services.active_conn import admins_active_connections
from app.custom_exceptions.custom_errors import TimeError, DataMissingError, LengthError

admin_router = Blueprint('admin_router', __name__, url_prefix='/admin')

@admin_router.route('/logout', methods=["GET"])
async def logout_user():
  session.clear()
  return jsonify({"Message": "Successfully logged out"})

@admin_router.route('/students', methods=["GET"])
async def get_students():
  try:
    students = await AdminService.get_students()
    return students
  except Exception as e:
    return jsonify({"Message": str(e)})

@admin_router.route('/students/create_student', methods=["POST"])
async def create_student():
  try:
    new_student = await AdminService.create_student()
    return new_student
  except DataMissingError as e:
    return jsonify(e.content), e.status_code
  except Exception as e:
    return jsonify({"Message": str(e)})

@admin_router.route('/students/delete_student', methods=["DELETE"])
async def delete_student():
  try:
    delete_student = await AdminService.delete_student()
    return delete_student
  except Exception as e:
    return jsonify({"Message": str(e)})

@admin_router.route('/rooms', methods=["GET"])
async def get_all_rooms():
  try:
    rooms = await AdminService.get_all_rooms()
    return rooms
  except Exception as e:
    return jsonify({"Error": str(e)})

@admin_router.route('/rooms/book_room', methods=["POST"])
async def booking_room():
  try:
    room = await AdminService.booking_room()
    return room
  except DataMissingError as e:
    return jsonify(e.content), e.status_code
  except LengthError as e:
    return jsonify(e.content), e.status_code
  except TimeError as e:
    return jsonify(e.content), e.status_code
  except Exception as e:
    return jsonify({"Message": str(e)})

@admin_router.route('/rooms/cancel_room', methods=["DELETE"])
async def cancel_room():
  try:
    room = await AdminService.cancel_room()
    return room
  except Exception as e:
    return jsonify({"Error": str(e)})

@admin_router.websocket('/connection')
async def admin_socket_conn():
  conn = websocket._get_current_object()
  admins_active_connections.add(conn)
  try:
    admin_socket = await AdminService.admin_socket_conn()
    return admin_socket
  except DataMissingError as e:
    return await websocket.send_json(e.content), e.status_code
  except LengthError as e:
    return await websocket.send_json(e.content), e.status_code
  except TimeError as e:
    return await websocket.send_json(e.content), e.status_code
  except Exception as e:
    return jsonify({"Error": str(e)})
  finally:
    admins_active_connections.remove(conn)