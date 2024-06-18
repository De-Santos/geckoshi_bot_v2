from database.vars import engine, Base


def init_db():
    Base.metadata.create_all(engine)
