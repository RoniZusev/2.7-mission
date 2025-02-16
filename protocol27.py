#   Ex. 2.7 template - protocol


LENGTH_FIELD_SIZE = 1024
PORT = 8820


def check_cmd(data):
    data = data.upper()
    """Check if the command is defined in the protocol (e.g RAND, NAME, TIME, EXIT)"""
    if str(data).startswith("DIR") == False and str(data).startswith("DELETE") == False and str(data).startswith("COPY") == False and str(data).startswith("EXECUTE") == False and str(data) != "TAKE_SCREENSHOT" and data != "SEND_PHOTO":
        return False
    return True


def create_msg(data):
    """Create a valid protocol message, with length field"""
    length = len(data)
    if length > 99:
        return "invalid message"
    if length > 0 and length < 10:
        return str(0) +str(length) + data
    return str(length) + data


def get_msg(my_socket):
    """Extract message from protocol, without the length field.
        If length field does not include a number, returns False, "Error". """
    data = my_socket.recv(2).decode()
    data2 = my_socket.recv(int(data)).decode()
    if str(data).isalpha() == True:
        return False, "Error"
    else:
        return True, data2

