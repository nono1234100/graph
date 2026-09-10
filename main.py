import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    layout="wide"
)

# 앱 메인 제목
st.title("영화 데이터 그래프 도감 1 - 시간")

# 데이터 로드 함수
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # 8자리 숫자로 된 날짜 열을 진짜 날짜 형태로 변환
    df["날짜"] = pd.to_datetime(df["날짜"].astype(str), format="%Y%m%d")
    return df

df = load_data()

# ── ① 영화별 일관객 변화 ──────────────────────────────────────────
st.header("① 영화별 일관객 변화")
st.write("영화들 하나 선택하고, 박스오피스에 등장한 기간 동안 일일 관객수가 어떻게 변했는지 살펴봅니다.")

# 영화 선택 드롭다운
movie_list = sorted(df["영화명"].dropna().unique())
selected_movie = st.selectbox("🎬 영화를 선택하세요.", movie_list)

if selected_movie:
    # 선택한 영화 데이터 필터링 및 날짜순 정렬
    movie_df = df[df["영화명"] == selected_movie].sort_values("날짜")
    
    # Plotly 선 그래프 생성 (사진과 동일한 제목 및 축 라벨 반영)
    fig = px.line(
        movie_df,
        x="날짜",
        y="일관객",
        title=f"{selected_movie}의 날짜별 일관객 변화",
        labels={"날짜": "날짜", "일관객": "일관객"},
        markers=True
    )
    
    # 이미지처럼 호버 시 [날짜: YYYY-MM-DD / 일관객: OOO명] 세로 배치 표기
    fig.update_traces(
        hovertemplate="%{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra></extra>"
    )
    
    # 마우스 가이드선(점선) 활성화 및 호버 스타일 설정
    fig.update_layout(
        hovermode="x",
        xaxis=dict(showspikes=True, spikethickness=1, spikecolor="gray", spikemode="across"),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    # Streamlit에 그래프 출력
    st.plotly_chart(fig, use_container_width=True)
    
    # '이 그래프로 알 수 있는 것' 하단 문구 자리
    st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")

# ── 앞으로 그래프 2, 3, 4, 5가 이 아래에 추가됩니다 ──────────
