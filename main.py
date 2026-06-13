import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

class ForeignCurrencyDepositAnalyzer:
    def __init__(self, initial_hkd=1000000):
        """
        初始化外汇定存分析器
        
        Parameters:
        initial_hkd: 初始港币金额
        """
        self.initial_hkd = initial_hkd
        self.results = {}
    
    def calculate_deposit_returns(self, currency_name, buy_rate, sell_rate, 
                                 #currency_interest_rate, hkd_interest_rate=0.023,
                                 currency_interest_rate, hkd_interest_rate=0.0025,
                                 exchange_rate_range=None, years=1):
        """
        计算外币定存与港币定存的收益对比
        
        Parameters:
        currency_name: 外币名称
        buy_rate: 港币兑外币汇率 (1 HKD = X foreign currency)
        sell_rate: 外币兑港币汇率 (1 foreign currency = X HKD)
        currency_interest_rate: 外币年利率
        hkd_interest_rate: 港币年利率 (默认2.3%)
        exchange_rate_range: 汇率波动范围 (min, max)，如不提供则使用当前汇率
        years: 存款年限
        """
        # 港币定存收益
        hkd_future_value = self.initial_hkd * (1 + hkd_interest_rate) ** years
        
        # 外币定存收益计算
        # 换汇成外币 using buy rate
        foreign_currency_amount = self.initial_hkd / buy_rate
        
        # 外币定存后金额
        foreign_currency_future = foreign_currency_amount * (1 + currency_interest_rate) ** years
        
        # 确定汇率范围
        if exchange_rate_range is None:
            # 如果没有提供汇率范围，假设汇率不变
            rate_min = rate_max = sell_rate  # 转换为外币兑港币汇率
        else:
            rate_min, rate_max = exchange_rate_range
        
        # 使用汇率范围计算换回港币金额
        hkd_from_foreign_min = foreign_currency_future * rate_min
        hkd_from_foreign_max = foreign_currency_future * rate_max
        hkd_from_foreign_target = foreign_currency_future * sell_rate
        
        # 计算收益差异
        advantage_min = hkd_from_foreign_min - hkd_future_value
        advantage_max = hkd_from_foreign_max - hkd_future_value
        advantage_target = hkd_from_foreign_target - hkd_future_value
        
        # 计算盈亏平衡汇率
        # 外币定存收益 = 港币定存收益 时的汇率
        break_even_rate = foreign_currency_future / hkd_future_value
        
        # 存储结果
        result = {
            'currency': currency_name,
            'hkd_future_value': hkd_future_value,
            'foreign_currency_future': foreign_currency_future,
            'hkd_from_foreign_min': hkd_from_foreign_min,
            'hkd_from_foreign_max': hkd_from_foreign_max,
            'hkd_from_foreign_target': hkd_from_foreign_target,
            'advantage_target': advantage_target,
            'advantage_min': advantage_min,
            'advantage_max': advantage_max,
            'break_even_rate': break_even_rate,
            'current_rate': buy_rate,  # 当前外币/HKD汇率
            'rate_range': (rate_min, rate_max)
        }
        
        self.results[currency_name] = result
        print(f"{result=}")
        return result
    
    def analyze_multiple_currencies(self, currencies_data):
        """
        分析多种外币
        
        Parameters:
        currencies_data: 字典列表，每个字典包含外币分析参数
        """
        for currency_data in currencies_data:
            self.calculate_deposit_returns(**currency_data)
        
        return self.results
    
    def generate_comparison_table(self):
        """生成对比表格"""
        if not self.results:
            return "没有可用的分析结果"
        
        data = []
        for currency, result in self.results.items():
            data.append({
                '货币': currency,
                '港币定存收益(HKD)': f"{result['hkd_future_value']:,.2f}",
                '外币定存最低收益(HKD)': f"{result['hkd_from_foreign_min']:,.2f}",
                '外币定存最高收益(HKD)': f"{result['hkd_from_foreign_max']:,.2f}",
                '外币定存目標收益(HKD)': f"{result['hkd_from_foreign_target']:,.2f}",
                '最低收益差(HKD)': f"{result['advantage_min']:,.2f}",
                '最高收益差(HKD)': f"{result['advantage_max']:,.2f}",
                '目標收益差(HKD)': f"{result['advantage_target']:,.2f}",
                '盈亏平衡汇率': f"{result['break_even_rate']:.4f}",
                '当前汇率': f"{result['current_rate']:.4f}"
            })
        
        df = pd.DataFrame(data)
        return df
    
    def plot_comparison(self):
        """绘制收益对比图"""
        if not self.results:
            print("没有可用的分析结果")
            return
        
        currencies = list(self.results.keys())
        hkd_values = [self.results[currency]['hkd_future_value'] for currency in currencies]
        foreign_min = [self.results[currency]['hkd_from_foreign_min'] for currency in currencies]
        foreign_max = [self.results[currency]['hkd_from_foreign_max'] for currency in currencies]
        foreign_target = [self.results[currency]['hkd_from_foreign_target'] for currency in currencies]
        
        x = np.arange(len(currencies))
        width = 0.2
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # 创建条形图
        bars1 = ax.bar(x - width, hkd_values, width, label='HKD fixed deposit return', color='blue')
        bars2 = ax.bar(x, foreign_min, width, label='Minimum Yield of Foreign Currency Fixed Deposit', color='darkred')
        bars3 = ax.bar(x + width, foreign_target, width, label='Target Yield of Foreign Currency Fixed Deposit', color='gray')
        bars4 = ax.bar(x + 2*width, foreign_max, width, label='Maximum Yield of Foreign Currency Fixed Deposit', color='green')
        
        
        # 添加数值标签
        def add_value_labels(bars):
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:,.0f}',
                        ha='center', va='bottom', fontsize=9)
        
        add_value_labels(bars1)
        add_value_labels(bars2)
        add_value_labels(bars3)
        add_value_labels(bars4)
        
        ax.set_xlabel('Currency Type')
        ax.set_ylabel('Revenue (HKD)')
        ax.set_title('Comparison between HKD and Foreign Dollars')
        ax.set_xticks(x)
        labels = [f"{currency} ({self.results[currency]['break_even_rate']:.4f})" for currency in currencies]
        ax.set_xticklabels(labels)
        # ax.set_xticklabels(currencies)
        ax.legend()
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    def get_recommendation(self, currency_name):
        """根据分析结果提供投资建议"""
        if currency_name not in self.results:
            return "未找到该货币的分析结果"
        
        result = self.results[currency_name]
        current_rate = result['current_rate']
        break_even = result['break_even_rate']
        rate_min, rate_max = result['rate_range']
        
        # 判断是否总是有利
        always_advantage = result['advantage_min'] > 0
        
        if always_advantage:
            return f"✅ 投资建议：选择{currency_name}定存\n" \
                   f"理由：在汇率波动范围内({rate_min:.4f}-{rate_max:.4f} {currency_name}/HKD)，" \
                   f"{currency_name}定存收益始终高于港币定存，预期额外收益为{result['advantage_min']:,.0f}至{result['advantage_max']:,.0f} HKD"
        else:
            # 判断当前汇率是否有利
            if current_rate <= break_even:
                return f"⚠️ 投资建议：谨慎选择{currency_name}定存\n" \
                       f"理由：当前汇率{current_rate:.4f} {currency_name}/HKD高于盈亏平衡点{break_even:.4f}，" \
                       f"如果汇率维持在当前水平，{currency_name}定存可能不如港币定存"
            else:
                return f"✅ 投资建议：选择{currency_name}定存\n" \
                       f"理由：当前汇率{current_rate:.4f} {currency_name}/HKD低于盈亏平衡点{break_even:.4f}，" \
                       f"预期额外收益为{result['advantage_min']:,.0f}至{result['advantage_max']:,.0f} HKD"

