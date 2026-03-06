import re
import json


def to_number(s: str) -> float:
    # "1 200,00" -> 1200.00
    return float(s.replace(" ", "").replace(",", "."))


with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

lines = [line.strip() for line in text.splitlines() if line.strip()]

items = []
i = 0

while i < len(lines):
    # Ищем номер позиции: "1." / "2." / ...
    if re.fullmatch(r"\d+\.", lines[i]):
        # следующая строка = название товара
        if i + 1 >= len(lines):
            break
        name = lines[i + 1]

        # следующая строка после названия:
        # "2,000 x 154,00"
        if i + 2 < len(lines):
            qty_price_line = lines[i + 2]
            m_qp = re.fullmatch(r"([\d,]+)\s*x\s*([\d\s]+,\d{2})", qty_price_line)
        else:
            m_qp = None

        # следующая строка после qty_price_line:
        # "308,00" или "1 200,00"
        if i + 3 < len(lines):
            total_line = lines[i + 3]
            m_total = re.fullmatch(r"[\d\s]+,\d{2}", total_line)
        else:
            m_total = None

        if m_qp and m_total:
            qty = m_qp.group(1)
            unit_price = m_qp.group(2)
            line_total = total_line

            items.append({
                "name": name,
                "quantity": to_number(qty),
                "unit_price": to_number(unit_price),
                "line_total": to_number(line_total)
            })

            # пропускаем блок:
            # номер
            # название
            # qty x price
            # total
            # Стоимость
            # total
            i += 6
            continue

    i += 1


# Способ оплаты
payment_method = None
payment_amount = None

m_payment = re.search(r"(Банковская карта|Наличные):\s*([\d\s]+,\d{2})", text)
if m_payment:
    payment_method = m_payment.group(1)
    payment_amount = to_number(m_payment.group(2))

# Итого
grand_total = None
m_total = re.search(r"ИТОГО:\s*([\d\s]+,\d{2})", text)
if m_total:
    grand_total = to_number(m_total.group(1))

# Дата и время
date = None
time = None
m_datetime = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})", text)
if m_datetime:
    date = m_datetime.group(1)
    time = m_datetime.group(2)

# Адрес
address = None
m_address = re.search(r"г\.\s*Нур-султан,.*", text)
if m_address:
    address = m_address.group(0)

# Название филиала
branch = None
m_branch = re.search(r"Филиал\s+(.+)", text)
if m_branch:
    branch = m_branch.group(1).strip()

# БИН
bin_value = None
m_bin = re.search(r"БИН\s+(\d+)", text)
if m_bin:
    bin_value = m_bin.group(1)

# Чек
receipt_number = None
m_receipt = re.search(r"Чек №(\d+)", text)
if m_receipt:
    receipt_number = m_receipt.group(1)

# Кассир
cashier = None
m_cashier = re.search(r"Кассир\s+(.+)", text)
if m_cashier:
    cashier = m_cashier.group(1).strip()

# Считаем сумму по позициям
calculated_total = sum(item["line_total"] for item in items)

result = {
    "branch": branch,
    "bin": bin_value,
    "receipt_number": receipt_number,
    "cashier": cashier,
    "date": date,
    "time": time,
    "payment_method": payment_method,
    "payment_amount": payment_amount,
    "grand_total": grand_total,
    "calculated_total": round(calculated_total, 2),
    "address": address,
    "items": items
}

print(json.dumps(result, ensure_ascii=False, indent=2))
