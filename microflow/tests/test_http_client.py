import responses, pytest, pytest_mock
from microflow.http_client import APIClient

base_url = "https://api.example.com"


@pytest.fixture
def client():
    return APIClient(base_url=base_url)


@responses.activate
def test_get_data(client):
    
    response=responses.Response(
        method=responses.GET,
        url=f"{base_url}/data",
        json={"key": "value"},
        status=200
    )
    responses.add(response)
    
    data = client.get_data("data")
    assert data == {"key": "value"}
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == f"{base_url}/data"
