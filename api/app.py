import os
from api import app as application
from api.v1.contato_resource import ContatoView as v1_Contato


application.add_url_rule(
    "/v1/contato",
    view_func=v1_Contato.as_view("contatos"),
    methods=["GET", "POST"],
)

application.add_url_rule(
    "/v1/contato/<int:contato_id>",
    view_func=v1_Contato.as_view("contato"),
    methods=["GET", "PUT", "DELETE"],
)


if __name__ == "__main__":
    application.run(
        debug=application.debug,
        host=os.environ.get("HOST", "0.0.0.0"),
        port=os.environ.get("PORT", 5000),
    )
