#!/usr/bin/env sh

for SCHEMA_FILE in OSCAL/json/schema/*
    do
        SCHEMA=`echo $SCHEMA_FILE | sed "s|OSCAL/json/schema/oscal_\(.*\)_schema.json|\1|"`
        datamodel-codegen --use-annotated --use-title-as-name --input $SCHEMA_FILE --output src/oscal_pydantic/$SCHEMA.py
    done



