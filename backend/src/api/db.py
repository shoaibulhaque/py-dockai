import os
import sqlmodel
from sqlmodel import Session, SQLModel

# Debug: Print all environment variables that start with DATABASE
print("🔍 Environment variables:")
for key, value in os.environ.items():
    if "DATABASE" in key or "API" in key or "PORT" in key:
        print(f"  {key} = {value}")

print(f"🔍 All env vars count: {len(os.environ)}")

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    print("❌ DATABASE_URL not found in environment variables!")
    print("Available environment variables:")
    for key in sorted(os.environ.keys()):
        print(f"  - {key}")
    raise ValueError("DATABASE_URL environment variable is not set!")

print(f"🔗 Connecting to database: {DATABASE_URL}")  # ✅ Debug info


engine = sqlmodel.create_engine(DATABASE_URL)


# database models
# Does not create db migrations
def init_db():
    print("creating database tables...")
    SQLModel.metadata.create_all(engine)


# api routes
def get_session():
    with Session(engine) as session:
        yield session
