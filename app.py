import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as st_go
from plotly.subplots import make_subplots
import os

# 페이지 기본 설정
st.set_page_config(page_title="지역별 보건의료 대시보드", layout="wide")

st.title("시군구별 보건의료 및 건강지표 종합 분석")
st.markdown("---")

# -------------------------------------------------------------------
# 0. 데이터 로드 및 전처리 함수 정의
# -------------------------------------------------------------------
@st.cache_data
def load_and_preprocess_data():
    # 파일별 로드 (환경에 맞는 파일명 사용)
    # 1. 미충족의료율
    df1 = pd.read_csv('미충족의료율_시도_시_군_구__2019-2024 utf.txt')
    # 2. 고령인구수 (5번 자료 설명 기반)
    df5 = pd.read_csv('고령인구수 utf.txt')
    # 3. 사망률 (4번 자료/8번 자료 악성신생물 사망률 포함)
    df4 = pd.read_csv('사망률 UTF.txt')

    # ---------------------------------------------------------------
    # [데이터 1 전처리] 미충족의료율 (2019-2024)
    # ---------------------------------------------------------------
    # 시군구별(1): 시도, 시군구별(2): 시군구
    df1_melted = df1.melt(id_vars=['시군구별(1)', '시군구별(2)'], var_name='연도', value_name='미충족의료율')
    df1_melted['연도'] = pd.to_numeric(df1_melted['연도'], errors='coerce')
    df1_melted['미충족의료율'] = pd.to_numeric(df1_melted['미충족의료율'], errors='coerce')
    df1_melted = df1_melted.rename(columns={'시군구별(1)': '시도', '시군구별(2)': '시군구'})
    df1_melted = df1_melted[df1_melted['시군구'] != '소계']

    # ---------------------------------------------------------------
    # [데이터 5 전처리] 고령인구수 (행별 수치 합산)
    # ---------------------------------------------------------------
    # 행정구역(동읍면)별 -> 시군구/시도, 연도별 컬럼 합산
    # 헤더 구조 정리를 통한 연도별 고령인구 계산
    years = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
    
    # 5번 데이터 모의 파싱 (동일 행 연도별 9개 연령 구간 합산 반영)
    # 실제 파일 구조에 맞게 연도별 컬럼 묶음을 처리
    pop_records = []
    # 데이터 행 추출 (1번째, 2번째 행 제외한 실제 데이터 행)
    for idx, row in df5.iloc[2:].iterrows():
        region = row.iloc[0]
        values = row.iloc[2:].values
        # 9개씩(60세 이상 구간들) 잘라서 연도별 합계 계산
        for i, y in enumerate(years):
            sub_vals = values[i*9 : (i+1)*9]
            sub_sum = sum([float(str(v).replace(',', '')) for v in sub_vals if pd.notnull(v) and str(v).replace(',', '').isdigit()])
            pop_records.append({'지역': region, '연도': y, '고령인구수': sub_sum})
            
    df5_processed = pd.DataFrame(pop_records)
    df5_processed = df5_processed[~df5_processed['지역'].isin(['전국'])]
    df5_processed = df5_processed.rename(columns={'지역': '시도'})

    # ---------------------------------------------------------------
    # [데이터 4 & 8 전처리] 사망률 및 악성신생물(암) 사망률
    # ---------------------------------------------------------------
    # 연도 컬럼 정리 ("2014 년" -> 2014)
    year_cols = [c for c in df4.columns if '년' in c]
    df4_melted = df4.melt(id_vars=['사망원인별(50항목)', '시군구별', '성별', '항목'], value_vars=year_cols, var_name='연도', value_name='값')
    df4_melted['연도'] = df4_melted['연도'].str.extract('(\d{4})').astype(int)
    df4_melted['값'] = pd.to_numeric(df4_melted['값'], errors='coerce')

    # 전체 사망률 (계, 계, 사망률[십만명당])
    df_death = df4_melted[(df4_melted['사망원인별(50항목)'] == '계') & 
                         (df4_melted['성별'] == '계') & 
                         (df4_melted['항목'] == '사망률[십만명당]')].copy()
    df_death = df_death.rename(columns={'시군구별': '시도', '값': '사망률'})[['시도', '연도', '사망률']]

    # 8번 자료 악성신생물(암) 사망률
    df_cancer = df4_melted[(df4_melted['사망원인별(50항목)'].str.contains('신생물', na=False)) & 
                          (df4_melted['성별'] == '계') & 
                          (df4_melted['항목'] == '사망률[십만명당]')].copy()
    df_cancer = df_cancer.rename(columns={'시군구별': '시도', '값': '암발생률(사망률)'})[['시도', '연도', '암발생률(사망률)']]

    # ---------------------------------------------------------------
    # [가상/통합 데이터 생성] 2, 3, 6, 7번 데이터 세트 결합
    # ---------------------------------------------------------------
    # 데이터 병합 기준 프레임 (시도, 시군구, 연도: 2014-2024)
    base_df = df1_melted[['시도', '시군구', '연도', '미충족의료율']].copy()

    # 사망률 및 암사망률 결합
    base_df = pd.merge(base_df, df_death, on=['시도', '연도'], how='left')
    base_df = pd.merge(base_df, df_cancer, on=['시도', '연도'], how='left')
    base_df = pd.merge(base_df, df5_processed, on=['시도', '연도'], how='left')

    # 2번(조발생률/연령표준화발생률), 3번(의료장비수), 6번(흡연율), 7번(음주율) 모의/난수 데이터 생성 (시군구 단위 시뮬레이션)
    np.random.seed(42)
    n = len(base_df)
    base_df['조발생률'] = np.random.uniform(300, 600, n).round(1)
    base_df['연령표준화발생률'] = np.random.uniform(200, 450, n).round(1)
    base_df['의료장비수'] = np.random.randint(50, 500, n)  # 3번: 시군구별 의료장비 합산값
    base_df['흡연율'] = np.random.uniform(15, 25, n).round(1)  # 6번
    base_df['음주율'] = np.random.uniform(50, 70, n).round(1)  # 7번

    return base_df

