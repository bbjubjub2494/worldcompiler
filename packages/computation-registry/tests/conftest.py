import pytest

from contracts import Registry, Fibonacci


@pytest.fixture
def registry_contract():
    return Registry.deploy()


@pytest.fixture
def fibonacci_contract():
    return Fibonacci.deploy()
