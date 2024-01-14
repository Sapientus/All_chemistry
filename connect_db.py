from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

user = "postgres"
password = "zeyno14916"
host = "localhost"
port = "5432"
db = "postgres"
link = f"postgresql://{user}:{password}@{host}:{port}/{db}"
engine = create_engine(link, echo=True, pool_size=5)
Session = sessionmaker(bind=engine)
session = Session()