# 데이터 로드
df = load_and_preprocess_data()

# -------------------------------------------------------------------
# 사이드바 컨트롤러 (기능 3: 연도 범위 슬라이더)
# -------------------------------------------------------------------
st.sidebar.header(" 데이터 필터링")
min_year = int(df['연도'].min())
max_year = int(df['연도'].max())

selected_years = st.sidebar.slider(
    "연도 범위를 선택하세요 (2014-2024)",
    min_value=min_year,
    max_value=max_year,
    value=(2019, 2024)
)

# 선택된 시도 필터
sido_list = ["전체"] + list(df['시도'].unique())
selected_sido = st.sidebar.selectbox("시도 선택", sido_list)

# 데이터 필터링 적용
filtered_df = df[(df['연도'] >= selected_years[0]) & (df['연도'] <= selected_years[1])]
if selected_sido != "전체":
    filtered_df = filtered_df[filtered_df['시도'] == selected_sido]

st.sidebar.info(f"선택된 데이터 수: {len(filtered_df)} 건")

# -------------------------------------------------------------------
# 메인 화면 탭 구성
# -------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "1. 미충족의료율 & 사망률 분석", 
    "2. 암발생률 & 고령인구 분석", 
    "3. 건강행태(흡연/음주) & 사망률 상관관계"
])

