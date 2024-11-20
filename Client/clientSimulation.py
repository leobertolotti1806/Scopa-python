import client

print("Sto cercando di abbinare un Fake User per il debug...")
client.connect(
    "FakeUser",
    lambda json : print("Fake User connesso!!\n\nBuon Debug!!"),
    lambda err : print(err)
)