from marshmallow import Schema, fields
# Schemas are used for validation

class PlainItemSchema(Schema):
    # dump_only means only used for returning data back to the client(not receiving from JSON)
    id = fields.Int(dump_only=True) 
    name = fields.Str(required=True) # field is required and must be in the JSON payload
    price = fields.Float(required=True) # required=True means the JSON INCLUDES the specific field!


class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True) # only used for sending data back to the client!
    name = fields.Str(required=True)


class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True) # only used for sending data back to the client!
    name = fields.Str()


# In the update schema (put) we are looking for name and price
class ItemUpdateSchema(Schema):
    name = fields.Str() # name and price are not required in the put schema
    price = fields.Float() # either name or price can be given so we take out required=True


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only = True)


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)


class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    # password should ALWAYS BE LOAD_ONLY b/c it should only be sent from user performing authentification
    password = fields.Str(required=True, load_only=True)