# 使用示例
def main(years=1, initial_hkd=1000000):
    # 初始化分析器
    analyzer = ForeignCurrencyDepositAnalyzer(initial_hkd)
    
    # 定义多种外币分析参数
    currencies_to_analyze = [
        #{
        #    'currency_name': 'USD',
        #    'buy_rate': 7.804025316258126,
        #    'sell_rate':  7.804025316258126,
        #    'currency_interest_rate': 0.044,    # 4.4%
        #    'exchange_rate_range': (7.75, 7.85) # USD/HKD 汇率范围
        #    ,'years': years
        #},
        {
            'currency_name': 'USD',
            'buy_rate': 1.5349,
            'sell_rate': 1.5167,
            'currency_interest_rate': 0.089,    # 8.9%
            'exchange_rate_range': (1.51, 1.54) # USD/HKD 汇率范围
            ,'years': years
        },
        {
            'currency_name': 'GBP',
            'buy_rate': 10.22467,
            'sell_rate': 10.133973,
            'currency_interest_rate': 0.118,    # 3.4%
            'exchange_rate_range': (9.4205, 10.8252) # GBP/HKD 汇率范围
            ,'years': years
        },
        {
            'currency_name': 'EUR',
            'buy_rate':  9.047301099608976,
            'sell_rate': 9.047301099608976,
            'currency_interest_rate': 0.069,    # 2.9%
            'exchange_rate_range': (7.9251, 9.287)   # EUR/HKD 汇率范围
            ,'years': years
        },
        {
            'currency_name': 'AUD',
            'buy_rate': 5.07658,
            'sell_rate': 5.0418,
            'currency_interest_rate': 0.118,    # 11.8%
            'exchange_rate_range': (4.5943, 5.2144)   # AUD/HKD 汇率范围
            ,'years': years
        },
        {
            'currency_name': 'CNY',
            'buy_rate': 1.0918222513374822,
            'sell_rate': 1.0918222513374822,
            'currency_interest_rate': 0.034,    # 3.4%
            'exchange_rate_range': (1.0548, 1.098)   # CNY/HKD 汇率范围
            ,'years': years
        }
    ]
    
    # 执行分析
    results = analyzer.analyze_multiple_currencies(currencies_to_analyze)
    
    # 生成对比表格
    print("=" * 80)
    print("港币与外币定存收益对比分析")
    print("=" * 80)
    comparison_table = analyzer.generate_comparison_table()
    print(comparison_table)
    
    # 显示投资建议
    print("\n" + "=" * 80)
    print("投资建议")
    print("=" * 80)
    for currency in results.keys():
        recommendation = analyzer.get_recommendation(currency)
        print(f"\n{recommendation}")
    
    # 绘制图表
    print("\n生成收益对比图表...")
    analyzer.plot_comparison()

