import pytest
from ml_instrumentation.Writer import Writer

@pytest.fixture
def writer():
    writer = Writer(
        db_path=':memory:',
        low_watermark=2,
        high_watermark=4,
    )
    yield writer
    writer.close()
