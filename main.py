from pywebio.input import input, select, FLOAT, PASSWORD
from pywebio.output import *
from pywebio import start_server
import json
import os

DATA_FILE = "data.json"

# تحميل البيانات
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": {"admin": "1234"}, "transactions": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# حفظ البيانات
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

data = load_data()

# تسجيل الدخول
def login():
    while True:
        user = input("اسم المستخدم")
        password = input("كلمة المرور", type=PASSWORD)

        if user in data["users"] and data["users"][user] == password:
            put_success("تم تسجيل الدخول")
            return user
        else:
            put_error("بيانات خاطئة")

# القائمة الرئيسية
def main_menu():
    while True:
        clear()
        put_text("📊 برنامج محاسبي متطور")

        choice = select("اختر", [
            "➕ إضافة عملية",
            "📋 عرض العمليات",
            "💰 عرض الرصيد",
            "📊 تقرير"
        ])

        if choice == "➕ إضافة عملية":
            add_transaction()
        elif choice == "📋 عرض العمليات":
            show_transactions()
        elif choice == "💰 عرض الرصيد":
            show_balance()
        elif choice == "📊 تقرير":
            report()

# إضافة عملية
def add_transaction():
    t_type = select("نوع العملية", ["إيراد", "مصروف"])
    amount = input("المبلغ", type=FLOAT)
    note = input("ملاحظة")

    data["transactions"].append({
        "type": t_type,
        "amount": amount,
        "note": note
    })

    save_data(data)
    put_success("تم الحفظ")

# عرض العمليات
def show_transactions():
    if not data["transactions"]:
        put_warning("لا توجد عمليات")
        return

    table = [["النوع", "المبلغ", "ملاحظة"]]

    for t in data["transactions"]:
        table.append([t["type"], t["amount"], t["note"]])

    put_table(table)

# الرصيد
def show_balance():
    balance = 0
    for t in data["transactions"]:
        if t["type"] == "إيراد":
            balance += t["amount"]
        else:
            balance -= t["amount"]

    put_text(f"💰 الرصيد: {balance}")

# تقرير
def report():
    income = sum(t["amount"] for t in data["transactions"] if t["type"] == "إيراد")
    expense = sum(t["amount"] for t in data["transactions"] if t["type"] == "مصروف")

    put_text(f"📈 إجمالي الإيرادات: {income}")
    put_text(f"📉 إجمالي المصروفات: {expense}")
    put_text(f"💰 الصافي: {income - expense}")

# التطبيق الرئيسي
def app():
    login()
    main_menu()
import os
start_server(app, port=int(os.environ.get("PORT", 8080)))
