import random
import string


def create_id(length):
    # combinación de letras y dígitos
    characters = string.ascii_letters + string.digits

    random_string = "".join(random.choice(characters) for _ in range(length))

    return random_string


def choose_capture_rate(capture_rates):
    tickets = []
    for key, value in capture_rates.items():
        tickets.extend([key] * value)

    return random.choice(tickets)
