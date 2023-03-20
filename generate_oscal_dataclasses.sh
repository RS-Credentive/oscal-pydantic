#!/usr/bin/env sh

for SCHEMA_FILE in OSCAL/json/schema/*
    do
        SCHEMA=`echo $SCHEMA_FILE | sed "s|OSCAL/json/schema/oscal_\(.*\)_schema.json|\1|"`
        datamodel-codegen --use-title-as-name --output-model-type dataclasses.dataclass --input $SCHEMA_FILE --output src/oscal_dataclass/$SCHEMA.py
    done



