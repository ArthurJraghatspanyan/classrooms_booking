from quart import jsonify, Blueprint
from app.services.guest import GuestService
from app.custom_exceptions.custom_errors import DataMissingError

guest_router = Blueprint('guest_router', __name__)

@guest_router.route('/rooms', methods=["GET"])
async def get_all_rooms():
  try:
    rooms = await GuestService.get_all_rooms()
    return rooms
  except Exception as e:
    return jsonify({"Error": str(e)})

@guest_router.route('/student_login', methods=["POST"])
async def student_login():
  try:
    result = await GuestService.student_login()
    return result
  except Exception as e:
    return jsonify({"Error": str(e)})

@guest_router.route('/admin_login', methods=["POST"])
async def admin_login():
  try:
    result = await GuestService.admin_login()
    return result
  except DataMissingError as e:
    return jsonify(e.content), e.status_code
  except Exception as e:
    return jsonify({"Error": str(e)})