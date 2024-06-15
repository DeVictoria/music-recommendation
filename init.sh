#!/bin/sh
export FLASK_APP=interface.py
flask db init
flask db migrate -m "users table"
flask db upgrade
