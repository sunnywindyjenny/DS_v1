# -------------------------------------------------------------
# 설치 명령 (터미널에서 한 번만 실행)
#   pip install streamlit plotly pandas
# 실행 방법
#   streamlit run streamlit_app.py
# -------------------------------------------------------------

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="매출 대시보드", layout="wide")

FONT_FAMILY = "Apple SD Gothic Neo, Noto Sans KR, Malgun Gothic, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"

st.title("매출 대시보드")

# ===== 데이터 정의 (업로드한 엑셀 값을 반영) =====
BAR_LABELS = ["2023-01","2023-02","2023-03","2023-04","2023-05","2023-06","2023-07","2023-08","2023-09","2023-10","2023-11","2023-12"]
BAR_VALUES = [885,918,887,1148,1436,1131,1217,1094,1188,1079,1343,1641]

df_bar = pd.DataFrame({"월": BAR_LABELS, "총 매출": BAR_VALUES})

TIME_LABELS = BAR_LABELS
TIME_SERIES = {
    "제품 A 매출": [272,147,217,292,423,351,295,459,109,311,377,342],
    "제품 B 매출": [86,137,120,266,138,190,108,243,280,89,137,224],
    "제품 C 매출": [158,407,235,95,403,142,335,185,313,267,405,408],
    "제품 D 매출": [222,97,167,242,373,301,245,59,261,327,292,342],
    "제품 E 매출": [147,130,148,253,99,147,234,148,225,85,132,325],
}
df_time = pd.DataFrame({"월": TIME_LABELS, **TIME_SERIES})

PIE_LABELS = ["제품 A","제품 B","제품 C","제품 D","제품 E"]
PIE_VALUES = [3595,2018,3353,2928,2073]
df_pie = pd.DataFrame({"제품": PIE_LABELS, "1분기 매출": PIE_VALUES})

SCATTER_X = [272,147,217,292,423,351,295,459,109,311,377,342]
SCATTER_Y = [149,227,293,335,197,197,338,315,235,177,82,81]
df_scatter = pd.DataFrame({"제품 A 매출": SCATTER_X, "비용": SCATTER_Y})

PARETO_LABELS = ["기획부","마케팅부","영업부","인사부","개발부"]
PARETO_VALUES = [954,923,559,477,209]
df_pareto = pd.DataFrame({"부서": PARETO_LABELS, "매출": PARETO_VALUES})
df_pareto = df_pareto.sort_values("매출", ascending=False).reset_index(drop=True)
df_pareto["누적 비율 (%)"] = (df_pareto["매출"].cumsum() / df_pareto["매출"].sum() * 100).round(2)

BUBBLE_POINTS = [
    {"제품":"제품 1","제품별 비용":884.0,"마진":699.0,"고객 수":127},
    {"제품":"제품 2","제품별 비용":759.0,"마진":170.0,"고객 수":122},
    {"제품":"제품 3","제품별 비용":829.0,"마진":572.0,"고객 수":59},
    {"제품":"제품 4","제품별 비용":392.0,"마진":496.0,"고객 수":198},
    {"제품":"제품 5","제품별 비용":963.0,"마진":414.0,"고객 수":165},
    {"제품":"제품 6","제품별 비용":907.0,"마진":586.0,"고객 수":258},
    {"제품":"제품 7","제품별 비용":559.0,"마진":651.0,"고객 수":293},
    {"제품":"제품 8","제품별 비용":209.0,"마진":187.0,"고객 수":247},
    {"제품":"제품 9","제품별 비용":923.0,"마진":274.0,"고객 수":129},
    {"제품":"제품 10","제품별 비용":477.0,"마진":637.0,"고객 수":225},
]
df_bubble = pd.DataFrame(BUBBLE_POINTS)

# ===== 3x2 레이아웃 =====
row1 = st.columns(3)
row2 = st.columns(3)

# 1) 바차트
with row1[0]:
    st.subheader("바차트 · 월별 총 매출")
    fig = px.bar(df_bar, x="월", y="총 매출")
    fig.update_layout(font=dict(family=FONT_FAMILY))
    st.plotly_chart(fig, use_container_width=True)

# 2) 시계열 라인
with row1[1]:
    st.subheader("시계열 · 제품별 월간 매출 추세")
    fig = go.Figure()
    for col in [c for c in df_time.columns if c != "월"]:
        fig.add_trace(go.Scatter(x=df_time["월"], y=df_time[col], mode="lines+markers", name=col))
    fig.update_layout(font=dict(family=FONT_FAMILY), xaxis_title="월", yaxis_title="매출")
    st.plotly_chart(fig, use_container_width=True)

# 3) 파이차트
with row1[2]:
    st.subheader("파이차트 · 1분기 제품별 매출 비중")
    fig = px.pie(df_pie, names="제품", values="1분기 매출", hole=0)
    fig.update_layout(font=dict(family=FONT_FAMILY))
    st.plotly_chart(fig, use_container_width=True)

# 4) 산점도
with row2[0]:
    st.subheader("산점도 · 제품 A 매출 vs 비용")
    fig = px.scatter(df_scatter, x="제품 A 매출", y="비용")  # Plotly 기본 모양은 동그라미
    fig.update_layout(font=dict(family=FONT_FAMILY))
    st.plotly_chart(fig, use_container_width=True)

# 5) 파레토 (막대 + 누적 비율 라인, 2축)
with row2[1]:
    st.subheader("파레토차트 · 부서별 매출")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_pareto["부서"], y=df_pareto["매출"], name="매출"))
    fig.add_trace(go.Scatter(x=df_pareto["부서"], y=df_pareto["누적 비율 (%)"], name="누적 비율 (%)", mode="lines+markers", yaxis="y2"))
    fig.update_layout(
        font=dict(family=FONT_FAMILY),
        xaxis=dict(title="부서"),
        yaxis=dict(title="매출"),
        yaxis2=dict(title="누적 비율 (%)", overlaying="y", side="right", range=[0, 100])
    )
    st.plotly_chart(fig, use_container_width=True)

# 6) 버블차트 (동그라미)
with row2[2]:
    st.subheader("버블차트 · 비용·마진·고객수 (동그라미)")
    # size를 고객 수로 매핑, 동그라미 유지
    fig = px.scatter(
        df_bubble,
        x="제품별 비용",
        y="마진",
        size="고객 수",
        hover_name="제품",
    )  # Plotly 기본 마커 = circle
    fig.update_layout(font=dict(family=FONT_FAMILY), xaxis_title="제품별 비용", yaxis_title="마진")
    st.plotly_chart(fig, use_container_width=True)

st.caption("데이터 출처: 업로드한 엑셀 파일 (요약 반영) · 한글 폰트는 시스템 기본 폰트를 사용합니다.")
