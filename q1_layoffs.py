# Q1 helper functions: AI-related layoffs by industry
# Data: AI Layoff Tracker - https://www.ailayofftracker.com/data
# Azeem Hussaini - Team Dhaka

import csv
import matplotlib.pyplot as plt


def load_layoffs(filename):
    data = []

    file = open(filename, "r", encoding="utf-8-sig")
    reader = csv.reader(file)
    next(reader)  # skip the header

    for row in reader:
        if len(row) < 4:
            continue

        year = int(row[0].strip()[:4])
        company = row[1].strip()
        industry = row[2].strip()
        jobs = row[3].strip()

        if jobs.isdigit():
            jobs = int(jobs)
        else:
            jobs = 0  # no exact number given

        data.append([year, company, industry, jobs])

    file.close()
    return data


def get_industries(data):
    industries = []

    for row in data:
        if row[2] not in industries:
            industries.append(row[2])

    industries.sort()
    return industries


def show_industries(data, chosen, start, end):
    results = []

    for industry in chosen:
        layoffs = 0
        jobs = 0

        for row in data:
            if row[2] == industry and start <= row[0] <= end:
                layoffs = layoffs + 1
                jobs = jobs + row[3]

        results.append([jobs, industry, layoffs])

    results.sort(reverse=True)  # most jobs cut first

    total = 0
    for result in results:
        total = total + result[0]

    if total == 0:
        print("\nNo layoffs found for those industries and years.")
        return

    print(f"\nAI-related layoffs, {start}-{end}")
    print(f"Total jobs cut: {total:,}\n")
    print(f"{'Rank':<6}{'Industry':<20}{'Layoffs':>8}{'Jobs cut':>11}{'Share':>9}")

    names = []
    jobs_cut = []

    rank = 1
    for jobs, industry, layoffs in results:
        share = jobs / total * 100
        print(f"{rank:<6}{industry:<20}{layoffs:>8}{jobs:>11,}{share:>8.1f}%")
        rank = rank + 1

        names.append(industry)
        jobs_cut.append(jobs)

    print(f"\nHardest hit: {results[0][1]} with {results[0][0]:,} jobs cut.")

    # Create a bar graph
    plt.figure(figsize=(10, 6))
    bars = plt.bar(names, jobs_cut, width=0.6)
    plt.bar_label(bars, fmt="{:,.0f}")  # show the number on each bar
    plt.xlim(-1, len(names))  # keep bars thin when only a few are chosen

    plt.title("AI-Related Layoffs by Industry " + str(start) + "-" + str(end))
    plt.xlabel("Industry")
    plt.ylabel("Jobs Cut")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig("industry_layoffs.png")
    plt.show()
