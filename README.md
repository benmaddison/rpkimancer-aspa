# rpkimancer-aspa

An [rpkimancer](https://github.com/benmaddison/rpkimancer/) plug-in providing
the ability to read and write example ASPA objects.

## Installation

``` sh
python -m pip install rpkimancer-aspa
```

## Usage

Object creation and inspection is provided by the `rpkincant` CLI tool.

See `rpkincant --help` for usage information.

For usage as a library, see the
[rpkimancer docs](https://benmaddison.github.io/rpkimancer).

## Contributing

After making changes to the ASN.1 module source, execute `make asn1` to update
the patched version in python distribution tree.

To setup a development environment with the required test dependencies:

``` sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r packaging/requirements-dev.txt
```
