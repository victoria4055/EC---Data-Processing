# victoria villasana

class InMemoryDB:
    def __init__(self):
        self.database = {}
        self.transaction = None

    # starting new transaction
    def begin_transaction(self):
        # if already transaction then raises error
        if self.transaction is not None:
            raise Exception("Transaction already in progress.")
        self.transaction = {}

    # sets a key-value pair only within active transaction
    def put(self, key, value):
        # if none is active then raise error
        if self.transaction is None:
            raise Exception("No transaction in progress.")
        # temporarily saving change
        self.transaction[key] = value

    # gets value for key
    def get(self, key):
        # if active and updated then return value
        if self.transaction and key in self.transaction:
            return self.transaction[key]
        # otherwise return from orig commit
        return self.database.get(key, None)
    
    # commit all changes to database
    def commit(self):
        if self.transaction is None:
            raise Exception("No transaction in progress.")
        # apply changes to main database
        self.database.update(self.transaction)
        self.transaction = None

    # cancels transaction and uncommitted changes
    def rollback(self):
        if self.transaction is None:
            raise Exception("No transaction in progress.")
        self.transaction = None


# testing here

if __name__ == "__main__":
    db = InMemoryDB()

    # should print none bc nothing in database yet
    print(db.get("A"))

    # should give error bc no transaction yet
    try:
        db.put("A", 5)
    except Exception as e:
        print("Error:", e)

    # begins transaction
    db.begin_transaction()

    # puts value 5 for key "A" in transaction
    db.put("A", 5)

    # should return 5 bc just set inside transaction
    print(db.get("A"))

    # updates A to 6 within transaction
    db.put("A", 6)

    # commit's the transaction
    db.commit()

    # A should return 6
    print(db.get("A"))

    # raises error bc no active transaction
    try:
        db.commit()
    except Exception as e:
        print ("Error:", e)

    # starts new transaction and puts B as value 10
    db.begin_transaction()
    db.put("B", 10)

    # undoes the changes made for B
    db.rollback()

    # returns none bc B was never committed
    print(db.get("B"))

    # starting new transaction w multiple keys
    db.begin_transaction()
    db.put("X", 100)
    db.put("Y", 200)

    # getting values inside transaction
    print("In transaction X is : ", db.get("X"))
    print("In transaction Y is : ", db.get("Y"))

    # commit so changes are saved
    db.commit()
    print("After commit X is : ", db.get("X"))
    print("After commit Y is : ", db.get("Y"))

    # testing updating key inside transaction
    db.begin_transaction()
    db.put("X", 300)
    print("Updated X in transaction is : ", db.get("X"))
    db.rollback()
    print("After rollback X is : ", db.get("X"))