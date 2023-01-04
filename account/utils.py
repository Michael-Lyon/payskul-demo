
import uuid


def get_code():
   return  str(uuid.uuid1())[:6]

