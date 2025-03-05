from mongoengine import Document, StringField, EnumField

from app.schemes.student import Role, GroupName

class Student(Document):
  username = StringField(required=True, min_length=5)
  name = StringField(required=True, min_length=3)
  surname = StringField(required=True, min_length=3)
  group_name = EnumField(GroupName)
  role = EnumField(Role)
  secret_code = StringField(required=True)

  def to_dict(self):
    return {
      "username": self.username,
      "name": self.name,
      "surname": self.surname,
      "group_name": self.group_name.value if self.group_name else None,
      "role": self.role.value if self.role else None,
      "secret_code": self.secret_code
    }