class FileWriter:

  def __init__(self, filename):
    self.filename = filename

  def write(self, data):
   with open(self.filename, "w") as f:
    f.write(str(data))
