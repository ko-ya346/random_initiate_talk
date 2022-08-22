"""
処理流れ

csvファイル読み込み、なければ自前のサンプルデータ読み込み
データ表示
番組名、MC絞り込み機能
"""
import numpy as np
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid


URL = (
    "https://drive.google.com/file/d/1rmZoK6ZCrLxiGIL58aIKlvP4vDLMr2Ip/view?usp=sharing"
)
KEY = st.secrets.GoogleDriveApiKey.key


@st.cache
def load_data():
    path = f"https://www.googleapis.com/drive/v3/files/{URL.split('/')[-2]}?alt=media&key={KEY}"
    df = pd.read_csv(path)

    return df


@st.cache
def load_upload_data(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        assert list(df.columns.values) == [
            "番組名",
            "MC",
            "セリフ",
        ], "アップロードしたファイルの列名は(番組名, MC, セリフ)となっていません"

        return df
    except:
        return


st.title("Random Initiate Talk")
uploaded_file = st.file_uploader("csvファイルアップロード", type="csv")
uploaded_df = load_upload_data(uploaded_file)
if uploaded_df is None:
    st.write("アップロードしたファイルを読み込めませんでした")

using_data = st.radio("どのデータを使う？", ("デフォルトのデータ", "アップロードしたデータ"))
if using_data == "デフォルトのデータ" or uploaded_df is None:
    df = load_data()
else:
    df = uploaded_df

st.subheader("Initiate Talk Data")

AgGrid(df, fit_columns_on_grid_load=True)  # 列幅自動調整

random_index = None
if st.button("クリックするとランダムに話題を振ります"):
    random_index = np.random.randint(0, df.shape[0])


if random_index is not None:
    program_name, mc, serif = df.loc[random_index]
    st.subheader(f"番組名: {program_name}")
    st.subheader(f"MC: {mc}")
    st.subheader(f"セリフ: {serif}")
