#Base exception
class AnimalException(Exception):
    pass


#Raised when an animal is not found
class AnimalNotFoundException(AnimalException):
    pass

#Raised when trying to add a duplicate animal
class AnimalAlreadyExistsException(AnimalException):
    pass
