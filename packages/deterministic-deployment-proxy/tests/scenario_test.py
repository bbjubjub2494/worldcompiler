from deterministic_deployment_proxy import proxy_deploy, proxy_predict_address


def test_proxy_deploy():
    # NOTE: this initcode is a bit broken and deploys an empty contract.
    initcode = bytes.fromhex(
        "608060405234801561001057600080fd5b506040516020806101008339810180604052810190808051906020019092919050505080600081905550"
    )
    deployment_salt = b"\xa0" * 32
    deployed_address = proxy_deploy(initcode, deployment_salt)
    assert deployed_address == "0x7184cAA7558FE9d89096d15Df5D90D96876B4E1F"
    assert proxy_predict_address(initcode, deployment_salt) == deployed_address
