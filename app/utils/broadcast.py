from app.services.active_conn import admins_active_connections, students_active_connections

async def broadcast_to_admins(message: str):
  for conn in list(admins_active_connections):
    try:
      await conn.send_json(message)
    except:
      admins_active_connections.remove(conn)

from app.services.active_conn import students_active_connections

async def broadcast_to_students(message: str):
  for conn in list(students_active_connections):
    try:
      await conn.send_json(message)
    except:
      students_active_connections.remove(conn)