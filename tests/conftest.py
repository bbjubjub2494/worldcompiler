import pytest
from script.deploy import deploy_hex0, deploy_hex2, deploy_M1
import src
import boa
from boa.util.abi import Address, abi_decode

@pytest.fixture
def hex0_contract():
    return deploy_hex0()

@pytest.fixture
def hex2_contract():
    return deploy_hex2()

@pytest.fixture
def M1_contract():
    return deploy_M1()

@pytest.fixture
def datacontract_initcode_prefix():
    return src.load_datacontract_initcode_prefix()

@pytest.fixture
def inputaddressed_initcode_template():
    return src.load_inputaddressed_initcode_template()

class ERC7955Factory:
    def __init__(self, address):
        self.address = address

    def deploy(self, initcode, salt=b'\0'*32):
        ret = boa.env.raw_call(self.address, data=salt+initcode).output
        return abi_decode("(address)", ret)[0]

@pytest.fixture
def erc7955_factory():
    address = "0xC0DE207acb0888c5409E51F27390Dad75e4ECbe7"
    code = bytes.fromhex("60203d3d3582360380843d373d34f580601457fd5b3d52f3")
    boa.env.set_code(address, code)
    return ERC7955Factory(address)
