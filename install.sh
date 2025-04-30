#!/data/data/com.termux/files/usr/bin/bash

echo "[✓] جاري تثبيت المتطلبات..."

pkg update -y
pkg install -y python git

pip install requests python-cfonts

# نسخ الأداة للمسار العالمي
cp instainfo.py /data/data/com.termux/files/usr/bin/instainfo
chmod +x /data/data/com.termux/files/usr/bin/instainfo

echo "[✓] تم التثبيت بنجاح! اكتب الأمر التالي:"
echo "instainfo username"
