from database.database import database


def get_user_by_name(user: 'str'):
    userdata = next(
        filter(
            lambda item: item['username'] == user, 
            database['users']
        ),
        None
    )

    return userdata


def check_user(user: 'str', password: 'str') -> 'bool':
    userdata = get_user_by_name(user)
    
    return (userdata and (userdata['password'] == password))
