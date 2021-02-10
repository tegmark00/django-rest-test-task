import requests
from typing import Union
from faker import Faker

from app.config import *
from app.user import User


class Bot:

    def __init__(self):
        self.fake = Faker()

    @staticmethod
    def make_request(endpoint: str, data: Union[None, dict] = None):
        response = requests.post(endpoint, data=data)
        return response

    @staticmethod
    def make_auth_request(user: User, endpoint: str, data: Union[dict, None] = None):
        headers = {'Authorization': 'Bearer ' + user.token}
        response = requests.post(endpoint, data=data, headers=headers)
        return response

    def generate_userdata(self) -> dict:
        return {
            'email': self.fake.email(),
            'first_name': self.fake.name().split(' ')[0],
            'last_name': self.fake.name().split(' ')[1],
            'password': USER_DEFAULT_PASSWORD
        }

    def generate_post(self):
        return {
            'text': self.fake.text()
        }

    def create_user(self, userdata: dict):
        return self.make_request(API_ENDPOINT_SIGNUP, userdata)

    def login_user(self, creds: dict):
        return self.make_request(API_ENDPOINT_LOGIN, creds)

    def add_post(self, user: User, post: dict):
        return self.make_auth_request(user, API_ENDPOINT_ADD_POST, post)

    def like_post(self, user: User, post_id: int):
        return self.make_auth_request(user, API_ENDPOINT_LIKE_POST + str(post_id) + '/')
