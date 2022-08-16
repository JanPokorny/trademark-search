import environ

@environ.config(prefix='POSTGRES')
class PostgresConfig:
    USER = environ.var()
    PASSWORD = environ.var()
    DB = environ.var()
    HOST = environ.var()