# 快速分析单一货币的函数
def quick_analyze(currency_name, buy_rate, sell_rate, currency_interest_rate, 
                  hkd_interest_rate=0.023, exchange_rate_range=None, initial_hkd=1000000):
    """
    快速分析单一货币与港币的定存收益对比
    """
    analyzer = ForeignCurrencyDepositAnalyzer(initial_hkd=initial_hkd)
    result = analyzer.calculate_deposit_returns(
        currency_name, buy_rate, sell_rate, currency_interest_rate,
        hkd_interest_rate, exchange_rate_range
    )
    
    print(f"\n{currency_name} vs HKD 定存分析:")
    print(f"港币定存收益: {result['hkd_future_value']:,.2f} HKD")
    print(f"{currency_name}定存收益范围: {result['hkd_from_foreign_min']:,.2f} - {result['hkd_from_foreign_max']:,.2f} HKD")
    print(f"收益差异: {result['advantage_min']:,.2f} - {result['advantage_max']:,.2f} HKD")
    print(f"盈亏平衡汇率: {result['break_even_rate']:.4f} {currency_name}/HKD")
    print(f"当前汇率: {result['current_rate']:.4f} {currency_name}/HKD")
    
    recommendation = analyzer.get_recommendation(currency_name)
    print(f"\n{recommendation}")
    
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='外汇定存收益分析工具')
    parser.add_argument('--years', type=float, default=1.0,
                       help='存款年限 (支持小数如1.5年)')
    parser.add_argument('--initial_hkd', type=float, default=1000000.0, help="初始港币金额")
    years = parser.parse_args().years
    initial_hkd = parser.parse_args().initial_hkd
    # 运行完整分析
    main(years, initial_hkd)
    
    # 快速分析示例
    print("\n" + "=" * 80)
    print("快速分析示例 - 美元定存")
    print("=" * 80)
    quick_analyze(
        currency_name="USD",
        buy_rate=7.804025316258126,
        sell_rate=7.804025316258126,
        currency_interest_rate=0.044,
        exchange_rate_range=(7.75, 7.85)
    )
