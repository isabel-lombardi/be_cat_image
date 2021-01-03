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
        symbols = ['?','#','$','%','@','.',",","_","-",'+']
        if len(login_data['password']) < 6:
            return False
        if not any(c in symbols for c in login_data['password']):
            return False
        if not any(char.isupper() for char in login_data['password']): 
            return False
        if not any(char.isdigit() for char in login_data['password']):
            return False
        else:
            return True

    @staticmethod
    def is_images_number_valid(image_data):
        if len(image_data) > 10:
            return False
        return True

    @staticmethod
    def images_format_validation(decoded_images: dict) -> list:
        """If the format of some images is wrong it returns the ids of the wrong images,
        otherwise, if everything is ok, return empty list

        :param decoded_images:
        :return: list of id of wrong images
        """
        wrong_images_id = []
        for key in decoded_images:
            if not decoded_images[key].format in ['JPEG', 'PNG']:
                # print(decoded_images[idx].format)
                wrong_images_id.append(key)
        return wrong_images_id

    @staticmethod
    def is_json_login_data_valid(login_data: dict) -> bool:
        """Check if the username and password keys exist in the json

        :param login_data:
        :return: bool
        """
        for key in ['username', 'password']:
            if key not in login_data:
                return False
        return True

    @staticmethod
    def is_json_images_data_valid(images_data: dict) -> bool:
        """Check that the json keys are integers

        :param images_data:
        :return: bool
        """
        for key in images_data:
            if not key.isdigit():
                return False
        return True
