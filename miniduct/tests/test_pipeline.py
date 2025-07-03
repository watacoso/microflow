import datetime

import pytest

from miniduct import run_pipeline

TEST_DATETIME = datetime.datetime(2023, 10, 1, 12, 0, 0)


@pytest.fixture
def patch_datetime_now(monkeypatch):
    class MockDatetime:
        @classmethod
        def now(cls):
            return TEST_DATETIME

    # Mock the datetime class to return a fixed date and time
    monkeypatch.setattr(datetime, "datetime", MockDatetime)


def test_main(mocker, patch_datetime_now):
    expected_output_name = "test_pipeline_20231001_120000.json"

    expected_data = {"data": "mock_data"}
    mock_datasource = mocker.Mock(name="DataSource")
    mock_datasource.get.return_value = expected_data

    mock_outputs = [mocker.Mock(name="Output1"), mocker.Mock(name="Output2")]

    run_pipeline(pipeline_name="test_pipeline", ingestion=mock_datasource, outputs=mock_outputs)

    mock_datasource.get.assert_called_once()

    for output in mock_outputs:
        output.write.assert_called_once()
        data = mock_datasource.get.return_value
        print(f"Data to be written: {data}")
        output.write.assert_called_with(expected_data, expected_output_name)
