import uuid

def validate_add(model):
    """
    function to validate data to get added
    """

    msg = []

    if str(model.get('enabled', None)):
        if not str(model.get('enabled')) in ('True', 'true', 'False', 'false'):  # Given Mock data has false
            msg.append("Enabled Flag Invalid. Must be a boolean.")
    else:
        msg.append("Enabled Flag Missing.")

    if model.get('guid', None):
        if not (is_valid_uuid(model.get('guid'))):
            msg.append("Guid Invalid. Invalid UUID.")
    else:
        msg.append("Guid Missing.")

    if msg:
        return False, msg
    else:
        return True, msg

def is_valid_uuid(uuid_val, version=4):
    """
    Check if uuid_val is a valid UUID.
    """

    try:
        uuid_obj = uuid.UUID(uuid_val, version=version)
    except ValueError:
        return False

    return str(uuid_obj) == uuid_val