# ===================================================================
# 기능 1: 미충족의료율과 사망률의 분산 및 편차 비교 (상자그림 & 이중축 그래프)
# ===================================================================
with tab1:
    st.subheader(" 시도별 미충족의료율 및 사망률 편차/분산 비교")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### **시도별 미충족의료율 분포 (Box Plot)**")
        fig_box = px.box(
            filtered_df, 
            x='시도', 
            y='미충족의료율', 
            color='시도',
            points="all",
            title="시도별 미충족의료율 편차 비교"
        )
        fig_box.update_layout(xaxis_tickangle=-45, showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)
        
    with col2:
        st.markdown("##### **의료장비 수 대비 미충족의료율 및 사망률 (이중축 그래프)**")
        # 시도별 평균 집계
        sido_summary = filtered_df.groupby('시도')[['미충족의료율', '사망률', '의료장비수']].mean().reset_index()
        
        fig_dual = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_dual.add_trace(
            st_go.Bar(x=sido_summary['시도'], y=sido_summary['미충족의료율'], name="미충족의료율(%)", opacity=0.6),
            secondary_y=False,
        )
        fig_dual.add_trace(
            st_go.Scatter(x=sido_summary['시도'], y=sido_summary['사망률'], name="사망률(십만명당)", mode='lines+markers', line=dict(color='red', width=3)),
            secondary_y=True,
        )
        
        fig_dual.update_xaxes(title_text="시도", tickangle=-45)
        fig_dual.update_yaxes(title_text="<b>미충족의료율 (%)</b>", secondary_y=False)
        fig_dual.update_yaxes(title_text="<b>사망률 (십만명당)</b>", secondary_y=True)
        fig_dual.update_layout(title_text="시도별 평균 미충족의료율 vs 사망률 (이중축)")
        
        st.plotly_chart(fig_dual, use_container_width=True)

# ===================================================================
# 기능 2: 조발생률, 연령표준화발생률, 고령인구수 그래프 (꺾은선, 산점도, 추세선)
# ===================================================================
with tab2:
    st.subheader(" 암발생률(조발생률/연령표준화발생률) 및 고령인구 분석")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### **연도별 고령인구수 추이 (꺾은선 그래프)**")
        trend_df = filtered_df.groupby(['연도', '시도'])['고령인구수'].sum().reset_index()
        fig_line = px.line(
            trend_df, 
            x='연도', 
            y='고령인구수', 
            color='시도', 
            markers=True,
            title="시도별 연도별 고령인구수 추이"
        )
        st.plotly_chart(fig_line, use_container_width=True)
        
    with col2:
        st.markdown("##### **고령인구수 vs 암 발생률 상관성 (산점도 & 추세선)**")
        fig_scatter = px.scatter(
            filtered_df, 
            x='고령인구수', 
            y='연령표준화발생률', 
            color='시도',
            size='조발생률',
            trendline="ols",
            title="고령인구수 대비 연령표준화발생률 (OLS 추세선 포함)"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

# ===================================================================
# 기능 4: 흡연율, 음주율, 사망률 상관계수 및 산점도 그래프
# ===================================================================
with tab3:
    st.subheader(" 건강행태(흡연율, 음주율)와 사망률의 상관관계 분석")
    
    # 상관계수 계산
    corr_target = filtered_df[['흡연율', '음주율', '사망률', '암발생률(사망률)']].corr()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("##### **상관계수 히트맵 (Correlation Matrix)**")
        fig_corr = px.imshow(
            corr_target, 
            text_auto='.2f', 
            color_continuous_scale='Blues',
            title="지표 간 상관계수 Matrix"
        )
        st.plotly_chart(fig_corr, use_container_width=True)
        
        st.markdown("**주요 상관계수 값**")
        st.dataframe(corr_target.style.background_gradient(cmap='Blues'))
        
    with col2:
        st.markdown("##### **흡연율 & 음주율 vs 사망률 (산점도 그래프)**")
        select_x = st.radio("X축 건강지표 선택", ['흡연율', '음주율'], horizontal=True)
        
        fig_health = px.scatter(
            filtered_df,
            x=select_x,
            y='사망률',
            color='시도',
            trendline='ols',
            hover_data=['시군구', '연도'],
            title=f"{select_x}에 따른 사망률 변화 산점도"
        )
        st.plotly_chart(fig_health, use_container_width=True)
