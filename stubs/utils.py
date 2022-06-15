import base64

def decode_str(string):

    '''
    Parameters
    ----------
    string : str
        Original encoded string in base64 format

    Returns
    -------
    message : str
        Decoded string

    '''

    base64_message = string
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')

    return message