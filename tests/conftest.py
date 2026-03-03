import copy
import pytest
from fastapi.testclient import TestClient
import src.app as app_module

ORIGINAL = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def isolated_activities(monkeypatch):
    monkeypatch.setattr(app_module, "activities", copy.deepcopy(ORIGINAL))
    yield


@pytest.fixture
def client():
    return TestClient(app_module.app)
