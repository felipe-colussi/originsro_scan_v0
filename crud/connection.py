import psycopg2


def connect():
    """Conecta ao servidor - DATABASE """
    try:
        conn = psycopg2.connect(
            database='origins_ro_v2',
            host='localhost',
            user='origins_project',
            password='13524500'
        )
        return conn
    except psycopg2.Error as erro:
        print(f'Erro na conexão ao PostgreSQL Server: {erro}')


def disconnect(conn):
    """desconecta uma conexão"""
    if conn:
        conn.close()


def db_updater(function, *args, **kwargs):
    """Decorator to open and close connections before execute a update/insert functions"""
    def wrapper(*args, **kwargs):
        conn = connect()
        conn.set_session(autocommit=True)
        cursor = conn.cursor()
        x = function(*args, **kwargs, cursor=cursor)
        disconnect(conn)
        return x
    return wrapper


def db_reader(function, *args, **kwargs):
    def wrapper(*args, **kwargs):
        conn = connect()
        conn.set_session(readonly=True, autocommit=True)
        cursor = conn.cursor()
        x = function(*args, **kwargs, cursor=cursor)
        disconnect(conn)
        return x
    return wrapper




