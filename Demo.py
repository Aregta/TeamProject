import sys
from q2_growth import load_data, show_company, compare_companies
from q1_layoffs import load_layoffs, get_industries, show_industries
from q3_comparison import compare_employment

def question_1(layoffs_file):
    print("\nAI Layoffs by Industry")

    try:
        data = load_layoffs(layoffs_file)
    except FileNotFoundError:
        print("Layoffs file not found.")
        return

    industries = get_industries(data)

    print("\nAvailable industries:")

    for industry in industries:
        print("-", industry)

    choice = input("\nEnter industries, separated by commas (or all): ").strip()

    if choice.lower() == "all":
        chosen = industries
    else:
        chosen = []
        for typed in choice.split(","):
            for industry in industries:
                if typed.strip().lower() == industry.lower() and industry not in chosen:
                    chosen.append(industry)

    if len(chosen) == 0:
        print("No matching industries.")
        return

    try:
        start = int(input("Enter start year: "))
        end = int(input("Enter end year: "))
    except ValueError:
        print("Please enter valid years.")
        return

    if start > end:
        print("Start year cannot be greater than end year.")
        return

    show_industries(data, chosen, start, end)


def question_2(staff_file):
    print("\nAI Company Employee Growth")

    try:
        data = load_data(staff_file)
    except FileNotFoundError:
        print("Staff file not found.")
        return

    companies = []

    for row in data:
        if row[0] not in companies:
            companies.append(row[0])

    print("\nAvailable companies:")

    for company in companies:
        print("-", company)

    company = input("\nEnter company name (or all): ").strip()

    try:
        start = int(input("Enter start year: "))
        end = int(input("Enter end year: "))
    except ValueError:
        print("Please enter valid years.")
        return

    if start > end:
        print("Start year cannot be greater than end year.")
        return

    if company.lower() == "all":
        compare_companies(data, start, end)
    else:
        show_company(data, company, start, end)


def question_3(layoffs_file, staff_file):
    print("\nAI Layoffs vs Employment Growth")

    try:
        start = int(input("Enter start year: "))
        end = int(input("Enter end year: "))
    except ValueError:
        print("Please enter valid years.")
        return

    if start > end:
        print("Start year cannot be greater than end year.")
        return

    if start < 2023 or end > 2026:
        print("Please enter years between 2023 and 2026.")
        return

    years = list(range(start, end + 1))
    layoffs = {year: 0 for year in years}
    staff = {}

    try:
        with open(layoffs_file, encoding="utf-8-sig") as file:
            reader = csv.DictReader(file, skipinitialspace=True)

            for row in reader:
                year = int(row["date"][:4])
                count = row["employees_affected_exact"].strip()

                if year in layoffs and count:
                    layoffs[year] += int(count)

        with open(staff_file, encoding="utf-8-sig") as file:
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

    except FileNotFoundError:
        print("Dataset file not found.")
        return

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

    plt.figure()

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
    plt.close()



def show_help():
    print("\nRun: python3 Demo.py layoffs.csv staff.csv")
    print("Use your filenames: layoffs first, staff second.")
    print("1: AI-related layoffs by industry")
    print("2: Employee growth at AI companies")
    print("3: Compare layoffs and employment growth")
    print("0: Exit")


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 Demo.py layoffs.csv staff.csv")
        return

    layoffs_file = sys.argv[1]
    staff_file = sys.argv[2]

    while True:
        print("\nAI AND EMPLOYMENT")
        print("1. Question 1")
        print("2. Question 2")
        print("3. Question 3")
        print("4. Help")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            question_1(layoffs_file)
        elif choice == "2":
            question_2(staff_file)
        elif choice == "3":
            question_3(layoffs_file, staff_file)
        elif choice == "4":
            show_help()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Enter 0, 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
