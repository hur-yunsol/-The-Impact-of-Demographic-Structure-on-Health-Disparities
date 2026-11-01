# &#x20;인구사회학적 구조와 의료 인프라의 지역별 차이가 주요 암 발생 및 건강 격차에 미치는 복합적 영향 분석

> \*\*2026 데이터분석 연구발표회 연구 프로젝트\*\*  
> 본 프로젝트는 대한민국 시군구별 인구사회학적 특성, 생활습관, 의료 인프라의 격차가 주요 암 발생 패턴(조발생률 vs 연령표준화발생률) 및 전반적인 건강 지표(기대여명, 사망률, 미충족의료율)에 미치는 복합적 영향을 다각도로 분석하고, Streamlit 대시보드를 통해 시각화합니다.

\---

## &#x20;1. 연구 개요 (Problem Definition)

### &#x20;연구 배경 및 필요성

건강 문제를 개인의 생활습관(비만율, 흡연 등)만으로 설명하기에는 한계가 있습니다. 개인이 살아가는 \*\*인구사회학적 환경(고령화, 소득 수준)\*\*과 \*\*의료 서비스 접근성(의료 인프라, 미충족의료율)\*\*이 복합적으로 작동하기 때문입니다.  
본 연구는 단순 개인 차원의 분석에서 확장하여 인구 구조, 사회경제적 환경, 생활습관, 의료 인프라를 통합 분석함으로써 지역 간 건강 불평등의 원인을 탐색하고, 지역 특성에 맞춘 예방·보건의료 정책의 필요성을 제시하고자 합니다.

### &#x20;핵심 연구 질문 (Research Questions)

* **큰 질문:** 대한민국 시군구별 인구사회학적 특성과 의료 인프라의 격차가 주요 암 발병 패턴 및 지역 간 전반적인 건강 격차에 어떤 복합적인 영향을 미치는가?
* **작은 질문 ①:** 2014\~2018년 시군구별 고령인구 비율은 암 발생률과 어떤 관계를 보이며, 조발생률과 연령표준화발생률 비교 시 지역 간 차이는 어떻게 달라지는가?
* **작은 질문 ②:** 2014\~2018년 시도별 소득 관련 지표, 고령인구 비율, 흡연율, 고위험음주율 및 신체활동 지표는 기대여명과 사망률 등 전반적인 건강 수준과 어떤 관계를 보이는가?
* **작은 질문 ③:** 2014\~2018년 시도별 인구 천 명당 의사 수와 병상 수는 미충족의료율, 기대여명 및 사망률과 어떤 관계를 보이며, 의료 인프라가 비슷한 지역 사이에서도 건강 수준 차이가 나타나는가?

\---

## &#x20;2. 팀원 구성 및 역할 (Team Members)

|학번|이름|담당 역할|
|:-:|:-:|-|
|**20820**|**허윤솔**|- 연구 기획 및 보건학적 가설 수립<br>- 공공데이터 수집 및 Pandas 기반 전처리/병합<br>- Streamlit 인터랙티브 웹앱 구현<br>- 시각화 결과 해석 및 정책 제안 도출|

\---

## &#x20;3. 활용 공공데이터 (Data Sources)

본 연구는 **KOSIS 국가통계포털** 및 **질병관리청**의 대한민국 전국 시·도 및 시·군·구 지자체 단위 국가승인통계를 활용하였습니다.

