class TimeError(Exception):
  def __init__(self, content, status_code=400):
    self.content = content
    self.status_code = status_code

class DataMissingError(Exception):
  def __init__(self, content, status_code=400):
    self.content = content
    self.status_code = status_code

class LengthError(Exception):
  def __init__(self, content, status_code=400):
    self.content = content
    self.status_code = status_code