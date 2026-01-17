objects = [
    ("Containment Cell A", 4),
    ("Archive Vault", 1),
    ("Bio Lab Sector", 3),
    ("Observation Wing", 2)
]
sorted= sorted(objects, key=lambda x: x[1])
for i in sorted:
    print(f"{i[0]} - уровень угрозы: {i[1]}")