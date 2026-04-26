import json

def calculate_time_based_costs(target_hours=4):
    """Calculate enhancement costs to achieve target playtime"""

    # Load current data
    with open('data/upgrade_data.json', 'r') as f:
        data = json.load(f)

    enhancements = data['enhancements']

    # Game parameters
    base_income = 33  # Starting DPC + DPS
    target_seconds = target_hours * 3600  # Convert to seconds

    # Model player progression over time
    current_income = base_income
    total_time = 0
    time_per_purchase = []

    print(f"Target playtime: {target_hours} hours ({target_seconds} seconds)")
    print("Modeling progression with current costs...")

    for i, enhancement in enumerate(enhancements):
        cost = enhancement['cost']
        title = enhancement.get('title', f'Enhancement {i+1}')

        # Calculate time to earn this cost
        if current_income > 0:
            time_to_earn = cost / current_income
        else:
            time_to_earn = cost / base_income

        total_time += time_to_earn
        time_per_purchase.append(time_to_earn)

        print(".1f")

        # Apply enhancement benefits to income
        bonus = enhancement.get('bonus', 0) or 0
        save_key = enhancement.get('save_key')

        if save_key == 'ducksPerClick' or save_key == 'duckColor' or save_key == 'poolColor':
            current_income += bonus
        elif save_key == 'ducksPerSecond':
            current_income += bonus
        elif 'multiplier' in str(save_key):
            current_income *= (1 + bonus)
        elif save_key == 'magicalAutoClickers':
            current_income += 50  # Estimate auto-clicker contribution
        elif save_key == 'magicalAutoClickerSpeed':
            current_income *= 1.05  # Speed boost

        # General income growth
        current_income *= 1.02

    actual_hours = total_time / 3600
    print(".1f")
    print(".1f")

    # Now calculate what costs should be to achieve target time
    print(f"\nRecalculating costs for {target_hours} hour target...")

    # Reset for recalculation
    current_income = base_income
    total_time = 0
    new_costs = []

    target_time_per_purchase = target_seconds / len(enhancements)

    for i, enhancement in enumerate(enhancements):
        title = enhancement.get('title', f'Enhancement {i+1}')

        # Calculate new cost based on target time
        if i < 15:
            # Early game: keep nearly the same costs
            new_cost = int(enhancement['cost'] * 1.05)  # Max 5% increase
        else:
            # Mid and late game: apply full scaling
            scaling_factor = 1.5 + ((i - 15) * 0.1)  # 1.5x to 7.0x+
            new_cost = int(current_income * target_time_per_purchase * scaling_factor)

        # Ensure minimum cost and reasonable maximum
        new_cost = max(new_cost, 1000)
        new_cost = min(new_cost, 1000000000)  # Cap at 1 billion

        new_costs.append(new_cost)

        # Update income for next calculation
        bonus = enhancement.get('bonus', 0) or 0
        save_key = enhancement.get('save_key')

        if save_key == 'ducksPerClick' or save_key == 'duckColor' or save_key == 'poolColor':
            current_income += bonus
        elif save_key == 'ducksPerSecond':
            current_income += bonus
        elif 'multiplier' in str(save_key):
            current_income *= (1 + bonus)
        elif save_key == 'magicalAutoClickers':
            current_income += 50
        elif save_key == 'magicalAutoClickerSpeed':
            current_income *= 1.05

        current_income *= 1.02

    # Verify the new costs achieve target time
    print("\nVerifying new costs...")
    current_income = base_income
    total_time = 0

    for i, (enhancement, new_cost) in enumerate(zip(enhancements, new_costs)):
        time_to_earn = new_cost / current_income if current_income > 0 else new_cost / base_income
        total_time += time_to_earn

        # Update income
        bonus = enhancement.get('bonus', 0) or 0
        save_key = enhancement.get('save_key')

        if save_key == 'ducksPerClick' or save_key == 'duckColor' or save_key == 'poolColor':
            current_income += bonus
        elif save_key == 'ducksPerSecond':
            current_income += bonus
        elif 'multiplier' in str(save_key):
            current_income *= (1 + bonus)
        elif save_key == 'magicalAutoClickers':
            current_income += 50
        elif save_key == 'magicalAutoClickerSpeed':
            current_income *= 1.05

        current_income *= 1.02

    final_hours = total_time / 3600
    print(".1f")

    return new_costs

if __name__ == "__main__":
    costs = calculate_time_based_costs(target_hours=4)

    print("\nNew balanced enhancement costs:")
    for i, cost in enumerate(costs, 1):
        print(f"{i:2d}: {cost:,}")

    print("\nComparison with current costs:")
    with open('data/upgrade_data.json', 'r') as f:
        data = json.load(f)

    for i, (enh, new_cost) in enumerate(zip(data['enhancements'], costs)):
        old_cost = enh['cost']
        change = "↑" if new_cost > old_cost else "↓" if new_cost < old_cost else "="
        ratio = new_cost / old_cost if old_cost > 0 else 1
        print(f"{i+1:2d}: {enh['title'][:25]:25} | {old_cost:>10,} → {new_cost:>10,} {change} ({ratio:.1f}x)")