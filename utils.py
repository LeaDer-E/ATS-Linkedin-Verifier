# utils.py
import re
import time
from functools import wraps
from logging import Logger

# Regex for extracting phone numbers
PHONE_REGEX = re.compile(
    r"(\+966\s?\d{1,3}\s?\d{3}\s?\d{3,4}|\+966\s?0?\d{9}|\b0\d{9}\b|\b0\d{2}\s?\d{3}\s?\d{4})"
)

import re

PHONE_REGEX = re.compile(
    r"(?:\+966|\(?\+966\)?|0)?[\s-]*5(?:[\s-]*\d){8}"
)

def extract_phone_from_text(text_lines):
    """
    Extracts the first valid Saudi phone number from the first 5 lines.
    Normalizes the number to +966XXXXXXXXX format.
    """
    for line in text_lines[:5]:
        match = PHONE_REGEX.search(line)
        if match:
            raw = match.group()
            # Remove spaces, dashes, parentheses
            phone = re.sub(r"[^\d+]", "", raw)

            # Normalize
            if phone.startswith("05"):  # local format
                phone = "+966" + phone[1:]
            elif phone.startswith("5"):  # missing 0
                phone = "+966" + phone
            elif phone.startswith("+9660"):  # wrong extra 0
                phone = "+966" + phone[5:]
            elif phone.startswith("(+966)"):  # with parentheses
                phone = "+966" + phone[5:]

            # Validation: لازم يكون 13 خانة مع +966
            digits = re.sub(r"\D", "", phone)
            if len(digits) == 12:  # 966 + 9 digits
                return phone
    return None



def timing(logger: Logger):
    """
    Decorator to measure execution time of functions and log it.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            elapsed = end - start
            logger.info(f"Function '{func.__name__}' executed in {elapsed:.2f} seconds")
            return result
        return wrapper
    return decorator