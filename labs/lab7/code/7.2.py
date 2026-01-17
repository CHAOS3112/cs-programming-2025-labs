staff_shifts = [
    {"name": "Dr. Shaw", "shift_cost": 120, "shifts": 15},
    {"name": "Agent Torres", "shift_cost": 90, "shifts": 22},
    {"name": "Researcher Hall", "shift_cost": 150, "shifts": 10}
]
total_costs = list(map(lambda x: x["shift_cost"] *x["shifts"], staff_shifts))
max_cost = max(total_costs)
print("Общая стоимость работы каждого сотрудника:", total_costs)
print("Максимальная стоимость:", max_cost)
