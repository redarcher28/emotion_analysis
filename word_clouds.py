import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba
from collections import Counter
# 读取Excel文件
file_path = '多所高校互动姜萍_带行为属性_合并.xlsx'
data = pd.read_excel(file_path)

# 提取博文内容
text_data = data['博文内容'].dropna().tolist()
text = ' '.join(text_data)

# 进行分词（使用精确模式）
wordlist = jieba.cut(text, cut_all=False)
wordlist_space_split = ' '.join(wordlist)

# 去除多余的空格和无意义的字符
wordlist_space_split = ' '.join(wordlist_space_split.split())

# 统计词频
word_counts = Counter(wordlist_space_split.split())
# 过滤频率小于5的词
filtered_word_counts = {word: count for word, count in word_counts.items() if count >= 20}
# 扩展停用词列表
stopwords = {'ydl','月','第','岁','第','因为','曾','获','日','位','多所', '高校',
             '个', '只是', '互动', '的', '和', '是', '了', '在', '我', '也', '有', '就', '不', '人',
             '都', '一个', '上', '我们', '你', '为', '这', '他', '她', '它', '将', '与', '对', '被',
             '去','会','生姜','萍','等','属于','吧','说','能', '吗', '收起', 'd', '级', '届', '参加',
             '可以','名是','二十余','大家','那么','关注','获评','视频'}
keywords = [
    "邵阳学院", "学生", "入围", "决赛", "数学", "天才", "祝贺", "录取",
    "高校", "教育", "学术", "培养", "成绩", "天赋", "关注", "未来", "中考", "高考",
    "常熟理工", "浙江大学", "清华", "北大", "剑桥", "麻省理工", "博士生", "优秀毕业生", "数学建模", "荣誉",
    "博士", "江苏大学", "媒体", "热搜", "社会关注", "未成年人", "家长", "学校", "学习",
    "成长", "发展", "前途", "知识", "天才少女", "名校", "成就", "入学", "博弈", "精英", "伯乐"
]

# 将关键词添加到文本中以确保它们在词云中突显
keywords_text = ' '.join(keywords)
wordlist_space_split += ' ' + keywords_text

# 生成词云
wordcloud = WordCloud(font_path='simhei.ttf', stopwords=stopwords, background_color='white', width=800, height=600, max_words=30).generate(wordlist_space_split)

# 显示词云图
plt.figure(figsize=(10, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
