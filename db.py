# victoria villasana

class InMemoryDB:
    def __init__(self):
        self.database = {}
        self.transaction = None

    def begin_transaction(self):
        if self.transaction is not None:
            raise Exception("Transaction already in progress.")
        self.transaction = {}

    def put(self, key, value):
        if self.transaction is None:
            raise Exception("No transaction in progress.")
        self.transaction[key] = value

    def get(self, key):
        if self.transaction and key in self.transaction:
            return self.transaction[key]
        return self.database.get(key, None)
    
    def commit(self):
        if self.transaction is None:
            raise Exception("No transaction in progress.")
        self.database.update(self.transaction)
        self.transaction = None

    def rollback(self):
        if self.transaction is None:
            raise Exception("No transaction in progress.")
        self.transaction = None


# testing here

if __name__ == "__main__":
    db = InMemoryDB()

    print(db.get("A"))
    try:
        db.put("A", 5)
    except Exception as e:
        print("Error:", e)

    db.begin_transaction()
    db.put("A", 5)
    print(db.get("A"))
    db.put("A", 6)
    db.commit()
    print(db.get("A"))

    try:
        db.commit()
    except Exception as e:
        print ("Error:", e)

    db.begin_transaction()
    db.put("B", 10)
    db.rollback()
    print(db.get("B"))