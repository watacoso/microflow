from miniduct.pipeline import run_pipeline
import pytest
import datetime
from unittest.mock import MagicMock

TIME_FORMAT = "%Y%m%d_%H%M%S"

@pytest.fixture
def mock_data_source():
    class MockDataSource:
        def get(self):
            print("MockDataSource: Fetching data")
    mock_data_source = MockDataSource()
    mock_data_source.get = MagicMock(name='get', return_value={"data": "mock_data"})
    return mock_data_source
        
@pytest.fixture
def mock_outputs():
    class MockOutput1:
        def write(self, data, file_name):
            print(f"MockOutput1: Writing data {data} to {file_name}")
            
    class MockOutput2:
        def write(self, data, file_name):
            print(f"MockOutput2: Writing data {data} to {file_name}")
        
    mock_output1 = MockOutput1()
    mock_output1.write = MagicMock()
    mock_output2 = MockOutput2()
    mock_output2.write = MagicMock()
    return [mock_output1, mock_output2]

def test_run_pipeline(mock_data_source, mock_outputs):
 
    run_pipeline(
        pipeline_name="test_pipeline",
        ingestion=mock_data_source,
        outputs=mock_outputs
    )
    
    mock_data_source.get.assert_called_once()
    
    for output in mock_outputs:
        output.write.assert_called_once()
        data = mock_data_source.get.return_value
        print(f"Data to be written: {data}")
        file_name = f"test_pipeline_{datetime.datetime.now().strftime(TIME_FORMAT)}.json"
        output.write.assert_called_with(data, file_name)