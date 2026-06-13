import streamlit as st

st.set_page_config(
    page_title="대한민국 여론분석기",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# 이미지
# -----------------------------

CANDLE_IMAGE = "https://i.pinimg.com/736x/b9/52/2f/b9522f96d451eac189ad2a3d31510b13.jpg"

FLAG_IMAGE = "https://img1.newsis.com/2025/02/22/NISI20250222_0001776155_web.jpg?rnd=20250222165036"

# -----------------------------
# CSS
# -----------------------------

st.markdown("""
<style>

.main {
    background-color:#0e1117;
}

.title {
    text-align:center;
    font-size:52px;
    font-weight:800;
    color:white;
}

.subtitle {
    text-align:center;
    color:#c0c0c0;
    margin-bottom:20px;
}

.result-box {
    padding:20px;
    border-radius:15px;
    border:1px solid #444;
    background:#1a1a1a;
}

.keyword-title {
    text-align:center;
    font-size:24px;
    font-weight:700;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# session state
# -----------------------------

if "keyword" not in st.session_state:
    st.session_state.keyword = ""

# -----------------------------
# 상단 배너
# -----------------------------

left, center, right = st.columns([2,4,2])

with left:
    st.image(CANDLE_IMAGE, use_container_width=True)

with center:

    st.markdown(
        """
        <div class='title'>
        대한민국 여론분석기
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class='subtitle'>
        대한민국 주요 이슈 및 여론조사 분석 플랫폼
        </div>
        """,
        unsafe_allow_html=True
    )

with right:
    st.image(FLAG_IMAGE, use_container_width=True)

st.divider()

# -----------------------------
# 실시간 키워드
# -----------------------------

st.markdown(
    "<div class='keyword-title'>🔥 실시간 관심 키워드</div>",
    unsafe_allow_html=True
)

keywords = [
    "대통령",
    "국민의힘",
    "더불어민주당",
    "삼성전자",
    "부동산"
]

cols = st.columns(5)

for i, kw in enumerate(keywords):

    if cols[i].button(
        kw,
        use_container_width=True
    ):
        st.session_state.keyword = kw
        st.rerun()

st.write("")

# -----------------------------
# 검색창
# -----------------------------

search = st.text_input(
    "키워드를 입력하세요",
    value=st.session_state.keyword,
    placeholder="예: 대통령"
)

if search != st.session_state.keyword:
    st.session_state.keyword = search

st.divider()

# -----------------------------
# 중앙선관위
# -----------------------------

st.link_button(
    "📋 중앙선거여론조사심의위원회 바로가기",
    "https://www.nesdc.go.kr",
    use_container_width=True
)

st.divider()

# -----------------------------
# 결과
# -----------------------------

keyword = st.session_state.keyword.strip()

if keyword:

    st.header(f"📊 {keyword}")

    st.markdown(
        f"""
        <div class='result-box'>

        <h3>{keyword}</h3>

        현재 버전은 UI 및 검색 테스트 버전입니다.

        <br>

        향후 추가 예정 기능

        <ul>
            <li>중앙선관위 자동 검색</li>
            <li>여론조사 데이터 자동 수집</li>
            <li>최근 1개월 추세 분석</li>
            <li>조사기관별 비교</li>
            <li>지지율 꺾은선 그래프</li>
            <li>조사 원문 링크 제공</li>
        </ul>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        f"'{keyword}' 관련 여론조사가 검색되면 이 영역에 그래프와 분석 결과가 표시됩니다."
    )

else:

    st.markdown("""
    ## 👋 사용 방법

    1. 관심 있는 키워드를 입력하세요.
    2. 또는 실시간 관심 키워드를 클릭하세요.
    3. 검색 결과가 이곳에 표시됩니다.
    """)

# -----------------------------
# 하단
# -----------------------------

st.divider()

st.caption(
    "대한민국 여론분석기 Beta v0.1"
)
