"""저층 장스팬 구조물의 가새 조건별 고유주기 예측 웹앱.
원본 joblib 4개를 수정하거나 재학습하지 않습니다.
"""
from pathlib import Path
import joblib
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
NAVY = '#1E3A5F'
TEAL = '#087E78'
TS = 0.5657

NUMBER_DATA = {0: 0.9765, 2: 0.7947, 3: 0.6118, 4: 0.5622, 5: 0.5116, 6: 0.5017}
ARRANGEMENT_DATA = {'기본설계안': 0.5622, '좌측분산': 0.6219, '중앙분산': 0.6563, '우측분산': 0.6560, '중앙집중': 0.6764}
SHAPE_DATA = {'X형': 0.5157, 'K형': 0.5233, '역V형': 0.5231}
SIZE_DATA = {
    (5.5, 4.25): 0.5157, (4.0, 4.0): 0.5474, (4.25, 6.0): 0.5340,
    (5.0, 5.0): 0.5232, (5.5, 5.5): 0.5190, (5.5, 6.0): 0.5134,
    (5.5, 6.25): 0.5118, (6.0, 4.25): 0.5164, (6.0, 5.5): 0.5251,
    (6.25, 5.0): 0.5332, (7.0, 4.25): 0.5329,
}

st.set_page_config(page_title='AI 고유주기 예측', page_icon='🏗️', layout='centered')
st.markdown('''<style>
.stApp {background: #F4F5F7;}
.block-container {max-width: 760px; padding-top: 1.7rem; padding-bottom: 3rem;}
h1,h2,h3 {color: #1E3A5F !important;}
div.stButton > button {border-radius: 14px; min-height: 48px; font-weight: 700; border-color: #B8C8DA;}
div.stButton > button[kind="primary"] {background: #1E3A5F; border-color: #1E3A5F; color: white;}
.hero {background: #1E3A5F; color: white; border-radius: 19px; padding: 24px; margin-bottom: 18px;}
.hero h2 {color: white !important; margin: 0 0 5px 0; font-size: 1.55rem;}
.hero p {color: #E1EAF4; margin: 0; font-size: .91rem;}
.result {background: #1E3A5F; color: white; border-radius: 18px; padding: 22px; margin: 14px 0;}
.result .number {font-size: 2.4rem; font-weight: 800; letter-spacing: -.03em;}
.result .label {font-size: .95rem; opacity: .88;}
.detail {background: white; border-radius: 15px; padding: 17px 20px; margin: 10px 0; border: 1px solid #E5EAF0;}
.detail .caption {color: #586779; font-size: .85rem;}
.detail .value {font-size: 1.25rem; font-weight: 700; color: #1E3A5F;}
.notice {color: #B42318; font-size: .87rem; margin-top: 18px;}
</style>''', unsafe_allow_html=True)

@st.cache_resource(show_spinner=False)
def load_model(kind):
    # 모델을 생성한 scikit-learn 1.6.1 환경에서 불러옵니다.
    return joblib.load(ROOT / f'{kind}_model.joblib')


def predict(kind, frame):
    return float(load_model(kind).predict(frame)[0])


def show_result(value, actual):
    st.markdown(f'<div class="result"><div class="label">AI 예측 고유주기</div><div class="number">{value:.4f} s</div></div>', unsafe_allow_html=True)
    if actual is None:
        st.markdown('<div class="detail"><div class="caption">MIDAS 고유주기</div><div class="value">비교 데이터 없음</div><div class="caption">오차율: 산출 불가</div></div>', unsafe_allow_html=True)
    else:
        error = abs(value - actual) / abs(actual) * 100
        st.markdown(f'<div class="detail"><div class="caption">MIDAS 해석값</div><div class="value">{actual:.4f} s</div><div class="caption">오차율: {error:.2f}% (해당 조건의 학습 데이터와 비교)</div></div>', unsafe_allow_html=True)
    if abs(value - TS) <= 0.03:
        st.warning(f'예측 주기가 응답스펙트럼 경계주기 Ts={TS:.4f} s에 가깝습니다. (±0.03 s)')
    st.markdown('<div class="notice">※ 예측 결과는 연구용 참고값이며 내진설계의 근거로 사용할 수 없습니다. 최종 판단은 상세 구조해석이 필요합니다.</div>', unsafe_allow_html=True)


