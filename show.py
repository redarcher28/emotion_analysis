from pyecharts import options as opts
from pyecharts.charts import Graph
import pandas as pd

# 加载节点和边数据
nodes_file = 'filtered_nodes_final.csv'
edges_file = 'filtered_edges_final.csv'

nodes_df = pd.read_csv(nodes_file)
edges_df = pd.read_csv(edges_file)

# 确认列名
if 'Count' in edges_df.columns:
    edges_df.rename(columns={'Count': 'Weight'}, inplace=True)

# 定义中心节点
center_nodes = ['支持', '反对', '娱乐化讨论', '理性讨论', '质疑']

# 创建节点和边的数据列表
nodes = []
for index, row in nodes_df.iterrows():
    if row['Id'] in center_nodes:
        nodes.append({
            "name": row['Id'],
            "symbolSize": 50,
            "itemStyle": {"color": "orange"}
        })
    else:
        nodes.append({
            "name": row['Id'],
            "symbolSize": 30,
            "itemStyle": {"color": "skyblue"}
        })

# 添加边并根据权重设置边的粗细
edges = []
for index, row in edges_df.iterrows():
    edges.append({
        "source": row['Source'],
        "target": row['Target'],
        "value": row['Weight'],
        "lineStyle": {"width": row['Weight']}
    })

# 创建Graph对象
graph = Graph()

# 添加节点和边，设置节点可拖拽
graph.add("", nodes, edges, repulsion=5000, edge_length=200, is_draggable=True)

# 设置全局配置项
graph.set_global_opts(
    title_opts=opts.TitleOpts(title="情感共现网络图"),
)

# 设置系列配置项
graph.set_series_opts(
    label_opts=opts.LabelOpts(is_show=True, position="right", formatter="{b}"),
    edge_label=opts.LabelOpts(
        is_show=True,
        position="middle",
        formatter="{c}",
        font_size=12,  # 可以根据需要调整字体大小
        color="black"  # 设置标签颜色
    )
)

# 渲染图表
graph.render("index.html")
