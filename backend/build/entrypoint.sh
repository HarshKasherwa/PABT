#!/bin/sh

banner ARTICLE BOOKMARK TOOL

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --no-access-log