if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'last_result' not in st.session_state:
    st.session_state.last_result = None


def goto(page):
    st.session_state.page = page
    st.session_state.last_result = None


labels = {'number': '가새 개수', 'arrangement': '가새 배치', 'shape': '가새 형태', 'size': '가새 크기'}
if st.session_state.page == 'home':
    st.markdown('<div class="hero"><h2>AI 고유주기 예측 시스템</h2><p>저층 장스팬 구조물 · 가새 보강 조건별 분석</p></div>', unsafe_allow_html=True)
    st.write('분석할 가새 조건을 선택해 주세요.')
    for key in ['number', 'arrangement', 'shape', 'size']:
        if st.button('▸  ' + labels[key], key=f'home_{key}', use_container_width=True):
            goto(key)
            st.rerun()
    st.info('기존 MIDAS Gen 해석 결과 25개 조건을 바탕으로 학습한 독립 Random Forest 모델 4개를 사용합니다.')
    st.caption('AI 예측은 연구용 참고자료이며 실제 구조설계를 대신하지 않습니다.')
else:
    kind = st.session_state.page
    if st.button('←  홈으로 돌아가기'):
        goto('home')
        st.rerun()
    st.markdown(f'<div class="hero"><h2>{labels[kind]} 분석</h2><p>기존 Random Forest 모델 기반 고유주기 예측</p></div>', unsafe_allow_html=True)
    if kind == 'number':
        number = st.number_input('가새 개수', min_value=0, max_value=100, value=5, step=1)
        frame = pd.DataFrame({'가새개수': [int(number)]})
        actual = NUMBER_DATA.get(int(number))
    elif kind == 'arrangement':
        arrangement = st.radio('가새 배치 선택', list(ARRANGEMENT_DATA), horizontal=False)
        st.caption('고정 조건: 가새 4개, X형, 높이 5.5m × 폭 6.5m')
        frame = pd.DataFrame({'가새배치': [arrangement]})
        actual = ARRANGEMENT_DATA[arrangement]
    elif kind == 'shape':
        shape = st.radio('가새 형태 선택', list(SHAPE_DATA), horizontal=True)
        st.caption('고정 조건: 가새 3개, 기본설계안, 높이 5.5m × 폭 4.25m')
        frame = pd.DataFrame({'가새형태': [shape]})
        actual = SHAPE_DATA[shape]
    else:
        left, right = st.columns(2)
        with left:
            height = st.number_input('가새 높이 (m)', min_value=0.01, value=5.5, step=0.25, format='%.2f')
        with right:
            width = st.number_input('가새 폭 (m)', min_value=0.01, value=4.25, step=0.25, format='%.2f')
        st.caption('고정 조건: 가새 3개, 기본설계안, X형')
        frame = pd.DataFrame({'가새높이(m)': [float(height)], '가새폭(m)': [float(width)]})
        actual = SIZE_DATA.get((round(float(height), 4), round(float(width), 4)))
        if not (4.0 <= height <= 7.0 and 4.0 <= width <= 6.25):
            st.warning('입력값이 학습 데이터 범위(높이 4.0~7.0m, 폭 4.0~6.25m)를 벗어났습니다. 예측 신뢰성을 검증하지 않았습니다.')
    if st.button('고유주기 예측하기', type='primary', use_container_width=True):
        try:
            result = predict(kind, frame)
            st.session_state.last_result = (kind, result, actual)
        except Exception:
            st.session_state.last_result = None
            st.error('모델을 불러오거나 예측하지 못했습니다. 배포 환경의 Python 및 scikit-learn 버전을 확인해 주세요.')
    if st.session_state.last_result is not None and st.session_state.last_result[0] == kind:
        _, value, observed = st.session_state.last_result
        show_result(value, observed)
