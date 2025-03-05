from quart import session

async def get_current_user():
  api_key = session.get('x-api-key')
  if not api_key:
    return None
  return api_key

async def get_current_admin():
  admin_key = session.get('admin_key')
  if not admin_key:
    return None
  return admin_key