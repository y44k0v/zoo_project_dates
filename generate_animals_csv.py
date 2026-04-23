"""
generate_animals_csv.py
-----------------------
Generates a CSV file with 100 realistic zoo animals ready to be imported
into the Django zoo app's Animal table via the admin panel.

Usage:
    python generate_animals_csv.py

Output:
    animals_data.csv  (created in the same directory as this script)

CSV columns match the Animal model fields:
    name, age, weight, born_in_captivity, date_added
"""

import csv
import random
from datetime import date, timedelta

# ---------------------------------------------------------------------------
# Data pools
# ---------------------------------------------------------------------------

ANIMALS = [
    # (species_name, min_age, max_age, min_weight_kg, max_weight_kg)
    ("African Elephant",   5,  60,  2500, 6000),
    ("African Lion",       1,  16,   120,  250),
    ("African Penguin",    1,  20,     2,    4),
    ("Aldabra Giant Tortoise", 10, 150, 100, 250),
    ("American Bison",     2,  20,   400,  900),
    ("Amur Leopard",       1,  15,    25,   75),
    ("Amur Tiger",         1,  16,   100,  300),
    ("Andean Condor",      1,  70,     7,   15),
    ("Arabian Oryx",       1,  20,    65,  100),
    ("Arctic Fox",         1,   8,     3,    9),
    ("Asian Elephant",     5,  60,  2000,  5000),
    ("Asian Small-Clawed Otter", 1, 12, 1, 5),
    ("Bald Eagle",         1,  28,     3,    7),
    ("Black Rhinoceros",   3,  40,   800, 1400),
    ("Black-Footed Ferret", 1,  5,    0.6,   1),
    ("Blue-Tongued Skink", 1,  20,   0.3,   0.6),
    ("Bonobo",             2,  40,    30,   60),
    ("Bornean Orangutan",  3,  45,    30,   90),
    ("Brown Bear",         2,  25,   150,  360),
    ("California Sea Lion", 1, 20,    50,  300),
    ("Capybara",           1,   8,    35,   65),
    ("Cheetah",            1,  12,    35,   65),
    ("Chimpanzee",         2,  50,    32,   60),
    ("Chinese Giant Salamander", 5, 60, 20, 60),
    ("Clouded Leopard",    1,  11,    11,   23),
    ("Colobus Monkey",     1,  20,     7,   14),
    ("Common Hippopotamus", 5, 45,  1500, 3200),
    ("Crocodile Monitor",  2,  20,    10,   20),
    ("Dall Sheep",         1,  13,    60,  110),
    ("Dhole",              1,  10,    12,   20),
    ("Dromedary Camel",    3,  25,   400,  700),
    ("Dusky Leaf Monkey",  1,  20,     5,   9),
    ("Dwarf Mongoose",     1,   6,   0.2,  0.4),
    ("Eastern Bongo",      1,  19,   150,  405),
    ("Eclectus Parrot",    1,  30,   0.4,  0.6),
    ("Fennec Fox",         1,  14,     1,    2),
    ("Fossa",              2,  20,     5,   10),
    ("Galapagos Tortoise", 20, 170,   70,  250),
    ("Gentoo Penguin",     1,  20,     4,    8),
    ("Giant Anteater",     2,  14,    18,   39),
    ("Giant Panda",        3,  20,    75,  150),
    ("Giraffe",            2,  25,   750, 1200),
    ("Golden Lion Tamarin", 1, 15,   0.5,  0.8),
    ("Gorilla",            4,  40,    70,  200),
    ("Grant's Zebra",      2,  20,   175,  385),
    ("Gray Wolf",          1,  13,    25,   65),
    ("Greater Flamingo",   1,  40,     2,    4),
    ("Green Anaconda",     3,  30,    30,   90),
    ("Grizzly Bear",       2,  25,   150,  360),
    ("Hammerhead Shark",   3,  30,   150,  450),
    ("Harpy Eagle",        1,  35,     4,    9),
    ("Humboldt Penguin",   1,  25,     3,    6),
    ("Indian Rhinoceros",  4,  45,  1500, 2700),
    ("Jaguar",             1,  12,    56,  100),
    ("King Cobra",         3,  20,     3,    9),
    ("Komodo Dragon",      5,  30,    40,   90),
    ("Koala",              1,  18,     4,   15),
    ("Lar Gibbon",         2,  44,     4,    8),
    ("Lemur",              1,  20,     2,    4),
    ("Leopard",            1,  12,    28,   90),
    ("Loggerhead Sea Turtle", 15, 70, 70, 200),
    ("Long-Tailed Chinchilla", 1, 10, 0.4, 0.8),
    ("Lowland Tapir",      2,  30,   150,  300),
    ("Mandrill",           2,  20,    11,   37),
    ("Meerkat",            1,  10,   0.6,  0.9),
    ("Melagris Warthog",   1,  15,    50,  150),
    ("Moose",              2,  20,   270,  720),
    ("Mountain Gorilla",   4,  40,    70,  200),
    ("Nile Crocodile",     10, 70,   225,  750),
    ("North American River Otter", 1, 13, 5, 14),
    ("Ocelot",             1,  13,     8,   16),
    ("Okapi",              3,  30,   200,  350),
    ("Polar Bear",         3,  25,   200,  700),
    ("Prevost's Squirrel", 1,  10,   0.3,  0.5),
    ("Pronghorn Antelope", 1,  10,    40,   65),
    ("Pygmy Hippopotamus", 3,  40,   160,  270),
    ("Red Kangaroo",       1,  16,    18,   90),
    ("Red Panda",          1,  14,     3,    6),
    ("Red Wolf",           1,  14,    23,   40),
    ("Reticulated Python", 5,  25,    60,  160),
    ("Ring-Tailed Lemur",  1,  16,     2,    4),
    ("Rodrigues Fruit Bat", 1, 10,   0.3,  0.5),
    ("Royal Bengal Tiger", 2,  16,   100,  260),
    ("Scarlet Macaw",      1,  40,     1,  1.5),
    ("Secretary Bird",     1,  19,     2,    5),
    ("Serval",             1,  20,     9,   18),
    ("Siberian Crane",     1,  25,     4,    7),
    ("Sloth Bear",         2,  20,    55,  145),
    ("Snow Leopard",       2,  16,    22,   55),
    ("Sumatran Orangutan", 3,  45,    30,   90),
    ("Sun Bear",           2,  25,    25,   65),
    ("Tasmanian Devil",    1,   6,     4,   14),
    ("Thomson's Gazelle",  1,  10,    15,   35),
    ("Warthog",            1,  15,    50,  150),
    ("White Rhinoceros",   5,  45,  1400, 2300),
    ("Wolverine",          1,  13,     7,   25),
    ("Wombat",             1,  15,    20,   35),
]

