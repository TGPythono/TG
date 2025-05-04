import os

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

def save_and_generate(username, result_text):
    generate_profile_page(username, result_text)
    update_index(username)
    print(f"[✓] تم توليد صفحة لحساب @{username} وتحديث الصفحة الرئيسية.")

# مثال على الاستخدام:
# save_and_generate("a70igk", "البيانات هنا...")