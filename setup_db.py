from sqlalchemy import create_engine
from Tchat.dependencies.users import User



engine = create_engine(
     'postgresql+psycopg2://junior:testdb@localhost/tempchat'
)

User.metadata.create_all(engine)