# Zoos / enclosure locations used as part of name disambiguation
ENCLOSURE_SUFFIXES = [
    "", "", "", "", "",   # Most animals have no suffix (plain name)
    " (East)", " (West)", " (North)", " (South)",
    " II", " III",
]


def random_date(start_year: int = 2018, end_year: int = 2025) -> str:
    """Return a random date between Jan 1 of start_year and Dec 31 of end_year."""
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    delta = (end - start).days
    return (start + timedelta(days=random.randint(0, delta))).isoformat()


def generate_animals(n: int = 100) -> list[dict]:
    """
    Generate n animal records.

    Strategy:
    - Shuffle and cycle through the species pool so we get variety.
    - For repeated species add a disambiguation suffix.
    - Randomise age, weight, born_in_captivity, and date_added within
      realistic bounds for each species.
    """
    random.shuffle(ANIMALS)

    # Track how many times each species appears so we can add suffixes
    species_count: dict[str, int] = {}
    records: list[dict] = []

    for i in range(n):
        species = ANIMALS[i % len(ANIMALS)]
        name_base, min_age, max_age, min_w, max_w = species

        species_count[name_base] = species_count.get(name_base, 0) + 1
        count = species_count[name_base]

        # Add a suffix when the same species appears more than once
        if count == 1:
            name = name_base
        elif count == 2:
            name = f"{name_base} II"
        elif count == 3:
            name = f"{name_base} III"
        else:
            name = f"{name_base} {count}"

        age = random.randint(min_age, max_age)

        # Weight scaled loosely with age (young animals are lighter)
        age_fraction = (age - min_age) / max(max_age - min_age, 1)
        weight_range = max_w - min_w
        # Add ±15 % noise
        base_weight = min_w + weight_range * age_fraction
        noise = random.uniform(-0.15, 0.15) * weight_range
        weight = round(max(min_w, min(max_w, base_weight + noise)), 1)

        # Animals born in captivity are slightly more common in a managed zoo
        born_in_captivity = random.random() < 0.65

        date_added = random_date()

        records.append({
            "name": name,
            "age": age,
            "weight": weight,
            "born_in_captivity": born_in_captivity,
            "date_added": date_added,
        })

    # Sort by date_added so the CSV is easy to read chronologically
    records.sort(key=lambda r: r["date_added"])
    return records


def write_csv(records: list[dict], filepath: str = "animals_data.csv") -> None:
    fieldnames = ["name", "age", "weight", "born_in_captivity", "date_added"]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    print(f"✓  Written {len(records)} animals to '{filepath}'")


if __name__ == "__main__":
    animals = generate_animals(100)
    write_csv(animals)
