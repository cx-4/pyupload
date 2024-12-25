#!/bin/bash

rm key.pem
rm cert.pem
if ! command -v openssl 2>&1 > /dev/null
then
    echo "openssl not found"
    exit 1
fi

openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -sha256 -nodes -subj "/C=US/ST=Washington/L=Redmond/O=Microsoft Corporation/CN=Microsoft Product Secure Server CA"


if ! command -v python3 2>&1 > /dev/null
then
    echo "python3 not found"
    exit 1
fi

FLASK_APP=up.py python3 -m flask run --host 0.0.0.0 --cert=cert.pem --key=key.pem --port=8443

