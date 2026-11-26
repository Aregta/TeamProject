
import csv
import argparse
import matplotlib.pyplot as plt


# Read employee data from the CSV file
def load_data(filename):
    data = []

    with open(filename, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Only include full company reports
            if row["Type"].strip() != "Full company":
                continue

            # Skip reports excluded from the dataset's graphs
            if row["Exclude from graph view"].strip().lower() == "true":
                continue

            # Skip missing employee counts
            if row["Staff count"].strip() == "":
                continue

            company = row["Company"].strip()
            date = row["Date"].strip()
            staff = int(float(row["Staff count"]))

            data.append([company, date, staff])

    # Sort reports by date
    data.sort(key=lambda row: row[1])

    return data


# Get reports for a company within the selected years
def filter_data(data, company, start, end):
    results = []

    for row in data:
        year = int(row[1][:4])

        if row[0].lower() == company.lower():
            if start <= year <= end:
                results.append(row)

    return results


# Calculate employee growth
def calculate_growth(reports):
    first = reports[0][2]
    latest = reports[-1][2]

    added = latest - first

    if first > 0:
        growth = added / first * 100
    else:
        growth = 0

    return first, latest, added, growth


# Display one company's employee growth
def show_company(data, company, start, end):
    reports = filter_data(data, company, start, end)

    if len(reports) < 2:
        print("Not enough reports for this company.")
        return

    dates = []
    employees = []

    print("\nEmployee history:", reports[0][0])
    print("Date          Employees")
    print("------------------------")

    for row in reports:
        print(row[1], "   ", row[2])

        dates.append(row[1])
        employees.append(row[2])

    first, latest, added, growth = calculate_growth(reports)

    print("\nFirst count:", first)
    print("Latest count:", latest)
    print("Employees added:", added)
    print("Growth:", round(growth, 1), "%")

    # Create a line graph
    plt.figure(figsize=(10, 6))
    plt.plot(dates, employees, marker="o")

    plt.title(reports[0][0] + " Employee Growth")
    plt.xlabel("Date")
    plt.ylabel("Number of Employees")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    plt.savefig("company_growth.png")
    plt.show()


# Compare all AI companies
def compare_companies(data, start, end):
    companies = []
    results = []

    # Get all unique company names
    for row in data:
        if row[0] not in companies:
            companies.append(row[0])

    for company in companies:
        reports = filter_data(data, company, start, end)

        # At least two reports are needed to calculate growth
        if len(reports) >= 2:
            first, latest, added, growth = calculate_growth(reports)

            results.append(
                [company, first, latest, added, growth]
            )

    if len(results) == 0:
        print("Not enough reports for the selected years.")
        return

    # Rank companies by employees added
    results.sort(key=lambda row: row[3], reverse=True)

    print("\nAI Company Employment Growth")
    print("Years:", start, "-", end)

    print(
        f"{'Company':<18}"
        f"{'First':>10}"
        f"{'Latest':>10}"
        f"{'Added':>10}"
        f"{'Growth %':>12}"
    )

    print("-" * 60)

    names = []
    added_counts = []

    for row in results:
        print(
            f"{row[0]:<18}"
            f"{row[1]:>10}"
            f"{row[2]:>10}"
            f"{row[3]:>10}"
            f"{row[4]:>11.1f}%"
        )

        names.append(row[0])
        added_counts.append(row[3])

    print("\nCompany with the largest increase:", results[0][0])

    # Create a bar graph
    plt.figure(figsize=(10, 6))
    plt.bar(names, added_counts)

    plt.title(
        "AI Company Employee Growth "
        + str(start) + "-" + str(end)
    )

    plt.xlabel("AI Company")
    plt.ylabel("Employees Added")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig("company_comparison.png")
    plt.show()


# Main program
def main():
    parser = argparse.ArgumentParser(
        description="AI Company Employment Growth"
    )

    parser.add_argument(
        "--file",
        default="ai_companies_staff_report.csv"
    )

    parser.add_argument(
        "--company",
        default="all"
    )

    parser.add_argument(
        "--start",
        type=int,
        default=2023
    )

    parser.add_argument(
        "--end",
        type=int,
        default=2026
    )

    args = parser.parse_args()

    if args.start > args.end:
        print("Start year cannot be greater than end year.")
        return

    try:
        data = load_data(args.file)
    except FileNotFoundError:
        print("CSV file not found:", args.file)
        return

    if args.company.lower() == "all":
        compare_companies(data, args.start, args.end)
    else:
        show_company(data, args.company, args.start, args.end)


if __name__ == "__main__":
    main()
