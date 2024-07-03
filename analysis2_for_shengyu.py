import pandas as pd

# 加载新的数据
new_data_file = 'Professor_Welcome_Jiang_Ping.xlsx'
df_new = pd.read_excel(new_data_file)

# 合并主题属性和行为属性的关键词
attributes_keywords = {
    "社会议题": ["天才少女", "教育制度", "发展方向"],
    "教育话题": ["中专", "浙大", "教育资源", "特招"],
    "特定人物及相关方": ["姜萍", "姜萍老师", "支持者"],
    "其他社会成员": ["网友", "学生", "教师"],
    "回应": ["姜萍回应", "官方回应", "专家分析", "社会反应"],
    "未来展望": ["未来发展", "长远影响", "展望"],
    "质疑声": ["质疑", "反对", "不满"],
    "支持声": ["支持", "鼓励", "认可"],
    "娱乐化讨论": ["娱乐化", "戏谑", "调侃"],
    "理性讨论": ["理性", "分析", "讨论"]
}

behavior_keywords = {
    '支持': ['鼓励', '喜爱', '团结', '支持', '赞同', '期待'],
    '反对': ['谴责', '反感', '批评', '不满', '失望', '反对'],
    '质疑': ['疑问', '怀疑', '黑幕', '疑惑', '不解', '质问'],
    '理性讨论': ['客观陈述', '分析', '解释', '说明'],
    '娱乐化讨论': ['调剂', '搞笑', '吐槽', '哈哈', '笑死', '段子']
}

# 合并所有关键词
all_keywords = {**attributes_keywords, **behavior_keywords}

# 创建节点和边的数据列表
nodes = []
edges = []

# 创建节点
for attr in all_keywords.keys():
    nodes.append({"Id": attr, "Label": attr})

# 创建边
for index, row in df_new.iterrows():
    content = row['博文内容']
    behavior = row['行为属性']
    for attr, keywords in all_keywords.items():
        for keyword in keywords:
            if keyword in content:
                edges.append({"Source": behavior, "Target": attr, "Weight": 1})

# 转换为DataFrame
nodes_df = pd.DataFrame(nodes)
edges_df = pd.DataFrame(edges)

# 聚合边的权重
edges_agg = edges_df.groupby(['Source', 'Target'], as_index=False).count()
edges_agg.rename(columns={'Weight': 'Count'}, inplace=True)

# 去除行为属性节点与行为属性节点之间的边
edges_agg = edges_agg[~edges_agg['Source'].isin(behavior_keywords.keys()) | ~edges_agg['Target'].isin(behavior_keywords.keys())]

# 找出被使用的节点
included_nodes = set(edges_agg['Source']).union(set(edges_agg['Target']))

# 过滤未使用的节点
filtered_nodes_df = nodes_df[nodes_df['Id'].isin(included_nodes)]

# 保存为CSV文件
filtered_nodes_df.to_csv('outcome/filtered_nodes_教授欢迎.csv', index=False)
edges_agg.to_csv('outcome/filtered_edges_教授欢迎.csv', index=False)

