import asyncio
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import text

async def create_table_script(engine: AsyncEngine, sql_file_path: str = "db.sql"):
    """
    Execute SQL statements from a file.
    """
    try:
        with open(sql_file_path, "r", encoding="utf-8") as f:
            sql_statements = f.read()

        async with engine.connect() as conn:  # Use connect(), not begin()
            for stmt in sql_statements.split(";"):
                stmt = stmt.strip()
                if stmt:
                    await conn.execute(text(stmt))
            await conn.commit()  # Ensure DDL statements are committed
        print("✅ db.sql executed successfully!")
    except Exception as e:
        print("❌ Failed to execute db.sql:", e)