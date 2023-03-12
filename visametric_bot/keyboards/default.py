from ..constants import ADDRESS_OPTIONS, NATIONALITY_OPTIONS


def get_address_keyboards(get_nationality=False):
    objects = []
    if get_nationality:
        for object in NATIONALITY_OPTIONS:
            objects.append([{"text": object[0]}])
    else:
        for object in ADDRESS_OPTIONS:
            objects.append([{"text": object[0]}])
        
    return {
        "keyboard":objects,
        "one_time_keyboard": True,
        "resize_keyboard": True
    }
