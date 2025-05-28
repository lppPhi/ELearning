from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Kết nối SQL Server, thay đổi thông tin kết nối cho phù hợp
SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://sa:123456@ADMIN-PC\\SQLEXPRESS/ELearningDB?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"timeout": 30}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
