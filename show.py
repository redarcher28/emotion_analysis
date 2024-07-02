from pyecharts import options as opts
from pyecharts.charts import Graph, Page
from pyecharts.components import Table
from pyecharts.globals import ThemeType
import pandas as pd

# 加载节点和边数据
nodes_file = 'outcome/filtered_nodes_高校.csv'
edges_file = 'outcome/filtered_edges_高校.csv'

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
            "itemStyle": {"color": "orange"},
            "symbol": "diamond"  # 中心节点设置为菱形
        })
    else:
        color = "yellow" if row['Label'] == '行为属性' else "blue"
        shape = "circle" if row['Label'] == '行为属性' else "circle"
        nodes.append({
            "name": row['Id'],
            "symbolSize": 30,
            "itemStyle": {"color": color},
            "symbol": shape  # 根据节点类型设置形状
        })

# 添加边并根据权重设置边的粗细
edges = []
for index, row in edges_df.iterrows():
    weight = row['Weight']
    weight = max(1, min(weight, 10))  # 限制边的粗细在1到10之间
    edges.append({
        "source": row['Source'],
        "target": row['Target'],
        "value": row['Weight'],
        "lineStyle": {"width": weight}
    })

# 创建Graph对象
graph = Graph(init_opts=opts.InitOpts(width="1000px", height="800px"))

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

# 创建图例标注表格
table = Table()

# 添加表格内容
headers = ["颜色", "属性", "形状"]
rows = [
    ["黄色", "行为属性", "圆形"],
    ["蓝色", "主题属性", "矩形"]
]
table.add(headers, rows).set_global_opts(
    title_opts=opts.ComponentTitleOpts(title="颜色和形状标注")
)

# 渲染图表
page = Page(layout=Page.SimplePageLayout)
page.add(graph, table)
page.render("index.html")
