import client

print("Sto cercando di abbinare un Fake User per il debug...")

def initGame(obj):
    print("Fake User connesso!!\n\nBuon Debug!!")
    client.inviaJSON({"request": "startGameOk"})

client.connect(
    "FakeUser",
    initGame,
    lambda err : print(err)
)
