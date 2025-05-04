#!/usr/bin/env python3
import os
import requests
import sys
import webbrowser

# تثبيت المكتبة إذا مو موجودة
try:
    from cfonts import render
except:
    os.system('pip install python-cfonts')
    from cfonts import render

title = render("Instainfo", colors=['red', 'yellow'], align='center')
print(title)

# إضافة السكربت الخاص بتوليد الصفحات
PROFILE_DIR = "profiles"
INDEX_TEMPLATE = "index.html"
PROFILE_TEMPLATE = "site_template.html"

def generate_profile_page(username, result_text):
    with open(PROFILE_TEMPLATE, "r", encoding="utf-8") as f:
        template = f.read()

    page = template.replace("{{USERNAME}}", username)
    page = page.replace("{{RESULT}}", f"<pre>{result_text}</pre>")

    os.makedirs(PROFILE_DIR, exist_ok=True)
    with open(f"{PROFILE_DIR}/{username}.html", "w", encoding="utf-8") as f:
        f.write(page)

def update_index(username):
    with open(INDEX_TEMPLATE, "r", encoding="utf-8") as f:
        content = f.read()

    if "{{ACCOUNTS}}" not in content:
        print("[!] ملف index.html لازم يحتوي {{ACCOUNTS}}")
        return

    new_entry = f'<li><a href="profiles/{username}.html">{username}</a></li>'

    updated = content.replace("{{ACCOUNTS}}", new_entry + "\n{{ACCOUNTS}}")
    with open(INDEX_TEMPLATE, "w", encoding="utf-8") as f:
        f.write(updated)

if len(sys.argv) != 2:
    print("[!] الاستعمال: insta username")
    sys.exit()

username = sys.argv[1].strip()
url = f'https://i.instagram.com/api/v1/users/web_profile_info/?username={username}'

headers = {
    'user-agent': 'Mozilla/5.0',
    'x-ig-app-id': '936619743392459',
}

print(f"[~] جاري البحث عن معلومات: {username}")

try:
    res = requests.get(url, headers=headers).json()
    user = res["data"]["user"]
except:
    print("[!] لم يتم العثور على الحساب.")
    sys.exit()

# معلومات أساسية
name = user["full_name"]
user_id = user["id"]
bio = user["biography"]
followers = user["edge_followed_by"]["count"]
following = user["edge_follow"]["count"]
posts = user["edge_owner_to_timeline_media"]["count"]
profile_pic = user["profile_pic_url_hd"]
is_private = "نعم" if user["is_private"] else "لا"
is_verified = "نعم" if user["is_verified"] else "لا"
account_type = user.get("category_name", "غير محدد")
username_link = f"https://instagram.com/{username}"
web_viewer = f"https://insta-stalker.com/profile/{username}"

# أول منشور (إذا موجود)
try:
    latest_post = user["edge_owner_to_timeline_media"]["edges"][0]["node"]["display_url"]
except:
    latest_post = "لا يوجد منشورات"

# تاريخ الإنشاء (من موقع خارجي)
try:
    date = requests.get(f"https://o7aa.pythonanywhere.com/?id={user_id}").json()["date"]
except:
    date = "غير معروف"

# تحليل العلاقة من البايو
relation_hint = "نعم" if any(word in bio.lower() for word in ["taken", "love", "engaged", "married", "single"]) else "غير واضح"

# استخراج الكلمات من البايو
keywords = ", ".join([word for word in bio.split() if len(word) > 4])

# النتيجة
result = f"""
⌯ تم استخراج معلومات الحساب ⌯

[💙] الاسم             : {name}
[👻] اليوزر            : {username}
[🆔] المعرف            : {user_id}
[📄] البايو            : {bio}
[🔑] كلمات البايو      : {keywords or "لا توجد"}
[❤] علاقة؟            : {relation_hint}
[👥] المتابعين         : {followers}
[🗣] المتابَعين        : {following}
[💞] المنشورات         : {posts}
[🔗] رابط الحساب       : {username_link}
[⏱] تاريخ الإنشاء     : {date}
[🔒] خاص؟              : {is_private}
[✅] موثق؟             : {is_verified}
[📌] نوع الحساب        : {account_type}
[🖼] صورة البروفايل    : {profile_pic}
[📸] أحدث منشور        : {latest_post}
[🌐] رابط خارجي        : {web_viewer}
"""

print(result)

# حفظ النتيجة
with open(f"{username}_info.txt", "w", encoding="utf-8") as f:
    f.write(result)

print(f"[✓] تم حفظ النتائج في {username}_info.txt")

# توليد صفحة للحساب
generate_profile_page(username, result)

# تحديث الصفحة الرئيسية
update_index(username)

# فتح الصورة
ask = input("[?] هل تريد فتح صورة البروفايل؟ (y/n): ").lower()
if ask == 'y':
    webbrowser.open(profile_pic)