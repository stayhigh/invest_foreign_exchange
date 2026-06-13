"""
Purpose:
    打印复利利率表
Usage:
    python roi_cal.py --start_rate 0.01 --end_rate 0.12 --step 0.01 --years 5
"""
import numpy as np
import argparse

def generate_interest_table(start_rate, end_rate, step, years):
    """Generate a matrix of compound interest factors using vectorization."""
    rates = np.arange(start_rate, end_rate + step, step)
    years_arr = np.arange(1, years + 1)
    # Broadcasting: (N, 1) ** (M,) -> (N, M) matrix computed in C
    factors = (1 + rates[:, np.newaxis]) ** years_arr
    return rates, factors

def print_table(rates, factors):
    """Print the interest table with aligned formatting."""
    header = f"{'Rate':<10}" + "".join(f"{'Y'+str(y):<12}" for y in range(1, factors.shape[1] + 1))
    print(header)
    print("-" * len(header))
    
    for r, row in zip(rates, factors):
        print(f"{r:<10.4f}" + "".join(f"{val:<12.4f}" for val in row))

def validate_inputs(start_rate, end_rate, step, years):
    """Validate all input parameters."""
    if start_rate < 0 or end_rate < 0:
        raise ValueError("Interest rates cannot be negative")
    if step <= 0:
        raise ValueError("Step must be positive")
    if years <= 0:
        raise ValueError("Years must be a positive integer")
    if start_rate > end_rate:
        print(f"⚠️  Warning: start_rate ({start_rate}) > end_rate ({end_rate}). Swapping values.")
        start_rate, end_rate = end_rate, start_rate
    return start_rate, end_rate, step, years

def main():
    parser = argparse.ArgumentParser(description='打印复利利率表')
    parser.add_argument('--start_rate', type=float, default=0.02, help='起始利率 (默认: 0.02)')
    parser.add_argument('--end_rate', type=float, default=0.10, help='结束利率 (默认: 0.10)')
    parser.add_argument('--step', type=float, default=0.005, help='步长 (默认: 0.005)')
    parser.add_argument('--years', type=int, default=10, help='年份上限 (默认: 10)')

    args = parser.parse_args()

    try:
        start_rate, end_rate, step, years = validate_inputs(
            args.start_rate, args.end_rate, args.step, args.years
        )
        rates, factors = generate_interest_table(start_rate, end_rate, step, years)
    print_table(rates, factors)
    except ValueError as e:
        print(f"❌ Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()

