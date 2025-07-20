from deterministic_deployment_proxy import proxy_deploy, proxy_predict_address


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
    deployed_address = proxy_deploy(initcode, deployment_salt)
    # per https://gnosisscan.io/tx/0x28a86133c20fdd7235debd1e2c13a70406fd8a1ac4ec45f01ea1cdaa558f466d
    assert deployed_address == "0x10E8540B6EE2D52fE2C57D876bD830cbC9B0E366"
    assert proxy_predict_address(initcode, deployment_salt) == deployed_address
