from http.client import (
    NOT_FOUND,  # 404
    OK,  # 200
    CREATED,  # 201
    BAD_REQUEST,  # 400
    INTERNAL_SERVER_ERROR,  # 500
)
from flask import jsonify
from marshmallow import Schema, fields, validate


class DefaultSchema(Schema):
    @classmethod
    def build(cls, data):
        return jsonify(cls().dump(data)), OK.value

    @classmethod
    def created(cls, data):
        return jsonify(cls().dump(data)), CREATED.value


class ContatoSchema(DefaultSchema):
    id = fields.Integer()
    nome = fields.String(required=True, validate=validate.Length(max=100))
    telefone = fields.String(
        required=True, validate=validate.Length(max=30, min=1)
    )


# schemas padrao
class ErrorSchema(Schema):
    # code = fields.Integer(default=OK)

    @classmethod
    def build(cls):
        return jsonify(cls().dump({})), cls.code.value


class InternalServerErrorSchema(ErrorSchema):
    message = fields.String(default="Internal Server Error")
    code = fields.Integer(default=INTERNAL_SERVER_ERROR)
    description = fields.String(
        default="Houve um erro no servidor. Tente novamente mais tarde"
    )


class EmptyDataSchema(ErrorSchema):
    message = fields.String("Empty Data")
    code = fields.Integer(default=BAD_REQUEST)
    message = fields.String(
        default="Os dados requisitados não foram preenchidos"
    )


class NotFoundSchema(ErrorSchema):
    message = fields.String("Not Found")
    code = fields.Integer(default=NOT_FOUND)
    description = fields.String(default="Não encontrado")


class ValidationErrorSchema(ErrorSchema):
    message = fields.String("Validation Error")
    code = fields.Integer(default=BAD_REQUEST)
    description = fields.String("Erro de validação")
