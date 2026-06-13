import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="대한민국 여론분석기",
    page_icon="📊",
    layout="wide"
)

# -------------------
# CSS
# -------------------

st.markdown("""
<style>

.main{
    background-color:#111111;
}

.block-container{
    padding-top:1rem;
}

.title{
    text-align:center;
    font-size:48px;
    font-weight:800;
    color:white;
}

.subtitle{
    text-align:center;
    color:#cccccc;
    margin-bottom:20px;
}

.keyword-btn button{
    width:100%;
}

.result-box{
    padding:20px;
    border-radius:15px;
    background:#1e1e1e;
    border:1px solid #444;
}

</style>
""", unsafe_allow_html=True)

# -------------------
# 상단 배너
# -------------------

left, center, right = st.columns([2,4,2])

with left:
    st.image("assets/candle.jpg", use_container_width=True)

with center:

    st.markdown(
        """
        <div class="title">
        대한민국 여론분석기
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="subtitle">
        대한민국 주요 이슈와 여론조사 현황
        </div>
        """,
        unsafe_allow_html=True
    )

with right:
    st.image("assets/flag.jpg", use_container_width=True)

st.divider()

# -------------------
# 실시간 키워드
# -------------------

trending = [
    "대통령",
    "국민의힘",
    "더불어민주당",
    "삼성전자",
    "부동산"
]

st.subheader("🔥 실시간 관심 키워드")

cols = st.columns(len(trending))

selected_keyword = None

for i, keyword in enumerate(trending):

    if cols[i].button(keyword):
        selected_keyword = keyword

# -------------------
# 검색창
# -------------------

search_input = st.text_input(
    "키워드 입력",
    placeholder="예: 대통령"
)

keyword = selected_keyword if selected_keyword else search_input

st.divider()

# -------------------
# 중앙선관위 버튼
# -------------------

st.link_button(
    "중앙선거여론조사심의위원회 바로가기",
    "https://www.nesdc.go.kr"
)

st.divider()

# -------------------
# 결과
# -------------------

if keyword:

    st.header(f"📊 {keyword}")

    st.markdown(
        f"""
        <div class='result-box'>
        <h3>{keyword} 분석 결과</h3>

        현재 버전은 디자인 시연용 버전입니다.

        추후 기능:
        <ul>
            <li>중앙선관위 여론조사 자동 검색</li>
            <li>최근 1개월 추세 분석</li>
            <li>조사기관별 비교</li>
            <li>꺾은선 그래프</li>
            <li>조사 원문 링크 제공</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        f"'{keyword}' 관련 여론조사가 검색되면 "
        "이 위치에 그래프가 표시됩니다."
    )

else:

    st.markdown(
        """
        ### 👋 사용 방법

        1. 키워드를 입력하세요.
        2. 또는 실시간 관심 키워드를 클릭하세요.
        3. 향후 버전에서는 중앙선관위 여론조사를 자동 분석합니다.
        """
    )
