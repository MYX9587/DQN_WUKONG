import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def load_data_from_directory(directory, prefix):
    """从指定目录加载以指定前缀命名的 CSV 数据文件，并获取每个文件的最后一行 Reward 值。"""
    all_files = [f for f in os.listdir(directory) if f.endswith('.csv') and f.startswith(prefix)]
    rewards = []
    for file in all_files:
        file_path = os.path.join(directory, file)
        try:
            df = pd.read_csv(file_path)
            if 'Reward' in df.columns:
                last_reward = df['Reward'].iloc[-1]  # 获取最后一行的 Reward 值
                rewards.append(last_reward)
                print(f"读取文件: {file_path}, 最后一个 Reward 值: {last_reward}")
            else:
                print(f"警告: 文件中不包含 'Reward' 列")
        except Exception as e:
            print(f"无法读取文件 {file_path}: {e}")
    return rewards

def plot_total_rewards(rewards, save_path):
    """绘制每局结束时的总奖励分曲线。"""
    if rewards:  # 确保有数据可以绘制
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, len(rewards) + 1), rewards, marker='o')
        plt.xlabel('Episode')
        plt.ylabel('Reward')
        plt.title('Rewards per Episode')
        plt.grid(True)
        plt.savefig(save_path)
        plt.close()
        print(f"奖励曲线图已保存到 {save_path}")
    else:
        print("没有奖励数据可绘制。")

def main(directory, prefix):
    """主函数，生成奖励曲线图和数据文件。"""
    rewards = load_data_from_directory(directory, prefix)
    
    if rewards:
        # 生成奖励曲线图
        plot_total_rewards(rewards, os.path.join(directory + "/image", f'total_rewards_curve_{prefix}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'))
    else:
        print(f"没有找到以 '{prefix}' 前缀命名的有效奖励数据文件。")

if __name__ == "__main__":
    # 替换为你保存数据的目录
    data_directory = './data'
    
    # 固定的前缀类型
    prefix_type = 'episode_'  # 或 'overall_rewards'
    
    main(data_directory, prefix_type)