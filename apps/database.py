import config
from apps.DBcm import UseDatabase

dbname = config.database_name


async def create_tables():
    """create tables"""
    try:
        async with UseDatabase(dbname) as cursor:
            _SQL = """CREATE TABLE IF NOT EXISTS addresses(
            user_id INTEGER,
            name TEXT,
            address TEXT
            );
            """
            await cursor.execute(_SQL)
    except Exception as e:
        print(e)


async def save_address(user_id: int, name: str, address: str):
    """"""
    try:
        async with UseDatabase(dbname) as cursor:
            _SQL = """INSERT INTO addresses
            VALUES(?, ?, ?);"""
            await cursor.execute(_SQL, (user_id, name, address))
    except Exception as e:
        print(e)


async def load_data(user_id):
    """"""
    try:
        async with UseDatabase(dbname) as cursor:
            _SQL = """SELECT name, address FROM addresses 
            WHERE user_id =?; """
            await cursor.execute(_SQL, (user_id,))
            res = await cursor.fetchall()
            return res
    except Exception as e:
        print(e)


async def load_names(user_id):
    """"""
    try:
        async with UseDatabase(dbname) as cursor:
            _SQL = """SELECT name FROM addresses
            WHERE user_id=?;"""
            await cursor.execute(_SQL, (user_id,))
            res = await cursor.fetchall()
            return res
    except Exception as e:
        print(e)


async def load_address(user_id, name):
    """loads user`s address"""
    try:
        async with UseDatabase(dbname) as cursor:
            _SQL = """SELECT address FROM addresses
            WHERE user_id=?
            AND name=?;"""
            await cursor.execute(_SQL, (user_id, name))
            res = await cursor.fetchall()
            return res
    except Exception as e:
        print(e)


async def search_wallet(user_id, search_query):
    """"""
    try:
        async with UseDatabase(dbname) as cursor:
            _SQL = """SELECT name, address FROM addresses
            WHERE user_id = ?
            AND name LIKE ?;"""
            await cursor.execute(_SQL, (user_id, '%' + search_query + '%'))
            content = await cursor.fetchall()
            return content
    except Exception as e:
        print(e)


async def delete_all(user_id):
    """deletes all user`s data"""
    try:
        async with UseDatabase(dbname) as cursor:
            _SQL = """DELETE FROM addresses
            WHERE user_id=?;"""
            await cursor.execute(_SQL, (user_id,))
    except Exception as e:
        print(e)


async def delete_one(user_id, name):
    """deletes one chosen address"""
    try:
        async with UseDatabase(dbname) as cursor:
            _SQL = """DELETE FROM addresses
            WHERE user_id=?
            AND name=?;"""
            await cursor.execute(_SQL, (user_id, name))
    except Exception as e:
        print(e)


async def update_name(user_id, old_name, new_name):
    """"""
    try:
        async with UseDatabase(dbname) as cursor:
            _SQL = """UPDATE addresses
            SET name = ?
            WHERE user_id =?
            AND name = ?;"""
            await cursor.execute(_SQL, (new_name, user_id, old_name))
    except Exception as e:
        print(e)


async def update_address(user_id, old_name, new_address):
    """"""
    try:
        async with UseDatabase(dbname) as cursor:
            _SQL = """UPDATE addresses
            SET address = ?
            WHERE user_id = ?
            and name = ?;"""
            await cursor.execute(_SQL, (new_address, user_id, old_name))
    except Exception as e:
        print(e)
