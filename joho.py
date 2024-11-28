from numpy import var
import streamlit as st
st.title("初めてのstreamlit")
st.write("これから作品を作っていきます")
text=st.text_input("あなたの名前を教えてください")
st.write("あなたの名前は,"+text+"です")
condition=st.slider("あなたの今の調子は？",0,100,50)
st.write("コンディション：",condition)
option=st.selectbox("好きな数字を教えてください",list(["１番","２番","３番","４番"]))
st.write("あなたが選択したのは,"+option+"です")
import time
st.sidebar.write("プログレスバーの表示")
latest_iteration = st.empty() #空コンテンツと一緒に変数を作成 bar = st.progress (0) #プログレスを作る 値は0
bar=st.progress(0)
for i in range(100):
 latest_iteration.text(f'読み込み中{i+1}') #空のIterationにテキストを入れていく
 bar.progress(i+1) #barの中身をぐいぐい増やしていく
 time.sleep(0.01)
left_column, right_column = st.columns(2) 
button = left_column.button("右カラムに文字を表示") 
if button:
 right_column.write("ここは右カラムです")

from PIL import Image 
img = Image.open("S__139558930_0.jpg")
st.image(img, caption='生活場面', use_column_width=True)

import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.rand(100,2)/[50,50] + [35.69,139.70],columns = ['lat','lon',])
st.map(df)
st.table(df)
import numpy as np
df = pd.DataFrame(
np.random.rand(20,3), #20行3列
columns = ['a','b','c']
)
#表として表示する
st.table(df.style.highlight_max(axis=0))

#表からグラフ化 bar line area

st.bar_chart(df)