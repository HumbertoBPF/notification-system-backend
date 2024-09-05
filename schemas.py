from marshmallow import Schema, fields


class MessageSchema(Schema):
    subject = fields.Str(required=True)
    message = fields.Str(required=True)


class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class SignupSchema(Schema):
    email = fields.Str(required=True)
    country_code = fields.Str(required=False, load_default="en-us")
    phone_number = fields.Str(required=False, load_default=None)
    password = fields.Str(required=True)
    opt_in_email = fields.Bool(required=True)
    opt_in_phone = fields.Bool(required=True)
