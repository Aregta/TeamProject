import sys
import csv

def question_1(layoffs_file):
    # Add Q1 here: collect inputs, open/read/close the file, show results.
    pass


def question_2(staff_file):
    # Add Q2 here: collect inputs, open/read/close the file, show results.
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
