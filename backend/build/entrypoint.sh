#!/bin/sh

banner ARTICLE BOOKMARK TOOL

curl --create-dirs -o "$HOME"/.postgresql/root.crt "${CA_CERT}"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload --no-access-log