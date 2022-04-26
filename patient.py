from pymodm import MongoModel, fields


class Patient(MongoModel):
    record = fields.IntegerField(primary_key=True)
    name = fields.CharField()
    data = fields.ListField()
