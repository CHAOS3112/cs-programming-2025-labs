incidents = [
    {"id": 101, "staff": 4},
    {"id": 102, "staff": 12},
    {"id": 103, "staff": 7},
    {"id": 104, "staff": 20}
]
top= sorted(incidents, key=lambda x: x["staff"], reverse=True)[:3]
print(top)