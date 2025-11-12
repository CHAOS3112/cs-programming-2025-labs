students = [("Анна", [5, 4, 5]), ("Иван", [3, 4, 4]), ("Мария", [5, 5, 5])]
average_grades = {}
for name, grades in students:
    average = sum(grades) / len(grades)
    average_grades[name] = average 
best_student = max(average_grades, key=average_grades.get)
best_average = average_grades[best_student]
print(f"{best_student} имеет наивысший средний балл: {best_average}")