class BaseRepository:
    def __init__(self, db):
        self.db = db

    def add(self, obj):
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get_all(self, model):
        return self.db.query(model).all()