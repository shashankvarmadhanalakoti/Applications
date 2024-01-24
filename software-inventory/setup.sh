#!/bin/bash

echo "Enter Kandji API-Key"
read input_string
echo "KANDJI_API_KEY=$input_string">>./src/.env

pip3 install -r requirements.txt
