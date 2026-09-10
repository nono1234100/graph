import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

# 앱 제목 및 기본 설명
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown("1년치 일별 박스오피스 데이터를 바탕으로 시간 흐름에 따른 영화 관객 수 및 상영 지표의 변화를 시각화합니다.")

# 데이터 로드 함수 (Streamlit 캐싱 적용)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # 8자리 숫자 형태의 '날짜' 열을 진짜 datetime 객체로 변환
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

st.divider()

# ==========================================
# 구역 1: 영화별 일관객수 변화 추이
# ==========================================
st.header("📌 구역 1. 영화별 일관객수 변화 추이")

# 영화 선택 드롭다운 (가나다순 정렬)
movie_list = sorted(df['영화명'].dropna().unique())
selected_movie = st.selectbox("분석할 영화를 선택하세요:", movie_list)

if selected_movie:
    # 선택한 영화 데이터 추출 및 날짜순 정렬
    filtered_df = df[df['영화명'] == selected_movie].sort_values('날짜')
    
    # Plotly 선 그래프 생성
    fig = px.line(
        filtered_df,
        x='날짜',
        y='일관객',
        title=f"[{selected_movie}] 일별 관객수 추이",
        labels={'날짜': '날짜', '일관객': '일일 관객수(명)'},
        markers=True
    )
    
    # 마우스 오버(호버) 시 날짜와 관객수가 직관적으로 보이도록 설정
    fig.update_traces(
        hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객수:</b> %{y:,.0f}명<extra></extra>"
    )
    
    # 레이아웃 정돈 및 X축 통합 호버 설정
    fig.update_layout(
        xaxis_title="날짜",
        yaxis_title="일관객수 (명)",
        hovermode="x unified"
    )
    
    # Streamlit 화면에 그래프 출력
    st.plotly_chart(fig, use_container_width=True)
    
    # 그래프 하단 알 수 있는 것 문구 안내 박스
    st.info(f"💡 **이 그래프로 알 수 있는 것:** {selected_movie}의 상영 기간 동안 개봉일 직후 관객 폭발력, 주말/평일 관객 차이, 그리고 차트아웃(상영 종료) 시점까지의 관객 감소 추이를 한눈에 확인할 수 있습니다.")

st.divider()

# ==========================================
# 구역 2: (향후 그래프 추가를 위한 확장 구역)
# ==========================================
st.header("📌 구역 2. [추가 예정]")
st.caption("앞으로 시간 축과 관련된 새로운 분석 그래프가 이곳에 추가될 예정입니다.")
