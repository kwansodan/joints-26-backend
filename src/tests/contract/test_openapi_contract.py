import pytest
import schemathesis
from django.core.wsgi import get_wsgi_application
from django.db import close_old_connections
from schemathesis.config import GenerationConfig, SchemathesisConfig

app = get_wsgi_application()

config = schemathesis.Config.from_path(
    "src/tests/schemathesis.toml"
)

schema = schemathesis.openapi.from_wsgi(
    "/api/schema/", 
    app,
    config=config
)

@schema.parametrize()
@pytest.mark.contract
@pytest.mark.django_db(transaction=True)
def test_openapi_contract(case):
    close_old_connections()
    response = case.call()
    case.validate_response(response)
