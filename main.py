import streamlit as st
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from collections import Counter
import pandas as pd
import re

# --------------------------------------------------
# 설정
# --------------------------------------------------

st.set_page_config(
    page_title="대한민국 여론분석기",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# 이미지 URL
# --------------------------------------------------

CANDLE_IMAGE = "https://i.pinimg.com/736x/b9/52/2f/b9522f96d451eac189ad2a3d31510b13.jpg"

FLAG_IMAGE = "https://img1.newsis.com/2025/02/22/NISI20250222_0001776155_web.jpg?rnd=20250222165036"

# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown("""
<style>

.title{
    text-align:center;
    font-size:54px;
    font-weight:900;
    color:white;
    text-shadow:2px 2px 5px black;
}

.subtitle{
    text-align:center;
    color:#dddddd;
    font-size:18px;
}

.keyword-title{
    text-align:center;
    font-size:24px;
    font-weight:700;
}

.result-box{
    padding:20px;
    border-radius:15px;
    border:1px solid #444;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 세션 상태
# --------------------------------------------------

if "keyword" not in st.session_state:
    st.session_state.keyword = ""

# --------------------------------------------------
# 상단
# --------------------------------------------------

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
        뉴스 기반 대한민국 여론 분석
        </div>
        """,
        unsafe_allow_html=True
    )

with right:
    st.image(FLAG_IMAGE, use_container_width=True)

st.divider()

# --------------------------------------------------
# 실시간 키워드
# --------------------------------------------------

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

# --------------------------------------------------
# 검색창
# --------------------------------------------------

search = st.text_input(
    "키워드를 입력하세요",
    value=st.session_state.keyword,
    placeholder="예: 대통령"
)

if search != st.session_state.keyword:
    st.session_state.keyword = search

st.divider()

# --------------------------------------------------
# 뉴스 수집
# --------------------------------------------------

def get_news(query):

    try:

        encoded = urllib.parse.quote(query)

        url = (
            "https://news.google.com/rss/search?"
            f"q={encoded}+when:30d&hl=ko&gl=KR&ceid=KR:ko"
        )

        req = urllib.request.Request(
            url,
            headers={
                "User-Agent":"Mozilla/5.0"
            }
        )

        xml_data = urllib.request.urlopen(
            req,
            timeout=10
        ).read()

        root = ET.fromstring(xml_data)

        news = []

        for item in root.findall(".//item")[:50]:

            title = item.find("title").text
            link = item.find("link").text

            news.append({
                "title": title,
                "link": link
            })

        return news

    except Exception:
        return []

# --------------------------------------------------
# 감성 사전
# --------------------------------------------------

positive_words = [
    "상승",
    "증가",
    "개선",
    "회복",
    "성장",
    "돌파",
    "최고",
    "확대",
    "성공",
    "호재"
]

negative_words = [
    "하락",
    "감소",
    "위기",
    "논란",
    "우려",
    "실패",
    "악재",
    "폭락",
    "적자",
    "최저"
]

# --------------------------------------------------
# 감성 분석
# --------------------------------------------------

def analyze_news(news):

    pos = 0
    neg = 0
    neutral = 0

    for article in news:

        title = article["title"]

        score = 0

        for word in positive_words:
            if word in title:
                score += 1

        for word in negative_words:
            if word in title:
                score -= 1

        if score > 0:
            pos += 1

        elif score < 0:
            neg += 1

        else:
            neutral += 1

    return pos, neutral, neg

# --------------------------------------------------
# 키워드 추출
# --------------------------------------------------

def extract_keywords(news_titles):

    text = " ".join(news_titles)

    words = re.findall(
        r"[가-힣]{2,}",
        text
    )

    stopwords = {
        "대한",
        "관련",
        "기자",
        "뉴스",
        "오늘",
        "이번",
        "지난",
        "정부",
        "한국",
        "있다",
        "한다",
        "분석",
        "여론"
    }

    filtered = [
        w for w in words
        if w not in stopwords
    ]

    counter = Counter(filtered)

    return counter.most_common(10)

# --------------------------------------------------
# 실행
# --------------------------------------------------

keyword = st.session_state.keyword.strip()

if keyword:

    st.header(f"📊 {keyword}")

    with st.spinner("뉴스 분석 중..."):

        news = get_news(keyword)

    if not news:

        st.error("관련 뉴스를 찾지 못했습니다.")

    else:

        pos, neutral, neg = analyze_news(news)

        total = pos + neutral + neg

        if total == 0:
            total = 1

        pos_pct = round(pos/total*100, 1)
        neutral_pct = round(neutral/total*100, 1)
        neg_pct = round(neg/total*100, 1)

        c1, c2, c3 = st.columns(3)

        c1.metric("긍정", f"{pos_pct}%")
        c2.metric("중립", f"{neutral_pct}%")
        c3.metric("부정", f"{neg_pct}%")

        st.subheader("📈 여론 분포")

        chart_df = pd.DataFrame(
            {
                "비율":[
                    pos_pct,
                    neutral_pct,
                    neg_pct
                ]
            },
            index=[
                "긍정",
                "중립",
                "부정"
            ]
        )

        st.bar_chart(chart_df)

        st.subheader("🔥 주요 키워드")

        top_keywords = extract_keywords(
            [n["title"] for n in news]
        )

        kw_cols = st.columns(5)

        for i, (word, count) in enumerate(top_keywords[:5]):
            kw_cols[i].metric(
                word,
                count
            )

        st.subheader("📝 AI 요약")

        if pos_pct > neg_pct:

            st.success(
                f"""
                최근 뉴스 기준으로
                '{keyword}'에 대한 보도는
                긍정적인 흐름이 우세합니다.
                """
            )

        elif neg_pct > pos_pct:

            st.error(
                f"""
                최근 뉴스 기준으로
                '{keyword}'에 대한 보도는
                부정적인 흐름이 우세합니다.
                """
            )

        else:

            st.info(
                f"""
                최근 뉴스 기준으로
                '{keyword}'에 대한 보도는
                대체로 중립적입니다.
                """
            )

        st.subheader("📰 관련 뉴스")

        for article in news[:20]:

            st.markdown(
                f"- [{article['title']}]({article['link']})"
            )

else:

    st.info(
        "키워드를 입력하거나 실시간 관심 키워드를 선택하세요."
    )

st.divider()

st.caption(
    "본 서비스는 뉴스 제목 기반 분석이며 실제 여론조사 결과와 다를 수 있습니다."
)
