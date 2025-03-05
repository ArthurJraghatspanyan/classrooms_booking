import secrets

async def generate_secret_code():
  secret_code = secrets.token_hex(6)
  return secret_code

async def generate_api_key():
  api_key = secrets.token_hex(6)
  return {"x-api-key": api_key}

async def generate_admin_key():
  admin_key = secrets.token_hex(6)
  return {"admin_key": admin_key}