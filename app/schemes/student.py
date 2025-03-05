from enum import Enum
from pydantic import BaseModel, Field, field_validator
from app.custom_exceptions.custom_errors import DataMissingError, LengthError

class Role(str, Enum):
  admin = 'admin'
  student = 'student'

class GroupName(str, Enum):
  python_odyssey = 'Python Odyssey'
  js_epic = 'JS Epic'
  cpp_synergy = 'C++ Synergy'
  ai = "Artifical Intelligence"

class StudentBase(BaseModel):
  username: str = Field(..., min_length=5)
  name: str = Field(..., min_length=3)
  surname: str = Field(..., min_length=3)
  group_name: GroupName = Field(default=GroupName.python_odyssey)
  role: Role = Field(default=Role.student)

  @field_validator('username', mode='before')
  @classmethod
  def username_validation(cls, value):
    if not value:
      raise DataMissingError(content={"Message": "Username data is missing"})
    if len(value) < 5:
      raise LengthError(content={"Message": "Username length must be greater than or equal 5"})

    return value

  @field_validator('name', mode='before')
  @classmethod
  def name_validation(cls, value):
    if not value:
      raise DataMissingError(content={"Message": "Name data is missing"}, status_code=400)
    if len(value) < 3:
      raise LengthError(content={"Message": "Name length must be greater than or equal 3"})

    return value

  @field_validator('surname', mode='before')
  @classmethod
  def surname_validation(cls, value):
    if not value:
      raise DataMissingError(content={"Message": "Surame data is missing"}, status_code=400)
    if len(value) < 3:
      raise LengthError(content={"Message": "Surname length must be greater than or equal 3"})

    return value

class StudentLogin(BaseModel):
  username: str = Field(..., min_length=5)
  secret_code: str = Field(...)

  @field_validator('username', mode='before')
  @classmethod
  def username_validation(cls, value):
    if not value:
      raise DataMissingError(content={"Message": "Username data is missing"})

    return value
  
  @field_validator('secret_code', mode='before')
  @classmethod
  def secret_code_validation(cls, value):
    if not value:
      raise DataMissingError(content={"Message": "Password data is missing"})

    return value

class StudentDelete(BaseModel):
  username: str = Field(..., min_length=5)

  @field_validator('username', mode='before')
  @classmethod
  def username_validation(cls, value):
    if not value:
      raise DataMissingError(content={"Message": "Username data is missing"})
    if len(value) < 5:
      raise LengthError(content={"Message": "Username length must be greater than or equal 5"})

    return value

class AdminLogin(BaseModel):
  admin_password: str = Field(...)

  @field_validator('admin_password', mode='before')
  @classmethod
  def password_validation(cls, value):
    if not value:
      raise DataMissingError(content={"Message": "Admin password data is missing"}, status_code=400)

    return value