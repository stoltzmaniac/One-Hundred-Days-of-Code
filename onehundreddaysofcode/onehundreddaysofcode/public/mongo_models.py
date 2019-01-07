from onehundreddaysofcode.database import medb


class RandomData(medb.Document):
    username = medb.StringField(max_length=100)
    text = medb.StringField(max_length=500)
