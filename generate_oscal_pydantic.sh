#!/usr/bin/env sh

for SCHEMA_FILE in OSCAL/json/schema/*
    do
        SCHEMA=`echo $SCHEMA_FILE | sed "s|OSCAL/json/schema/oscal_\(.*\)_schema.json|\1|"`
        datamodel-codegen --use-annotated --use-title-as-name --input $SCHEMA_FILE --output src/oscal_pydantic/$SCHEMA.py
    done

# Correct some problems with the automatically generated models
for PYDANTIC_MODEL in src/oscal_pydantic/*.py
    do
        # Invalid REGEX pattern 
        # ^(\\p{L}|_)(\\p{L}|\\p{N}|[.\\-_])*$ - replace with 
        # ^(\\w|_)(\\w|\\d|[.\\--_])*$
        sed -i 's=^(\\p{L}|_)(\\p{L}|\\p{N}|[.\\-_])*$=^(\\w|_)(\\w|\\d|[.\\--_])*$=' $PYDANTIC_MODEL

        # Get rid of Regex for datatypes other than str - it is redundant and will
        # create an error
    done