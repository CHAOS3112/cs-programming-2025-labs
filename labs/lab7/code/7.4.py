zones = [
    {"zone": "Sector-12", "active_from": 8, "active_to": 18},
    {"zone": "Deep Storage", "active_from": 0, "active_to": 24},
    {"zone": "Research Wing", "active_from": 9, "active_to": 17}
]
daytime_zones = list(filter(lambda z: z["active_from"] >= 8 and z["active_to"] <= 18, zones))
print(daytime_zones)
