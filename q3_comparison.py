
import csv
from datetime import datetime
import matplotlib.pyplot as plt

start = int(input("Start year (2023-2026): "))
end = int(input("End year (2023-2026): "))

if not 2023 <= start <= end <= 2026:
    quit("Invalid year range.")

years = list(range(start, end + 1))
layoffs = {year: 0 for year in years}

# Read AI-related layoffs
with open("AILayoff.csv", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file, skipinitialspace=True)
    for row in reader:
        year = int(row["date"][:4])
        count = row["employees_affected_exact"].strip()
        if year in layoffs and count:
            layoffs[year] += int(count)

# Read AI company employee counts
staff = {}
with open("Public view.csv", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file, skipinitialspace=True)
    for row in reader:
        if row["Type"].strip() != "Full company":
            continue
        count = row["Staff count"].replace(",", "").strip()
        if not count:
            continue
        date = datetime.strptime(row["Date"].strip(), "%m/%d/%Y")
        key = (row["Company"].strip(), date.year)
        if key not in staff or date > staff[key][0]:
            staff[key] = (date, int(float(count)))

# Compare year-by-year results
growth = []
print(f"\n{'Year':<8}{'Layoffs':>12}{'Staff change':>16}")

for year in years:
    changes = [
        staff[(company, year)][1] - staff[(company, year - 1)][1]
        for company, y in staff
        if y == year and (company, year - 1) in staff
    ]
    total = sum(changes) if changes else None
    growth.append(total)
    shown = f"{total:+,}" if total is not None else "N/A"
    print(f"{year:<8}{layoffs[year]:>12,}{shown:>16}")

# Create comparison graph
plt.plot(years, [layoffs[y] for y in years],
         marker="o", label="Reported AI layoffs")
plt.plot(years, [float("nan") if g is None else g for g in growth],
         marker="o", label="AI company staff change")
plt.xticks(years)
plt.xlabel("Year")
plt.ylabel("Employees")
plt.title("AI Layoffs vs AI Company Employment Changes")
plt.legend()
plt.tight_layout()
plt.savefig("q3_comparison.png")
plt.show()

