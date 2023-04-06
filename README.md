
## Deploy

Configure `~/.pypirc`:

```ini
[distutils]
index-servers =
    python

[python]
repository: https://us-central1-python.pkg.dev/rosebud-machine-learning/python/
```


Insert the following snippet into your pip.conf
```
[global]
extra-index-url = https://us-central1-python.pkg.dev/rosebud-machine-learning/python/simple/
```

Install keyring with google auth plugin:

```bash
pip install keyring keyrings.google-artifactregistry-auth
keyring --list-backends # should include google backend with priority 9
keyring get https://us-python.pkg.dev/ '' # should return google token
```

Build and publish:

```bash
pip install build twine
rm -rf dist
python -m build
twine upload -r python dist/*
```


HOWTO install last version without extra configuration
```
pip install --isolated keyring keyrings.google-artifactregistry-auth
PIP_EXTRA_INDEX_URL=https://us-central1-python.pkg.dev/rosebud-machine-learning/python/simple/ pip install -U roseml
```

References:

* <https://cloud.google.com/artifact-registry/docs/python/authentication>
* <https://stackoverflow.com/a/65424781>