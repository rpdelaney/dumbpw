def test_version_set():
    """The module sets a __version__."""
    import dumbpw  # noqa: PLC0415

    assert dumbpw.__version__
