# AI 고유주기 예측 웹앱

기존 Android 앱에 사용한 Random Forest 4개 모델을 재학습 없이 사용합니다.

## 배포 절차
1. GitHub에서 새 공개 저장소를 만듭니다.
2. 이 폴더 안의 `app.py`, `requirements.txt`, 4개 `.joblib`, `.streamlit/config.toml`을 저장소에 업로드합니다. ZIP 자체를 업로드하지 마세요.
3. https://share.streamlit.io/ 에 GitHub 계정으로 로그인합니다.
4. `Create app` → GitHub 저장소 선택 → Main file path `app.py` → Deploy를 선택합니다.
5. 배포 URL을 아이폰 Safari에서 열어 예측 결과를 확인합니다.

## 모델 재현 확인용 값
- 개수 5개: 0.523537 s
- 배치 기본설계안: 0.589782 s
- 형태 X형: 0.517798 s
- 크기 5.5 × 4.25: 0.517913 s

## 주의
- 모델은 scikit-learn 1.6.1에서 생성되어 해당 버전으로 고정했습니다.
- 웹앱의 '오차율'은 동일 학습 조건의 MIDAS 결과와 비교한 값이며, LOOCV 검증 오차가 아닙니다.
- 학습 조건 외 예측은 검증되지 않았습니다.
- 이 프로젝트는 연구용이며 구조설계의 근거로 사용하지 않습니다.
