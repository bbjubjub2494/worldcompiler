from erc7955 import factory_deploy, factory_predict_address


def test_example():
    initcode = bytes.fromhex(
        "61"  # PUSH2
        # beginning of runtime code
        "  33"  # CALLER
        "  FF"  # SELFDESTRUCT
        # end of runtime code
        "5F"  # PUSH0
        "52"  # MSTORE
        "60 02"  # PUSH2 2
        "60 1E"  # PUSH2 30
        "F3"  # RETURN
    )
    deployment_salt = b"\xa0" * 32
    deployed_address = factory_deploy(initcode, deployment_salt)
    # per https://gnosisscan.io/tx/0xf103fb5862ff4018f747a6920d0578266b11496a526abb12a526ee2800e0073f
    assert deployed_address == "0x3eBe728Be9BEE0393f476a186fb5457779cAde3d"
    assert factory_predict_address(initcode, deployment_salt) == deployed_address
