import tkinter as tk
from tkinter import ttk

dmg = (0, 0)  # Храним оба значения урона (PvP и PvE)
ret = [0, 0, 0, 0, 0, 0, 0, 0]

def update_label():
    """Обновление текста в Label с результатами"""
    txt =   f"PvP Damage: {dmg[0]:.1f}\nPvE Damage: {dmg[1]:.1f}\n" \
        f"{'Base Damage (Pre-Bleed):':<25} {ret[0]:.1f}\n" \
        f"{'Raw Damage (After Bleed):':<25} {ret[1]:.1f}\n" \
        f"{'Pre-Resist Damage:':<25} {ret[2]:.1f}\n" \
        f"{'Proficiency Armor Pen:':<25} {ret[3]:.1f}%\n" \
        f"{'Base Armor Pen:':<25} {ret[4]:.1f}%\n" \
        f"{'Total Armor Pen:':<25} {ret[5]:.1f}%\n" \
        f"{'Target Resistance:':<25} {ret[6]*100:.1f}%\n" \
        f"{'Effective Resistance:':<25} {ret[7]*100:.1f}%"
    pvp, pve = dmg
    result_label.config(text=txt)

def calculate_damage(stats, bleed_status):
    global ret 
    #ret = [0, 0, 0, 0, 0, 0, 0, 0]
    try:
        # Проверяем, что все необходимые значения есть
        if len(stats) < 12:
            stats += [0] * (12 - len(stats))
    except:
        stats = [0] * 12
    
    # Извлекаем и преобразуем параметры
    proficiency = int(stats[0])
    power = int(stats[1])
    wep_stat = int(stats[2])
    wep_scaling = float(stats[3])
    wep_base = int(stats[4])
    armor_pen_input = float(stats[5])
    
    # Расчет пробивания брони
    proficiency_pen = proficiency * 2.5
    total_armor_pen = armor_pen_input + proficiency_pen
    total_armor_pen_clamped = min(100, max(0, total_armor_pen))
    armor_pen = total_armor_pen_clamped / 100
    
    # Дополнительные параметры оружия
    wep_stat2 = int(stats[6])
    wep_scaling2 = float(stats[7])
    wep_stat3 = int(stats[8])
    wep_scaling3 = float(stats[9])
    wep_stat4 = int(stats[10])
    wep_scaling4 = float(stats[11])
    
    has_bleed = bleed_status.get() == 1
    target_resist = min(100, max(0, float(stats[12]))) / 100
    
    # Расчет базового урона
    stat_scaling = (wep_stat * wep_scaling) + \
                   (wep_stat2 * wep_scaling2) + \
                   (wep_stat3 * wep_scaling3) + \
                   (wep_stat4 * wep_scaling4)

    proficiency_factor = 1 + (proficiency * 0.065)
    base_damage = wep_base + (0.75 * wep_base * stat_scaling * proficiency_factor) / 1000
    raw_damage = base_damage * 1.3 if has_bleed else base_damage
    
    # Модификаторы урона
    total_modifier = min(stats[13], 75) if len(stats) > 11 else 0
    multiplied_damage = raw_damage * (1 + total_modifier/100)
    
    # Финальный расчет урона
    effective_resist = target_resist * (1 - armor_pen)
    final_damage_PvP = multiplied_damage * (1 - effective_resist)
    final_damage_PvE = final_damage_PvP * 0.31 * power
    ret = [base_damage, raw_damage, multiplied_damage, proficiency_pen, armor_pen_input, total_armor_pen_clamped, target_resist*100, effective_resist*100]
    return final_damage_PvP, final_damage_PvE

def validate_number(input_str):
    """Валидация ввода - только числа"""
    if input_str == "":
        return True
    try:
        float(input_str)
        return True
    except ValueError:
        return False
    
def calc_damage():
    """Сбор данных и расчет урона"""
    global dmg
    stats = []
    for entry in entries:
        value = entry.get()
        stats.append(float(value) if value else 0.0)
    
    dmg = calculate_damage(stats, bleed_var)
    update_label()

# Создаем основное окно
root = tk.Tk()
root.title('Deepwoken Damage Calculator')
root.geometry("500x700")  # Увеличили ширину для лучшего отображения

# Регистрируем функцию валидации
validate_cmd = root.register(validate_number)

# Списки для элементов интерфейса
entries = []
labels = []
entry_names = [
    'Proficiency:',
    'Power:',
    'Weapon stat:',
    'Weapon scaling:',
    'Base Damage:',
    'Base armor PEN:',
    'Secondary stat:',
    'Sec scaling:',
    'Tertiary stat:',
    'Tert scaling:',
    'Tetra stat:',
    'Tetra scaling:',
    'Target Resistance:',
    'Damage modifier:'
]

# Создаем поля ввода и подписи
for i, name in enumerate(entry_names):
    # Метки параметров
    label = ttk.Label(root, text=name)
    label.place(x=20, y=20 + i*35)
    labels.append(label)
    
    # Поля ввода
    entry = ttk.Entry(root, validate="key", validatecommand=(validate_cmd, '%P'))
    entry.place(x=180, y=20 + i*35, width=50)
    entries.append(entry)

# Чекбокс для bleed
bleed_var = tk.IntVar()
bleed_check = ttk.Checkbutton(root, text="Bleed", variable=bleed_var)
bleed_check.place(x=180, y=20 + 14*35)

# Кнопка расчета
calculate_btn = ttk.Button(root, text="Calculate Damage", command=calc_damage)
calculate_btn.place(x=100, y=20 + 15*35, width=150)

# Label для вывода результата
txt =   f"PvP Damage: {dmg[0]:.1f}\nPvE Damage: {dmg[1]:.1f}\n" \
        f"{'Base Damage (Pre-Bleed):':<25} {ret[0]:.1f}\n" \
        f"{'Raw Damage (After Bleed):':<25} {ret[1]:.1f}\n" \
        f"{'Pre-Resist Damage:':<25} {ret[2]:.1f}\n" \
        f"{'Proficiency Armor Pen:':<25} {ret[3]:.1f}%\n" \
        f"{'Base Armor Pen:':<25} {ret[4]:.1f}%\n" \
        f"{'Total Armor Pen:':<25} {ret[5]:.1f}%\n" \
        f"{'Target Resistance:':<25} {ret[6]*100:.1f}%\n" \
        f"{'Effective Resistance:':<25} {ret[7]*100:.1f}%"
       
result_label = ttk.Label(root, text=txt, 
                        font=('Arial', 10, 'bold'), 
                        justify='left',
                        background='lightgray')
result_label.place(x=250, y=20, width=230, height=170)

root.mainloop()
