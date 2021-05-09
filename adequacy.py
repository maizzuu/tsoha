from string import ascii_letters

def check_username(username):
    for character in username:
        if character not in ascii_letters:
            if character not in "0123456789":
                return False
    return True

def check_password(password):
    big = False
    for character in password:
        if character in "0123456789":
            big = True
        if character not in ascii_letters:
            if character not in "0123456789":
                return False
    if not big:
        return False
    return True

def check_date(date):
    parts = date.split("-")
    y = parts[0]
    try:
        y = int(y)
    except ValueError:
        return False
    d = parts[2]
    try:
        d = int(d)
    except ValueError:
        return False
    m = parts[1]
    try:
        m = int(m)
    except ValueError:
        return False
    if not 2020 <= y <= 2100:
        return False
    if not 1 <= m <= 12:
        return False 
    if m in [1, 3, 5, 7, 8, 10, 12]:
        if not 1 <= d <= 31:
            return False
    elif m in [4, 6, 9, 11]:
        if not 1<= d <= 30:
            return False
    elif m == 2:
        if not 1<= d <= 28:
            return False
    return True
    
def check_time(time):
    parts = time.split(":")
    h = parts[0]
    if len(h)>2:
        return False
    try:
        h = int(h)
    except ValueError:
        return False
    m = parts[1]
    try:
        m = int(m)
    except ValueError:
        return False
    if not 0<= h <= 23:
        return False
    if not 0<= m <= 59:
        return False
    return True

