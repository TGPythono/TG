#!/bin/bash

echo "⌯ أداة InstaInfo لتحليل حسابات إنستغرام ⌯"
read -p "ادخل اليوزر: " username

if [ -z "$username" ]; then
    echo "[!] لازم تدخل يوزر"
    exit 1
fi

python3 instainfo.py $username