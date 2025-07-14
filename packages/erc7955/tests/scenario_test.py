from erc7955 import factory_deploy, factory_predict_address


def test_factory_deploy():
    # NOTE: this initcode is a bit broken and deploys an empty contract.
    initcode = bytes.fromhex(
        "608060405234801561001057600080fd5b506040516020806101008339810180604052810190808051906020019092919050505080600081905550"
    )
    deployment_salt = b"\xa0" * 32
    deployed_address = factory_deploy(initcode, deployment_salt)
    # per https://sepolia.etherscan.io/tx/0x0a2bb4a3f90508ca8546ea5ec9124a48624f50b84c5fb3cdfb8c85ea462b7e53
    assert deployed_address == "0x75eb1d1a60e4A135790E9FDaef152ee534f9b7C4"
    assert factory_predict_address(initcode, deployment_salt) == deployed_address
