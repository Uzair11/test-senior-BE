def prepare_creds(db_creds:dict) -> dict :
    new_creds = {}
    for key, value in db_creds.items():
        if key in ['host','username','password','db_name','port','db_type']:
            if key == 'db_name':
                new_creds['database'] = value
                continue
            elif key == 'username':
                new_creds['user'] = value
                continue
            new_creds[key] = value
    return new_creds

