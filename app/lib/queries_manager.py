from .connection_manager import *

async def fetch_db_info_postgres(db_creds: dict) -> dict:
    async with PostgresConnectionManger(db_creds) as conn:
        query = """
        SELECT 
            ns.nspname as schema_name, 
            cls.relname as table_name, 
            attr.attname as column_name, 
            pg_catalog.format_type(attr.atttypid, attr.atttypmod) as data_type
        FROM 
            pg_catalog.pg_attribute attr
            JOIN pg_catalog.pg_class cls ON attr.attrelid = cls.oid
            JOIN pg_catalog.pg_namespace ns ON cls.relnamespace = ns.oid
        WHERE 
            attr.attnum > 0
            AND NOT attr.attisdropped
            AND cls.relkind = 'r'
        ORDER BY 
            schema_name, 
            table_name, 
            column_name;
        """

        records = await conn.fetch(query)

        schema_tables = {}
        for record in records:
            schema = record['schema_name']
            table = record['table_name']
            column = record['column_name']
            data_type = record['data_type']

            schema_tables.setdefault(schema, {}).setdefault(table, []).append({column: data_type})

        return schema_tables

async def fetch_db_info_mysql(db_creds: dict) -> dict:
    async with MySQLConnectionManager(db_creds) as conn:
        query = """
        SELECT 
            table_schema AS `Database`, 
            table_name AS `Table`, 
            column_name AS `Field`, 
            column_type AS `Type`
        FROM 
            information_schema.columns
        WHERE 
            table_schema != 'information_schema' AND
            table_schema != 'mysql' AND
            table_schema != 'performance_schema' AND
            table_schema != 'sys'
        ORDER BY 
            table_schema, 
            table_name, 
            ordinal_position;
        """

        records = await conn.fetch(query)

        database_tables = {}
        for record in records:
            db_name = record['Database']
            table_name = record['Table']
            column_info = {record['Field']: record['Type']}

            database_tables.setdefault(db_name, {}).setdefault(table_name, []).append(column_info)

        return database_tables


async def fetch_table_exists_postgres(db_creds: dict, table_name: str) -> bool:
    async with PostgresConnectionManger(db_creds) as conn:
        query = """
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            AND table_name = $1
        );
        """

        record = await conn.fetchrow(query, table_name)

        return record['exists']

async def fetch_table_exists_mysql(db_creds: dict, table_name: str) -> bool:
    async with MySQLConnectionManager(db_creds) as conn:
        query = """
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            AND table_name = $1
        );
        """

        record = await conn.fetchrow(query, table_name)

        return record['exists']