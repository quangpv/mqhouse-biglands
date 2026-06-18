import random
import string
from datetime import datetime


def generate_product_code() -> str:
    date_part = datetime.now().strftime("%y%m%d")
    random_part = "".join(random.choices(string.digits, k=7))
    return f"{date_part}{random_part}"
