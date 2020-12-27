import os
import Config


def get_user_name():
    if Config.USER_NAME != "":
        return Config.USER_NAME
    elif os.environ.get("USER_NAME"):
        return os.environ.get("USER_NAME")
    return ""

def get_password():
    if Config.PASSWORD != "":
        return Config.PASSWORD
    elif os.environ.get("PASSWORD"):
        return os.environ.get("PASSWORD")
    return ""


