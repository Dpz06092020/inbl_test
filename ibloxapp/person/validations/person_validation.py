from person.validations import person_data_validation

def validate_add(model):
    """
    function to validate data to get added
    """

    msg = []
    if model.get('id', None):
        if not isinstance(model.get('id'), int):
            msg.append("ID Invalid. Must be an Integer.")
    else:
        msg.append("ID Missing.")

    if model.get('first_name', None):
        if not isinstance(model.get('first_name'), str):
            msg.append("First Name Invalid. Must be a String.")
    else:
        msg.append("First Name Missing.")

    if model.get('last_name', None):
        if not isinstance(model.get('last_name'), str):
            msg.append("Last Name Invalid. Must be a String.")
    else:
        msg.append("Last Name Missing.")

    if model.get('city', None):
        if not isinstance(model.get('city'), str):
            msg.append("City Invalid. Must be a String.")
    else:
        msg.append("City Missing.")

    if model.get('data', None):
        person_data_validation_msg = person_data_validation.validate_add(model.get('data')[0])
        if not person_data_validation_msg[0]:
            msg.append(person_data_validation_msg[1])
    else:
        msg.append("Data Missing.")

    if msg:
        return False, msg
    else:
        return True, msg
