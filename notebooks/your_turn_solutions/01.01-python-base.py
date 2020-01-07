# preparation
participants = [
    {"name": "Marc Jaubert", "age": 24},
    {"name": "Loïc Pomeroy", "age": 32},
    {"name": "Émeric Ponce", "age": 39},
    {"name": "Auguste Rapace", "age": 45},
    {"name": "Valéry Baume", "age": 26},
    {"name": "Hugues Badeaux", "age": 23},
    {"name": "Baudouin Pascal", "age": 46},
    {"name": "Gaspard Joguet", "age": 38},
    {"name": "Hubert Emmanuelli", "age": 35},
    {"name": "Laurent Mignard", "age": 21},
]

# solution
groups = {"A": 0, "B": 0}

for participant in participants:
    print(f"{participant['name']}: {participant['age']}")
    if participant["age"] > 35:
        groups["B"] += 1
    else:
        groups["A"] += 1

print(f"group A: {groups['A']}")
print(f"group B: {groups['B']}")
