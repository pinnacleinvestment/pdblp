import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--offline", action="store_true", default=False,
        help="Run tests in offline mode (has no BBG connection)"
    )
    parser.addoption(
        "--port", action="store", default=8194, type=int,
        help="Port to connect"
    )
    parser.addoption(
        "--host", action="store", default='localhost', help="Host to connect"
    )
    parser.addoption(
        "--timeout", action="store", default=5000, type=int,
        help="BCon.timeout value"
    )


def pytest_configure(config):
    config.cache.set('offline', config.getoption('--offline'))


def pytest_configure(config):
    config.cache.set('offline', config.getoption('--offline'))
    config.addinivalue_line(
        "markers", "ifbbg: mark test as requiring a live BBG connection"
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption('--offline'):
        skip_ifbbg = pytest.mark.skip(
            reason="No BBG connection, skipping tests"
        )
        for item in items:
            if "ifbbg" in item.keywords:
                item.add_marker(skip_ifbbg)