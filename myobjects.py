class People:
    def __init__(self, id, name, isInstructor, password):
        self.id = id
        self.name = name
        self.isInstructor = isInstructor
        self.password = password


class Assignment:
    def __init__(self, id, name, files, max_point, grades):
        self.id = id
        self.name = name
        self.files = files
        self.max_point = max_point
        self.grades = grades


class File:
    def __init__(self, fileID, location):
        self.location = location
        self.fileID = fileID

