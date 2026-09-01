# backend/core/roles.py
from enum import Enum

class Role(str, Enum):
    user = "user"
    coach = "coach"
    admin = "admin"
