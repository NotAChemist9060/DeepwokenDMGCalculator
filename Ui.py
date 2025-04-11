import tkinter as tk
from tkinter import ttk

# Глобальная переменная для хранения урона
dmg = (0, 0)  # Теперь храним оба значения урона (PvP и PvE)

def update_label(*args):
    """Обновление текста в Label с результатами"""
    pvp, pve = dmg
    result_label.config(text=f"PvP Damage: {pvp:.1f}\nPvE Damage: {pve:.1f}")

def calculate_damage(stats):
    try:
        i = stats[12]
    except:
        stats = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    proficiency = int(stats[0])
    power = int(stats[1])
    wep_stat = int(stats[2])
    wep_scaling = float(stats[3])
    wep_base = int(stats[4])
    armor_pen_input = float(stats[5])
    
    proficiency_pen = proficiency * 2.5
    total_armor_pen = armor_pen_input + proficiency_pen
    total_armor_pen_clamped = min(100, max(0, total_armor_pen))
    armor_pen = total_armor_pen_clamped / 100
    
    wep_stat2 = int(stats[6])
    wep_scaling2 = float(stats[7])
    wep_stat3 = int(stats[8])
    wep_scaling3 = float(stats[9])
    
    has_bleed = stats[10] == 1
    target_resist = min(100, max(0, float(stats[11]))) / 100
    
    stat_scaling = (wep_stat * wep_scaling) + \
                  (wep_stat2 * wep_scaling2) + \
                  (wep_stat3 * wep_scaling3)
    
    proficiency_factor = 1 + (proficiency * 0.065)
    base_damage = wep_base + (0.75 * wep_base * stat_scaling * proficiency_factor) / 1000
    raw_damage = base_damage * 1.3 if has_bleed else base_damage
    
    total_modifier = min(stats[12], 75)
    multiplied_damage = raw_damage * (1 + total_modifier/100)
    
    effective_resist = target_resist * (1 - armor_pen)
    final_damage_PvP = multiplied_damage * (1 - effective_resist)
    final_damage_PvE = final_damage_PvP * 0.31 * power
    
    return final_damage_PvP, final_damage_PvE

def validate_number(input_str):
    if input_str == "":
        return True
    try:
        float(input_str)
        return True
    except ValueError:
        return False
    
def calc_damage():
    global dmg
    stats = []
    for entry in entries:
        value = entry.get()
        stats.append(float(value) if value else 0.0)
    
    dmg = calculate_damage(stats)
    update_label()  # Явно обновляем Label после расчета

# Создаем основное окно
root_1 = tk.Tk()
root_1.title('Deepwoken damage calculator')
root_1.geometry("300x600")  # Увеличили высоту для отображения двух строк урона

# Регистрируем функцию валидации
validate_cmd = root_1.register(validate_number)

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
    'Sec stat:',
    'Sec scaling:',
    'Tert stat:',
    'Tert scaling:',
    'Bleed(1/0):',
    'Target Resistance:',
    'Damage modifier:'
]

# Создаем поля ввода и подписи
for i in range(13):
    label = ttk.Label(root_1, text=entry_names[i])
    label.place(x=20, y=20 + i*35)
    labels.append(label)
    
    entry = ttk.Entry(root_1, validate="key", validatecommand=(validate_cmd, '%P'))
    entry.place(x=130, y=20 + i*35, width=30)
    entries.append(entry)

# Кнопка расчета
calculate_btn = ttk.Button(root_1, text="Calculate", command=calc_damage)
calculate_btn.place(x=110, y=20 + 13*35, width=80)

# Label для вывода результата (две строки)
result_label = ttk.Label(root_1, text="PvP Damage: 0\nPvE Damage: 0", 
                        font=('Arial', 10), justify='left')
result_label.place(x=20, y=20 + 14*35, width=260, height=50)

root_1.mainloop()
