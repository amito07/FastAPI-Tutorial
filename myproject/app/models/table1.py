from tortoise.models import Model
from tortoise import fields


class test_table(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, null=False)
    phone_number = fields.IntField(null=False)


class user_table(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, null=False)
    age = fields.IntField(max=100, null = False)
    phone_number = fields.IntField(null=True)
    img_url = fields.JSONField(null=True)
