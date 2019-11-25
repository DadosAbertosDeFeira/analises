#!/bin/bash
ENVFILE=.env
if test -f "$ENVFILE"; then
  rm .env
  echo "PYTHONSTARTUP=$PWD/.startup.py" >> .env
else
  echo "PYTHONSTARTUP=$PWD/.startup.py" >> .env
fi