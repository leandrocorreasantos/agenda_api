from http.client import OK
from flask import jsonify, request
from flask.views import MethodView
from marshmallow import ValidationError
from api import db
from api.v1.schemas import (
    ContatoSchema,
    InternalServerErrorSchema,
    EmptyDataSchema,
    NotFoundSchema,
    ValidationErrorSchema,
)
from api.models import Contato


class ContatoView(MethodView):
    def get(self, contato_id=None):
        if contato_id is None:
            contatos = Contato.query.all()
            return jsonify(ContatoSchema(many=True).dump(contatos)), OK.value

        contato = Contato.query.get(contato_id)
        return jsonify(ContatoSchema().dump(contato)), OK.value

    def post(self):
        contato = {}
        data = request.get_json()
        if not data:
            return EmptyDataSchema().build()

        try:
            contato = ContatoSchema().load(data)
        except ValidationError as err:
            return ValidationErrorSchema().build(err.messages)

        try:
            db.session.add(Contato(**contato))
            db.session.commit()
        except Exception:
            db.session.rollback()
            return InternalServerErrorSchema().build()

        return ContatoSchema().created(contato)

    def put(self, contato_id=None):
        contato_id = int(contato_id)
        data = request.get_json()
        if not data or contato_id == 0:
            return EmptyDataSchema().build()

        contato = Contato.query.get(contato_id)
        if not contato:
            return NotFoundSchema().build()

        try:
            novo_contato = ContatoSchema().load(data)
        except ValidationError as err:
            return ValidationErrorSchema().build(err.message)

        contato.update(**novo_contato)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return InternalServerErrorSchema().build()

        return ContatoSchema().dump(contato)

    def delete(self, contato_id=None):
        contato_id = int(contato_id)
        if contato_id == 0:
            return EmptyDataSchema().build()

        contato = Contato.query.get(contato_id)
        if not contato:
            return NotFoundSchema().build()

        try:
            db.session.delete(contato)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return InternalServerErrorSchema().build()

        return jsonify({}), OK.value
