import random

def create_user_name(first_name, last_name):
    user_name = first_name + '_' + last_name
    user_name = user_name.lower()
    user_name = user_name + '_' + str(random.randint(1,99999))
    return user_name