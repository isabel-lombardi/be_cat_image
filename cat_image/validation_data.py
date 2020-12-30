from re import search
class ValidationData:
    @staticmethod
    def is_username_valid(login_data: dict):
        regex = '^[a-z0-9A-Z]+[\._]?[a-z0-9A-Z]+[@]\w+[.]\w{2,3}$'
        if search(regex, login_data["username"]):
            return True
        elif len(login_data["username"]) >= 4 or len(login_data["username"]) <= 10:
            return True
        else:
            return False

    @staticmethod
    def is_password_valid(login_data: dict):
        return True

    @staticmethod
    def is_images_number_valid():
        return True

    @staticmethod
    def is_images_format_valid():
        pass
