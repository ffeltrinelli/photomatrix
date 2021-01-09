from photomatrix import __main__ as photomatrix
import pytest
try:
    from importlib import metadata
except ImportError:
    # on Python <3.8 use importlib-metadata package
    import importlib_metadata as metadata


def test_printed_version(capsys):
    expected_version = metadata.version('photomatrix')

    with pytest.raises(SystemExit):
        photomatrix.main(['--version'])

    actual_output = capsys.readouterr().out.rstrip()
    assert actual_output, 'No output found'
    assert actual_output == expected_version
