# taiwan_stock_dashboard/service/stock_service.py

import json
import twstock
import os
import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

STOCK_FILE = resource_path('stocks.json')

def load_stock_list(filename=STOCK_FILE):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def save_stock_list(stock_list, filename=STOCK_FILE):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(stock_list, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Failed to write stocks.json:", e)

def fetch_stock_data(stock_list):
    result = []
    for stock_id in stock_list:
        stock = twstock.Stock(stock_id)
        if not stock.price or not stock.open:
            continue
        try:
            name = twstock.codes[stock_id].name
            current = stock.price[-1]
            prev_close = stock.price[-2]
            volume = stock.capacity[-1]
            open_price = stock.open[-1]
            pct = ((current - prev_close) / prev_close) * 100
            result.append([
                stock_id,
                name,
                f"{current:.2f}",
                f"{pct:+.2f}%",
                f"{prev_close:.2f}",
                f"{volume:,}",
                f"{open_price:.2f}"
            ])
        except Exception as e:
            print(f"Failed to fetch data for {stock_id}", e)
            continue
    return result


