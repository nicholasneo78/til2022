import base64
import numpy as np

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

def convert_arena(arena, toList = True):

    '''
    Parameters
    ----------
    arena : numpy array
        Original encoded string in base64 format

    toList : boolean
        

    Returns
    -------
    result : str
        Decoded string
    '''

    result = np.where(arena <= 0, 1, 0)

    if toList:
        return result.tolist()
    
    else:
        return result