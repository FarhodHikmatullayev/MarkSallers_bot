import datetime
from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config
from data.config import DEVELOPMENT_MODE


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        print('DEVELOPMENT_MODE', DEVELOPMENT_MODE)
        if DEVELOPMENT_MODE:
            self.pool = await asyncpg.create_pool(
                user=config.DB_USER,
                password=config.DB_PASS,
                host=config.DB_HOST,
                database=config.DB_NAME
            )
        else:
            self.pool = await asyncpg.create_pool(
                dsn=config.DATABASE_URL
            )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def create_user(self, phone, username, telegram_id, full_name):
        sql = "INSERT INTO Users (phone, username, telegram_id, full_name) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, phone, username, telegram_id, full_name, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_users(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    # for sellers
    async def create_seller(self, first_name, last_name, phone, branch_id, code):
        sql = "INSERT INTO Seller (first_name, last_name, phone, branch_id, code) VALUES($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql, first_name, last_name, phone, branch_id, code, fetchrow=True)

    async def select_all_sellers(self):
        sql = "SELECT * FROM Seller"
        return await self.execute(sql, fetch=True)

    async def select_sellers(self, **kwargs):
        sql = "SELECT * FROM Seller WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    # async def delete_all_sellers(self):
    #     sql = "DELETE FROM Seller"
    #     return await self.execute(sql, execute=True)

    async def delete_all_sellers(self):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    # Avval Marks jadvalidagi seller ga bog'langan yozuvlarni o'chirish
                    await connection.execute("""
                        DELETE FROM mark
                        WHERE seller_id IN (SELECT id FROM seller)
                    """)

                    # So'ng Seller jadvalidagi barcha yozuvlarni o'chirish
                    await connection.execute("DELETE FROM seller")
        except Exception as e:
            raise Exception(f"Barcha seller'larni o'chirishda xato yuz berdi: {e}")

    # for branches
    async def create_branch(self, name):
        sql = "INSERT INTO Branch (name) VALUES($1) returning *"
        return await self.execute(sql, name, fetchrow=True)

    async def select_branch(self, **kwargs):
        sql = "SELECT * FROM Branch WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    # for marks

    async def create_mark(self, seller_id, user_id, category_id, mark, description):
        created_at = datetime.datetime.now()
        sql = "INSERT INTO Mark (seller_id, user_id, category_id, mark, description, created_at) VALUES($1, $2, $3, $4, $5, $6) returning *"
        return await self.execute(sql, seller_id, user_id, category_id, mark, description, created_at, fetchrow=True)

    async def select_marks(self, **kwargs):
        sql = "SELECT * FROM Mark WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_all_marks(self):
        sql = "SELECT * FROM Mark"
        return await self.execute(sql, fetch=True)

    # for categories
    async def select_all_categories(self):
        sql = "SELECT * FROM Category"
        return await self.execute(sql, fetch=True)

    async def select_category(self, id):
        sql = f"SELECT * FROM Category WHERE id = $1"
        return await self.execute(sql, id, fetchrow=True)
