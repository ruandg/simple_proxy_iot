# Command structure constants

CMD_REQ = {
    'UCID': 0,
    'COMMAND': '',
    'PARAMETERS': {}
}

CMD_RES = {
    'UCID': 0,
    'RESULT': '',
    'RETURN': {}
}

# LST command constants

CMD_LST_COMMAND = 'LST'
CMD_LST_PARAMETERS = {
    'STATUS': ''
}
CMD_LST_STATUS_ON = 'ON'
CMD_LST_STATUS_OFF = 'OFF'
CMD_LST_STATUS_ALL = 'ALL'
CMD_LST_STATUS = [
    CMD_LST_STATUS_ON, 
    CMD_LST_STATUS_OFF, 
    CMD_LST_STATUS_ALL
]

# OPEN command constants

CMD_OPEN_COMMAND = 'OPEN'
CMD_OPEN_PARAMETERS = {
    'UUID': ''
}

# PING command constants

CMD_PING_COMMAND = 'PING'
