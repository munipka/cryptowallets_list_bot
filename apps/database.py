import asyncio

import config
from apps.DBcm import UseDatabase

dbname = config.database_name


async def create_tables():
    """create tables"""
    async with UseDatabase(dbname) as cursor:
        _SQL = """CREATE TABLE IF NOT EXISTS addresses(
        user_id INTEGER,
        name TEXT,
        address TEXT
        );
        """
        await cursor.execute(_SQL)


async def save_address(user_id: int, name: str, address: str):
    """"""
    async with UseDatabase(dbname) as cursor:
        _SQL = """INSERT INTO addresses
        VALUES(?, ?, ?);"""
        await cursor.execute(_SQL, (user_id, name, address))


async def load_data(user_id):
    """"""
    async with UseDatabase(dbname) as cursor:
        _SQL = """SELECT name, address FROM addresses 
        WHERE user_id =?; """
        await cursor.execute(_SQL, (user_id,))
        res = await cursor.fetchall()
        return res


async def load_names(user_id):
    """"""
    async with UseDatabase(dbname) as cursor:
        _SQL = """SELECT name FROM addresses
        WHERE user_id=?;"""
        await cursor.execute(_SQL, (user_id,))
        res = await cursor.fetchall()
        return res


async def load_address(user_id, name):
    """loads user`s address"""
    async with UseDatabase(dbname) as cursor:
        _SQL = """SELECT address FROM addresses
        WHERE user_id=?
        AND name=?;"""
        await cursor.execute(_SQL, (user_id, name))
        res = await cursor.fetchall()
        return res


async def search_wallet(user_id, search_query):
    """"""
    async with UseDatabase(dbname) as cursor:
        _SQL = """SELECT name, address FROM addresses
        WHERE user_id = ?
        AND name LIKE ?;"""
        await cursor.execute(_SQL, (user_id, '%'+search_query+'%'))
        content = await cursor.fetchall()
        return content

async def delete_all(user_id):
    """deletes all user`s data"""
    async with UseDatabase(dbname) as cursor:
        _SQL = """DELETE FROM addresses
        WHERE user_id=?;"""
        await cursor.execute(_SQL, (user_id,))


async def delete_one(user_id, name):
    """deletes one chosen address"""
    async with UseDatabase(dbname) as cursor:
        _SQL = """DELETE FROM addresses
        WHERE user_id=?
        AND name=?;"""
        await cursor.execute(_SQL, (user_id, name))


async def update_name(user_id, old_name, new_name):
    """"""
    async with UseDatabase(dbname) as cursor:
        _SQL = """UPDATE addresses
        SET name = ?
        WHERE user_id =?
        AND name = ?;"""
        await cursor.execute(_SQL, (new_name, user_id, old_name))


async def update_address(user_id, old_name, new_address):
    """"""
    async with UseDatabase(dbname) as cursor:
        _SQL = """UPDATE addresses
        SET address = ?
        WHERE user_id = ?
        and name = ?;"""
        await cursor.execute(_SQL, (new_address, user_id, old_name))


if __name__ == "__main__":
    asyncio.run(delete_one(5346961, 'Solana'))
