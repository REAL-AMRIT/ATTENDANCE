from configparser import ConfigParser

config = ConfigParser()

config['settings'] = {
    'secret_key': 'zzzzzzz11'
}

config['database'] = {
    'database_URI': 'mysql+pymysql://root:@localhost:3306/aps2'

}


with open('..//cfg.ini', 'w') as f:
    config.write(f)
