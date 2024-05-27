import string
import random



def generate_short_url(size=7) -> str:
    letters = string.ascii_letters + string.digits
    short_tag = ''.join(random.choice(letters) for i in range(size))
    return short_tag