|데이터명|출처 / URL|분석 기간|주요 항목 / 활용 데이터|
|-|-|:-:|-|
|**데이터 1. 암발생자수 및 발생률**|KOSIS 국가통계포털|2014\~2018|시군구, 조발생률, 연령표준화발생률, 암종별 발생자수|
|**데이터 2. 행정구역별 흡연율**|KOSIS 국가통계포털 ([링크](https://kosis.kr/statHtml/statHtml.do?sso=ok&returnurl=https://kosis.kr:443/statHtml/statHtml.do?conn_path=MT_GTITLE01&list_id=103&obj_var_id=&seqNo=&tblId=DT_1YL21001E&vw_cd=MT_GTITLE01&itm_id=&language=kor&lang_mode=ko&orgId=101&))|2014\~2024|행정구역별 흡연율|
|**데이터 3. 시도별 사망원인생명표**|KOSIS 국가통계포털 ([링크](https://kosis.kr/statHtml/statHtml.do?sso=ok&returnurl=https://kosis.kr:443/statHtml/statHtml.do?conn_path=MT_ZTITLE&list_id=F_29&obj_var_id=&seqNo=&tblId=DT_1B45&vw_cd=MT_ZTITLE&itm_id=&language=kor&lang_mode=ko&orgId=101&))|2014, 2017, 2020, 2023|시도별, 연령별, 사망원인별 증가 기대여명|
|**데이터 4. 요양기관 주요 의료장비 현황**|KOSIS 국가통계포털 ([링크](https://kosis.kr/statHtml/statHtml.do?sso=ok&returnurl=https://kosis.kr:443/statHtml/statHtml.do?conn_path=MT_ZTITLE&list_id=354_MT_DTITLE&obj_var_id=&seqNo=&tblId=DT_HIRA4Q&vw_cd=MT_ZTITLE&itm_id=&language=kor&lang_mode=ko&orgId=354&))|2014\~2024|시군구별 진단방사선·특수의료장비 합산 수|
|**데이터 5. 미충족의료율**|KOSIS 국가통계포털 ([링크](https://kosis.kr/statHtml/statHtml.do?sso=ok&returnurl=https://kosis.kr:443/statHtml/statHtml.do?conn_path=MT_GTITLE01&list_id=103&obj_var_id=&seqNo=&tblId=DT_1YL202104E&vw_cd=MT_GTITLE01&itm_id=&language=kor&lang_mode=ko&orgId=101&))|2019\~2024|시군구별 미충족의료 경험 비율|
|**데이터 6. 시군구별 음주율**|KOSIS 국가통계포털 ([링크](https://kosis.kr/statHtml/statHtml.do?sso=ok&returnurl=https://kosis.kr:443/statHtml/statHtml.do?conn_path=MT_GTITLE01&list_id=103&obj_var_id=&seqNo=&tblId=DT_1YL20991E&vw_cd=MT_GTITLE01&itm_id=&language=kor&lang_mode=ko&orgId=101&))|2014\~2019|시군구별 음주율 / 고위험음주율|
|**데이터 7. 주민등록인구 현황**|KOSIS 국가통계포털 ([링크](https://kosis.kr/statHtml/statHtml.do?sso=ok&returnurl=https://kosis.kr:443/statHtml/statHtml.do?list_id=F_35&obj_var_id=&seqNo=&tblId=DT_117N_A11109&vw_cd=MT_ZTITLE&orgId=117&path=%252FstatisticsList%252FstatisticsListIndex.do&conn_path=MT_ZTITLE&itm_id=&lang_mode=ko&scrId=&))|2014\~2024|행정구역별 65세 이상 고령인구 합계|
|**데이터 8. 사망원인 통계**|KOSIS 국가통계포털 ([링크](https://kosis.kr/statHtml/statHtml.do?sso=ok&returnurl=https://kosis.kr:443/statHtml/statHtml.do?conn_path=MT_ZTITLE&list_id=F_27&obj_var_id=&seqNo=&tblId=DT_1B34E13&vw_cd=MT_ZTITLE&itm_id=&language=kor&lang_mode=ko&orgId=101&))|2014\~2024|악성신생물(암) 사망자수, 사망률, 연령표준화 사망률|

\---

## &#x20;4. 데이터 전처리 및 파생변수 (Data Preprocessing)

1. **데이터 정제 및 결합**

   * 텍스트 앞뒤 공백/탭 제거 및 지자체 행정구역 개편(명칭 변경/통합) 대응을 위한 지역명 표준화 진행.
   * `연도` 및 `시군구/시도` 키를 기준으로 `pandas.merge()`를 이용해 5개년 데이터셋 결합.
   * 일부 미조사 연도/항목 결측치 처리.
2. **파생변수(Derived Features) 생성**

   * **`고령화 보정 발생 격차`**: $(조발생률 - 연령표준화발생률)$  
→ 고령화율이 높은 지역에서 인구구조로 인해 환자 수가 착시되어 보이는 현상 분석.
   * **`생활습관 위험지수`**: 흡연율, 고위험음주율 등 표준화 점수(Z-score) 합산 파생 변수.

\---

## &#x20;5. 시각화 및 웹 대시보드 기능 (Streamlit App)

* **사이드바 컨트롤러**

  * **연도 선택 슬라이더**: 2014년 \~ 2018년 선택
  * **분석 질문 선택 라디오 버튼**: 질문 ①, ②, ③ 전환
  * **지역 필터 멀티 셀렉트 박스**: 시·도 및 시·군·구 단위 멀티 선택
* **분석 시각화**

  * **Tab 1:** 미충족의료율 상자그림(Boxplot) 및 미충족의료율 vs 사망률 이중축 그래프
  * **Tab 2:** 연도별 고령인구 추이 꺾은선 그래프 및 OLS 추세선 포함 암발생률 산점도
  * **Tab 3:** 흡연율·음주율·사망률간 Pearson 상관계수 히트맵 및 인터랙티브 추세선 산점도

\---

## &#x20;6. 결론 및 결론 해석 시 유의점 해석상의 유의점 (해석 한계 명시)

> 의료 인프라(병상/의사 수)가 많은 대도시 지역으로 타 지역 환자가 집중되는 \*\*의료 이용 쏠림 현상\*\*과 암의 \*\*장기 잠복기적 특성\*\*이 존재합니다. 따라서 인프라 수치와 사망률/기대여명 간의 상관관계를 \*\*단순 일대일 인과관계로 확장하여 해석하지 않습니다.\*\*

### 해결책 및 공공보건 정책 제안

* **분석 근거:** 단순 인구당 의료장비·병상 수 등 양적 인프라 수치보다 주민이 체감하는 **미충족의료율**과 **생활습관 위험지수**가 실제 기대여명 및 사망률 격차에 더 실질적인 영향을 미침.
* **주체:** 지방자치단체 보건소 및 보건복지부
* **실행 방안:**

  1. 의료 소외 지역 주민의 실질적 접근성 제고를 위한 **이동형 공공 검진 및 진료 버스** 운영 확대.
  2. 취약 지역 중심의 **만성질환 및 생활습관 관리 모바일 보건소 사업** 우선 추진을 통한 지역 간 건강 불평등 해소.

### 연구의 한계 (Limitations)

1. **생태학적 오류 (Ecological Fallacy):** 시군구/시도 집단 데이터를 기반으로 분석했으므로 개개인의 유전적 요인이나 개별 병원 이용 행태로 직접 일반화할 수 없음.
2. **시계열적 한계:** 분석 기간이 2014\~2018년(5개년)에 국한되어 최근 보건 환경 변화를 완벽하게 반영하지 못함.

\---

## 7\. 생성형 AI 활용 계획 (AI Tool Usage)

* **사용 도구:** ChatGPT, Gemini
* **AI 담당 업무:**

  * KOSIS 및 질병관리청 5개 CSV 데이터의 `pandas.merge()` 전처리 파이썬 코드 작성 보조.
  * Streamlit 웹앱 레이아웃 구조화 및 Plotly 인터랙티브 그래프 코드 구현.
* **팀 직접 판단 및 수행:**

  * 연구 주제 선정 및 보건학적 가설 수립.
  * 조발생률 vs 연령표준화발생률 차이가 지니는 의학적·보건학적 의미 해석.
  * 데이터 기반 공공보건 정책 해결책 도출 및 타당성 검토.
* **결과 검증 (Cross-Verification):**

  * AI가 도출한 통계치/상관계수를 KOSIS 원본 엑셀 데이터와 교차 대조하여 수치 검증.
  * 파이썬 출력 결과와 원본 데이터의 행·열 구조 일치 여부 확인.

