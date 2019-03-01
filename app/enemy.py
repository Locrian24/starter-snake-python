class Enemy:
    def __init__(self, enemy):
        self.body = enemy["body"]
        self.length = len(self.body)
        self.health = enemy["health"]