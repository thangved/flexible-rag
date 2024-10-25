import json

from fastapi.openapi.utils import get_openapi

from api.main import app

with open("docs/api/openapi.json", "w") as f:
    json.dump(
        get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            routes=app.routes,
            servers=app.servers,
            contact=app.contact,
            license_info=app.license_info,
            separate_input_output_schemas=app.separate_input_output_schemas,
            summary=app.summary,
            terms_of_service=app.terms_of_service,
        ),
        f,
    )
