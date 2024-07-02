import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table

# 定义文件路径列表
file_paths = [
    "outcome/filtered_edges_常熟理工.csv",
    "outcome/filtered_edges_gao_xiao.csv",
    "outcome/filtered_edges_浙大回应.csv",
    "outcome/filtered_edges_教授欢迎.csv",
    "outcome/filtered_edges_pinglun.csv"
]

# 读取CSV文件并将其存储在一个列表中
dfs = [pd.read_csv(file) for file in file_paths]

# 打印每个DataFrame的前五行以验证数据加载正确
print(dfs[0].head())
print(dfs[1].head())
print(dfs[2].head())
print(dfs[3].head())
print(dfs[4].head())

# 初始化一个空列表用于存储最终的数据表
final_table = []

# 定义数据集名称与其对应阶段的映射
dataset_names = ["常熟理工欢迎姜萍", "多所高校互动", "浙江大学第一阶段（浙大回应）", "浙江大学第二阶段（教授欢迎）", "浙江大学三阶段（教授评论）"]

# 遍历每个DataFrame
for i, df in enumerate(dfs):
    # 按Target分组并汇总每个Target的计数
    grouped_df = df.groupby("Target").sum(numeric_only=True).reset_index()
    for index, row in grouped_df.iterrows():
        # 仅选择特定的主题属性
        if row["Target"] in ["教育话题", "特定人物及相关方", "支持声", "其他社会成员", "质疑声"]:
            topic = row["Target"]
            count = row["Count"]
            # 将数据添加到最终的数据表中
            final_table.append([dataset_names[i], topic, count])

# 创建一个包含最终数据表的DataFrame
final_df = pd.DataFrame(final_table, columns=["主题", "主题属性", "数量"])

# 将数量列转换为整数类型
final_df["数量"] = final_df["数量"].astype(int)
# 添加一个总计列，按主题分组汇总数量
final_df["总计"] = final_df.groupby("主题")["数量"].transform("sum")

# 最终的数据表生成为Excel文件
final_df.to_excel("outcome/final_table.xlsx", index=False)

# 打印生成的DataFrame以验证
print(final_df)



