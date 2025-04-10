def calculate_pvp_damage():
    """
    Calculates PvP damage and returns multiplied damage (before resistance)
    """
    
    print("\n=== PvP Damage Calculation ===")
    
    # Core stats
    proficiency = int(input("Enter proficiency: "))
    swing_speed = float(input("Enter weapon swing speed: "))  # New input
    wep_stat = int(input("Enter Weapon Stat: "))
    wep_scaling = float(input("Enter Weapon Scaling: "))
    wep_base = int(input("Enter Base Damage: "))
    
    # Armor penetration calculation
    armor_pen_input = float(input("Enter base armor penetration % (0-100): "))
    proficiency_pen = proficiency * 2.5
    total_armor_pen = armor_pen_input + proficiency_pen
    total_armor_pen_clamped = min(100, max(0, total_armor_pen))
    armor_pen = total_armor_pen_clamped / 100

    # Optional scaling stats
    has_secondary = input("Has Secondary Scaling (y/n): ").lower() == 'y'
    has_tertiary = input("Has Tertiary Scaling (y/n): ").lower() == 'y'

    wep_stat2 = wep_scaling2 = wep_stat3 = wep_scaling3 = 0
    if has_secondary:
        wep_stat2 = int(input("Enter Secondary Stat: "))
        wep_scaling2 = float(input("Enter Secondary Scaling: "))
    if has_tertiary:
        wep_stat3 = int(input("Enter Tertiary Stat: "))
        wep_scaling3 = float(input("Enter Tertiary Scaling: "))

    # Defense and modifiers
    has_bleed = input("Has Bleed (y/n): ").lower() == 'y'
    target_resist = min(100, max(0, float(input("Enter Target Resistance % (0-100): ")))) / 100

    # Base damage calculation
    stat_scaling = (wep_stat * wep_scaling) + \
                   (wep_stat2 * wep_scaling2) + \
                   (wep_stat3 * wep_scaling3)
    
    proficiency_factor = 1 + (proficiency * 0.065)
    base_damage = wep_base + (0.75 * wep_base * stat_scaling * proficiency_factor) / 1000

    # Apply bleed first
    raw_damage = base_damage * 1.3 if has_bleed else base_damage

    # Damage modifiers input
    total_modifier = 0.0
    while True:
        modifier = input("Enter damage modifier % (0-75, 'done' to finish): ").lower()
        if modifier == 'done':
            break
        try:
            mod_value = float(modifier)
            if mod_value < 0:
                print("! Negative modifiers not allowed")
                continue
            total_modifier = min(total_modifier + mod_value, 75)
        except ValueError:
            print("! Numbers only")

    # Apply modifiers
    multiplied_damage = raw_damage * (1 + total_modifier/100)

    # Resistance calculation
    effective_resist = target_resist * (1 - armor_pen)
    final_pvp_damage = multiplied_damage * (1 - effective_resist)

    # Calculate DPS
    dps = (final_pvp_damage * swing_speed) / 1.3 * 2

    print("\n=== PvP Results ===")
    print(f"{'Base Damage (Pre-Bleed):':<25} {base_damage:.1f}")
    print(f"{'Raw Damage (After Bleed):':<25} {raw_damage:.1f}")
    print(f"{'Damage Modifiers:':<25} +{total_modifier:.1f}%")
    print(f"{'Pre-Resist Damage:':<25} {multiplied_damage:.1f}")
    print(f"{'Final PvP Damage:':<25} {final_pvp_damage:.1f}")
    print(f"{'DPS:':<25} {dps:.1f}") 

    return multiplied_damage

def calculate_pve_damage(multiplied_damage):
    """
    CORRECTED PvE Formula:
    base_pve_damage = multiplied_damage * (1 + player_level * 0.26)
    """
    print("\n=== PvE Damage Calculation ===")
    
    # Player level input with clamping
    player_level = int(input("Enter player level (1-20): "))
    player_level = max(1, min(20, player_level))
    
    pve_multiplier = 1 + (player_level * 0.26)
    base_pve_damage = multiplied_damage * pve_multiplier
    
    # DvM input 
    dvM = -1.0
    while dvM < 0:
        try:
            dvM = float(input("Enter DvM % (0 for base damage, >=0): "))
            if dvM < 0:
                print("DvM cannot be negative!")
        except ValueError:
            print("Numbers only!")

    # Apply DvM
    final_pve_damage = base_pve_damage * (1 + dvM/100)
    
    attacks_needed = (1000 / final_pve_damage) if final_pve_damage > 0 else "∞"

    # Results display
    print("\n=== PvE Results ===")
    print(f"{'Player Level:':<20} {player_level}")
    print(f"{'PvE Multiplier:':<20} {pve_multiplier:.2f}x (Base 100% + {player_level * 26}%)")
    print(f"{'Base PvE Damage:':<20} {base_pve_damage:.1f}")
    print(f"{'DvM Bonus:':<20} +{dvM:.1f}%")
    print(f"{'Final PvE Damage:':<20} {final_pve_damage:.1f}")
    print(f"{'Attacks for 1000 HP:':<20} {round(attacks_needed, 1)}")
    
    return final_pve_damage

while True:
    pvp_multiplied = calculate_pvp_damage()
    calculate_pve_damage(pvp_multiplied)
    
    does_continue = input("\nContinue? (y/n): ").lower()
    if does_continue == 'n':
        break
