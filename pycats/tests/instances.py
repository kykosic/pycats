import pytest


def test_instance_import():
    a = [1, 2, 3]

    with pytest.raises(AttributeError):
        a.map(lambda x: x + 1)

    import pycats.instances  # noqa: F401

    _ = a.map(lambda x: x + 1)
