# KOSPI Comparison (코스피 비교 분석)

[English Version](README_en.md)

현재의 코스피(KOSPI) 지수와 1980년대 3저 호황기 시절(1983년 6월 ~ 1987년 12월)의 코스피 지수를 비교 분석하여 시각화하는 프로젝트입니다.

매일 자동으로 업데이트되는 차트를 통해 과거의 시장 흐름과 현재의 지수 움직임을 비교할 수 있습니다.

👉 **실시간 차트 확인하기**:
- [한국어 버전](https://k-sunshine-log.github.io/kospi-comparison/)
- [영어 버전](https://k-sunshine-log.github.io/kospi-comparison/index_en.html)

## 주요 기능 (Features)

*   **데이터 자동 수집**: `FinanceDataReader` 라이브러리를 사용하여 KOSPI 지수 데이터를 실시간으로 가져옵니다.
*   **지수 비교 분석**:
    *   **스케일링 (Data Scaling)**: 1980년대 지수 데이터를 현재 지수 레벨에 맞춰 환산합니다. (시작점 5일 이동평균 기준)
    *   **시간 축 조정 (Time Shift)**: 과거 호황기 기간의 데이터를 현재 시점에 매핑하여 패턴을 비교합니다. (현재 시간 스케일 비율: 0.88)
*   **시각화 (Visualization)**:
    *   `Matplotlib`을 사용하여 다크 모드 스타일의 차트를 생성합니다.
    *   한글 폰트 지원 (OS별 자동 설정: Windows, Mac, Linux)
*   **자동화 배포 (CI/CD)**:
    *   GitHub Actions를 통해 매일 평일 오후 4시에 스크립트가 실행됩니다.
    *   생성된 차트는 `index.html`과 함께 GitHub Pages에 자동 배포됩니다.

## 요구 사항 (Requirements)

*   Python 3.9+
*   `finance-datareader`
*   `pandas`
*   `matplotlib`

## 설치 및 실행 방법 (Installation & Usage)

1.  **레포지토리 클론 (Clone)**

    ```bash
    git clone https://github.com/k-sunshine-log/kospi-comparison.git
    cd kospi-comparison
    ```

2.  **가상 환경 설정 (선택 사항)**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Mac/Linux
    # .venv\Scripts\activate  # Windows
    ```

3.  **의존성 패키지 설치**

    ```bash
    pip install -r requirements.txt
    ```

4.  **스크립트 실행**

    ```bash
    python main.py
    ```
    실행 후 `kospi_chart.png` 파일이 생성됩니다.

## 프로젝트 구조 (Structure)

*   `main.py`: 데이터 수집, 처리 및 차트 생성을 담당하는 메인 스크립트입니다.
*   `index.html`: 생성된 차트 이미지를 웹페이지로 보여주기 위한 HTML 파일입니다.
*   `.github/workflows/deploy.yml`: GitHub Actions 워크플로우 설정 파일입니다. (매일 자동 실행 및 배포)
*   `requirements.txt`: 프로젝트 실행에 필요한 Python 패키지 목록입니다.

## 자동화 (Automation)

이 프로젝트는 GitHub Actions를 사용하여 다음과 같은 작업을 수행합니다:

1.  **스케줄링**: 매일 평일 UTC 07:00 (한국 시간 16:00)에 실행됩니다.
2.  **환경 설정**: 우분투(Ubuntu) 환경에서 Python 3.9와 한글 폰트(나눔고딕)를 설치합니다.
3.  **차트 생성**: `main.py`를 실행하여 최신 데이터를 반영한 차트 이미지를 생성합니다.
4.  **배포**: 생성된 이미지와 `index.html`을 `gh-pages` 브랜치로 푸시하여 GitHub Pages를 업데이트합니다.

---
**Note**: 이 프로젝트는 과거의 시장 패턴을 현재와 비교하는 참고용 자료이며, 실제 투자를 위한 조언이 아닙니다.
