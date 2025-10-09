class BasicState:
    @property
    def max_books(self):
        return 10
    @property
    def max_days(self):
        return 14
    @property
    def free_extend(self):
        return 0
class StandardState:
    @property
    def max_books(self):
        return 20
    @property
    def max_days(self):
        return 30
    @property
    def free_extend(self):
        return 2
    def has_priority(self):
        return True
class PremiumState:
    @property
    def max_books(self):
        return 50
    @property
    def max_days(self):
        return 60
    @property
    def free_extend(self):
        return 5
    def has_priority(self):
        return True
