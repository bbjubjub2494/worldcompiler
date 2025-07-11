import Registry

MAX_N: constant(uint256) = 100

@external
def fib(n: uint256) -> uint256:
    a: uint256 = 0
    b: uint256 = 1
    assert n < MAX_N, "n is too large"
    for _: uint256 in range(n, bound=MAX_N):
        tmp: uint256 = a
        a = b
        b = tmp + b
    return b
