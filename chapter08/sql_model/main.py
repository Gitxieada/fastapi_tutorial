from sqlmodel import create_engine
ASYNC_DATABASE_URI = "sqlite+aiosqlite:///aiosqlite_user.db"
engine = create_engine(ASYNC_DATABASE_URI)