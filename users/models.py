from django.db import models
from db_collection import db

user_collection = db['users']
reset_token_collection = db['password_reset_tokens']