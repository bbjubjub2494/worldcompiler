import pytest
from script.deploy import deploy_hex0
import src

@pytest.fixture
def hex0_contract():
    return deploy_hex0()

@pytest.fixture
def datacontract_initcode_prefix():
    return src.load_datacontract_initcode_prefix()

@pytest.fixture
def inputaddressed_initcode_template():
    return src.load_inputaddressed_initcode_template()
