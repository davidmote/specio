# Veripy2Specio

A simple utility to validate and transform VeriPy output files into the Specio format.

**UNDER DEVELOPMENT**

Veripy2Specio is a python module that performs a variety of validations and transformations to both veripy (cucumber) output files and the official Specio file format.

Veripy2Specio includes a few options to validate a given JSON file against either schema.

At any time, run the following command to get help.

```bash
PYTHONPATH=. python -m veripy2specio --help
```

## Installing Veripy2Specio

Currently Veripy2Specio is not installed anywhere by default. To use Veripy2Specio locally, simply ensure that you have a valid virtual environment for Python 3.6 or later, and install the requirements with the following command.

```bash
cd glue/veripy2specio
pip install -r requirements.txt
```


## Running the Tests

```bash
PYTHONPATH=. py.test
```


## Transforming Format: Veripy to Specio

To convert a Veripy output file into a Specio report document, simply run the following command.

```bash
PYTHONPATH=. python -m veripy2specio -o <destination> <input>
```


## Validation Only

Veripy2Specio includes utility options that do not perform the actual conversion, instead simply checking that a given JSON file is a valid one.


### Validating a Veripy Output File


```bash
# Validate that a given file is a valid VeriPy output file.
PYTHONPATH=. python -m veripy2specio --verify-veripy <input>

# Validate that a given file is a valid Specio File
PYTHONPATH=. python -m veripy2specio --verify-specio <input>
```