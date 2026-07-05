import requests

TICKER = "AFLT"
URL = f"https://moex.com{TICKER}"

def get_absolute_max_oi():
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
        print(f"Ошибка: {e}")
        return None

if __name__ == "__main__":
    result = get_absolute_max_oi()
    if result:
        strike, oi = result
        
        # Генерируем готовый код индикатора, который всегда содержит актуальный страйк
        pine_code = f"""//@version=5
indicator("Макс ОИ МосБиржа (Авто)", overlay=true)
// Автоматически обновлено скриптом. Макс ОИ: {oi}
strikeLevel = {strike}
var line oiLine = na
if barstate.islast
    line.delete(oiLine)
    oiLine := line.new(x1=bar_index - 100, y1=strikeLevel, x2=bar_index, y2=strikeLevel, extend=extend.right, color=color.red, width=3)
    var label oiLabel = na
    label.delete(oiLabel)
    oiLabel := label.new(x=bar_index, y=strikeLevel, text="Макс ОИ: {oi} (Страйк " + str.tostring(strikeLevel) + ")", color=color.red, textcolor=color.white, style=label.style_label_left)
"""
        # Сохраняем как готовый индикатор
        with open("indicator.txt", "w", encoding="utf-8") as f:
            f.write(pine_code)
            
        print(f"Индикатор успешно сгенерирован: Страйк {strike}, ОИ {oi}")
