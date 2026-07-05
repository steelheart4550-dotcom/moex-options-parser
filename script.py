import requests
import os

TICKER = "AFLT"
URL = f"https://moex.com{TICKER}"

def get_max_oi_strike():
    try:
        response = requests.get(URL, timeout=15)
        data = response.json()
        
        columns = data['securities']['columns']
        rows = data['securities']['data']
        
        open_pos_idx = columns.index('OPENPOSITION')
        strike_idx = columns.index('STRIKE')
        
        max_oi = 0
        target_strike = 0.0
        
        for row in rows:
            oi = row[open_pos_idx]
            if oi and oi > max_oi:
                max_oi = oi
                target_strike = row[strike_idx]
                
        return float(target_strike), int(max_oi)
    except Exception as e:
        print(f"Ошибка получения данных: {e}")
        return None

if __name__ == "__main__":
    result = get_max_oi_strike()
    if result:
        strike, oi = result
        # Записываем значение в простом формате, понятном для TradingView
        with open("data.txt", "w") as f:
            f.write(f"{strike}")
        print(f"Обновлено: Страйк {strike} (ОИ: {oi})")
