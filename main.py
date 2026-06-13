import streamlit as st
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re

st.set_page_config(
    page_title="여론분석기",
    page_icon="🕯️",
    layout="wide"
)

# -----------------------------
# 디자인
# -----------------------------

st.markdown("""
<h1 style='text-align:center'>
🕯️ &nbsp;&nbsp;&nbsp;
여론분석기
&nbsp;&nbsp;&nbsp; 🇰🇷 🇺🇸
</h1>
""", unsafe_allow_html=True)

st.markdown(
    "<p style='text-align:center;color:gray;'>"
    "뉴스·여론조사 기반 대한민국 여론 분석"
    "</p>",
    unsafe_allow_html=True
)

# -----------------------------
# 실검 예시
# -----------------------------

trending_keywords = [
    "대통령",
    "삼성전자",
    "부동산",
    "코스피",
    "한미관계"
]

st.markdown("### 🔥 실시간 관심 키워드")

cols = st.columns(len(trending_keywords))

for i, keyword in enumerate(trending_keywords):
    cols[i].button(keyword)

st.divider()

# -----------------------------
# 검색창
# -----------------------------

keyword = st.text_input(
    "키워드를 입력하세요",
    placeholder="예: 대통령, 삼성전자, 물가"
)

# -----------------------------
# 감성분석용 단어
# -----------------------------

positive_words = [
    "상승",
    "성공",
    "호재",
    "개선",
    "증가",
    "확대",
    "돌파",
    "회복",
    "성장",
    "최고"
]

negative_words = [
    "하락",
    "실패",
    "악재",
    "감소",
    "위기",
    "논란",
    "적자",
    "폭락",
    "우려",
    "최저"
]

# -----------------------------
# RSS 뉴스 검색
# -----------------------------

def get_news(query):

    try:

        encoded = urllib.parse.quote(query)

        url = (
            "https://news.google.com/rss/search?"
            f"q={encoded}+when:30d&hl=ko&gl=KR&ceid=KR:ko"
        )

        data = urllib.request.urlopen(url, timeout=10).read()

        root = ET.fromstring(data)

        news = []

        for item in root.findall(".//item")[:20]:

            title = item.find("title").text
            link = item.find("link").text

            news.append({
                "title": title,
                "link": link
            })

        return news

    except Exception:
        return []

# -----------------------------
# 분석
# -----------------------------

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

# -----------------------------
# 실행
# -----------------------------

if keyword:

    st.header(f"📊 '{keyword}' 여론 분석")

    with st.spinner("뉴스 분석 중..."):

        news = get_news(keyword)

    if not news:

        st.error("관련 뉴스를 찾을 수 없습니다.")

    else:

        pos, neutral, neg = analyze_news(news)

        total = pos + neutral + neg

        if total == 0:
            total = 1

        pos_pct = round(pos / total * 100, 1)
        neutral_pct = round(neutral / total * 100, 1)
        neg_pct = round(neg / total * 100, 1)

        c1, c2, c3 = st.columns(3)

        c1.metric("긍정", f"{pos_pct}%")
        c2.metric("중립", f"{neutral_pct}%")
        c3.metric("부정", f"{neg_pct}%")

        st.subheader("여론 분포")

        chart_data = {
            "긍정": pos_pct,
            "중립": neutral_pct,
            "부정": neg_pct
        }

        st.bar_chart(chart_data)

        st.subheader("AI 요약")

        if pos_pct > neg_pct:
            st.success(
                f"최근 뉴스 기준으로 '{keyword}'에 대한 여론은 "
                "비교적 긍정적인 흐름을 보입니다."
            )
        elif neg_pct > pos_pct:
            st.error(
                f"최근 뉴스 기준으로 '{keyword}'에 대한 여론은 "
                "비교적 부정적인 흐름을 보입니다."
            )
        else:
            st.info(
                f"최근 뉴스 기준으로 '{keyword}'에 대한 여론은 "
                "중립적입니다."
            )

        st.subheader("관련 뉴스")

        for article in news:

            st.markdown(
                f"- [{article['title']}]({article['link']})"
            )

        st.divider()

        st.subheader("참고 사이트")

        st.markdown(
            """
            - 중앙선거여론조사심의위원회:
              https://www.nesdc.go.kr

            - 네이버 뉴스:
              https://news.naver.com

            - 구글 뉴스:
              https://news.google.com
            """
        )

st.divider()

st.caption(
    "본 서비스는 뉴스 제목 기반의 단순 분석이며 "
    "실제 여론조사 결과와 다를 수 있습니다."
)
