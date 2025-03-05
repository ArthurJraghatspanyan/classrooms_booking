import aiohttp
from quart import Blueprint, jsonify, session, websocket

from app.services.student import StudentService
from app.services.active_conn import students_active_connections
from app.custom_exceptions.custom_errors import TimeError, DataMissingError, LengthError

student_router = Blueprint('student_router', __name__, url_prefix='/student')

@student_router.route('/logout', methods=["GET"])
async def logout_user():
  session.clear()
  return jsonify({"Message": "Successfully logged out"})

@student_router.route('/rooms', methods=["GET"])
async def get_all_rooms():
  try:
    rooms = await StudentService.get_all_rooms()
    return rooms
  except Exception as e:
    return jsonify({"Error": str(e)})

@student_router.route('/send-notification', methods=["POST"])
async def send_notification():
  try:
    notification = await StudentService.send_notification()
    return notification
  except aiohttp.ClientError as e:
    return jsonify({"Message": f"Error, while sending message: {e}"}), 500
  except Exception as e:
    return jsonify({"Message": f"Unexpected error: {e}"}), 500

@student_router.websocket('/connection')
async def student_socket_conn():
  conn = websocket._get_current_object()
  students_active_connections.add(conn)
  try:
    booking_notification = await StudentService.student_socket_conn()
    return booking_notification
  except DataMissingError as e:
    await websocket.send_json(e.content), e.status_code
  except LengthError as e:
    await websocket.send_json(e.content), e.status_code
  except TimeError as e:
    await websocket.send_json(e.content), e.status_code
  except Exception as e:
    await websocket.send_json({"Message": f"Error with WebSocket connection: {str(e)}"}), 500
  finally:
    students_active_connections.remove(conn)