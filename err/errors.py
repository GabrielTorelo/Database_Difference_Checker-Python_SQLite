from constants import TRACKING_CODE


class Errors(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

    def get_response(self):
        return {
            "trackingCode": f"{TRACKING_CODE}.{str(self.get_code).zfill(2)}",
            "message": self.get_message
        }

    @property
    def get_code(self):
        return self.__code

    @get_code.setter
    def code(self, code: int):
        self.__code = code

    @property
    def get_message(self):
        return self.__message
    
    @get_message.setter
    def message(self, message: str):
        self.__message = message
