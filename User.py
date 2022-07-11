import database_worker
class User:
    logged_in = False
    def __init__(self, id):
        self.id = id
        database_worker.get_user_data(self.id)
    def is_authenticated(self):
        return self.logged_in # Later check if access token is still valid
    def is_active(self):
        return True # I wont do bans till I need to
    def is_anonymous(self):
        return False # no user can be anon
    def get_id(self):
        return self.id
    