"""
Purpose:
    打印利率表
Usage:
    python roi_cal.py --start_rate 0.01 --end_rate 0.12 --step 0.01 --years 5
"""
import numpy as np
import argparse

def print_interest_table(start_rate, end_rate, step, years):
    # 打印表头
    print(f"{'Rate':<10}", end="")
    for year in range(years):
        print(f"{'Year ' + str(year):<15}", end="")
    print()
    # 打印数据
    for r in np.arange(start_rate, end_rate, step):
        print(f"{r:<10.4f}", end="")
        for i in range(years):
            print(f"{(1 + r) ** i:<15.4f}", end="")
        print()

def main():
    parser = argparse.ArgumentParser(description='打印利率表')
    parser.add_argument('--start_rate', type=float, default=0.02, help='起始利率 (默认: 0.02)')
    parser.add_argument('--end_rate', type=float, default=0.10, help='结束利率 (默认: 0.10)')
    parser.add_argument('--step', type=float, default=0.005, help='步长 (默认: 0.005)')
    parser.add_argument('--years', type=int, default=10, help='年份上限 (默认: 10)')

    args = parser.parse_args()

    print_interest_table(args.start_rate, args.end_rate, args.step, args.years)

if __name__ == "__main__":
    main()
