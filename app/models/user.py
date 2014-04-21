class User():  
    def __init__(self, record):
        self._id = record["_id"]
        self.username = record["username"]
        self.password = record["password"]
        self.favorites = record["favorites"]

    def get_id(self):
        return str(self.username)
        
    def is_authenticated(self):
        return True
        
    def is_active(self):
        return True
        
    def is_anonymous(self):
        return False
