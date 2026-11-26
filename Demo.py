import sys
import csv
from q2_growth import load_data, show_company, compare_companies
def question_1(layoffs_file):
    # Add Q1 here: collect inputs, open/read/close the file, show results.
    pass


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
    pass


def question_3(layoffs_file, staff_file):
    # Add Q3 here: collect inputs, open/read/close both files, show results.
    pass


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
