def prepare_creds(db_creds:dict) -> dict :
    new_creds = {}
    for key, value in db_creds.items():
        if key in ['host','username','password','db_name','port','db_type']:
            if key == 'db_name':
                new_creds['db'] = value
            new_creds[key] = value
    return new_creds

