# OSCAL Pydantic

## Description
A simple module that contains pydantic datamodels representing the OSCAL standard. They are built from the OSCAL models published by NIST at https://github.com/usnistgov/OSCAL

Several Python projects include data models, but importing a large project just to get access to the datamodel represents a significant overhead. This module simply provides the models.

## Installation

Package coming!

## Usage

To import a specific model, include it in your python file:

e.g.: from oscal_pydantic import catalog

Alternatively, you can import the complete OSCAL schema:

from oscal_pydantic import complete

After importing, you should be able to define OSCAL objects that support pydantic's rich validation rules.

## License

This code is released under the [CC0 1.0 Universal Public Domain Dedication] (https://creativecommons.org/publicdomain/zero/1.0/).
