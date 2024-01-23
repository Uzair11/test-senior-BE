from abc import ABC, abstractmethod
import asyncio
import asyncpg
import aiomysql


class ConnectionManger(ABC):
    def __init__(self, creds):
        self.creds = creds
        self.conn = None

    @abstractmethod
    def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError


class PostgresConnectionManger(ConnectionManger):
    async def __aenter__(self):
        self.conn = await asyncpg.connect(**self.creds)
        return self.conn

    async def __aexit__(self, exc_type, exc_val
                        , traceback):
        await self.conn.close()


class MySQLConnectionManager(ConnectionManger):
    async def __aenter__(self):
        self.conn = await aiomysql.connect(**self.creds)
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
            await self.conn.wait_closed()

