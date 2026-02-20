import FinanceDataReader as fdr
import pandas as pd
import matplotlib.pyplot as plt
import platform
from matplotlib import rc
from datetime import datetime, timedelta, timezone

# 한글 폰트 설정
if platform.system() == 'Darwin':
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows':
    rc('font', family='Malgun Gothic')
elif platform.system() == 'Linux':
    rc('font', family='NanumGothic') # GitHub Actions (Ubuntu) 환경 대응
plt.rcParams['axes.unicode_minus'] = False

# 다크 모드 스타일 적용
plt.style.use('dark_background')


def plot_kospi_comparison():
    # 1. 데이터 다운로드 (FinanceDataReader)
    # 현재 데이터: 2023년 1월 1일 ~ 현재
    # KS11: KOSPI 지수
    df_curr = fdr.DataReader('KS11', '2023-06-01')

    # 과거 데이터: 3저 호황기 (1983년 6월 ~ 1989년 12월)
    # 1983년 6월을 시작점으로 잡습니다.
    # FinanceDataReader는 1980년대 데이터도 제공합니다.
    df_past = fdr.DataReader('KS11', '1983-06-01', '1987-12-31')

    if df_curr.empty or df_past.empty:
        print("데이터 다운로드 실패. 인터넷 연결을 확인하거나 날짜 범위를 조정하세요.")
        return

    # 2. 데이터 동기화 (Scaling & Time Shift)
    # (A) 시작점 기준값 설정
    # (A) 시작점 기준값 설정 (단일 일이 아닌 5일 이동평균으로 보정하여 안정화)
    # 단순히 첫날 종가로 계산하면 변동성에 의해 스케일 차이가 크게 날 수 있습니다.
    start_val_curr = df_curr['Close'].head(5).mean()  # 2024.01 초반 5일 평균
    start_val_past = df_past['Close'].head(5).mean()  # 1983.06 초반 5일 평균

    print(f"Current Start (Avg): {start_val_curr:.2f}")
    print(f"Past Start (Avg): {start_val_past:.2f}")


    # (B) 스케일링 팩터 계산 (현재값 / 과거값)
    scale_ratio = start_val_curr / start_val_past

    # (C) 과거 데이터 스케일링
    # 과거 지수를 현재 지수 레벨로 환산 (예: 122 -> 2525)
    df_past['Scaled_Close'] = df_past['Close'] * scale_ratio

    # (D) 날짜 매핑 (3저 호황기 데이터를 현재 날짜에 맞춰서 매핑)
    # df_curr의 시작 날짜를 기준으로 df_past의 경과일을 더해 가상의 현재 날짜 생성
    start_date_curr = df_curr.index[0]

    # (D) 날짜 매핑
    # 시간 축 비율 설정 (Time Scale Ratio)
    # 1.0 : 1:1 매칭 (물리적 시간 동일)
    # 0.5 : 과거 시간이 2배 빠르게 지나감 (그래프가 좌우로 50% 압축됨) -> KB증권 차트처럼 과거 긴 기간을 현재 짧은 기간에 겹쳐볼 때 사용
    # 1.5 : 과거 시간이 1.5배 느리게 지나감 (그래프가 좌우로 150% 늘어남)
    # 1.5 : 과거 시간이 1.5배 느리게 지나감 (그래프가 좌우로 150% 늘어남)
    TIME_SCALE_RATIO = 0.88

    # 경과일(Day)을 실수(float)로 변환 후 비율 적용
    elapsed_days = (df_past.index - df_past.index[0]).days * TIME_SCALE_RATIO

    # 다시 Timedelta로 변환하여 더하기
    df_past['Mapped_Date'] = start_date_curr + pd.to_timedelta(elapsed_days, unit='D')


    # 현재 데이터는 그대로 사용
    df_curr['Mapped_Date'] = df_curr.index

    # 3. 시각화
    plt.figure(figsize=(14, 8))

    # 과거 패턴 - 일봉 표시
    plt.plot(df_past['Mapped_Date'], df_past['Scaled_Close'],
             label=f'1980년대 3저 호황기 패턴 (1983.06~, x{scale_ratio:.2f})',
             color='#FFB6C1', linestyle='--', linewidth=1.5, alpha=0.8) # LightPink, 점선

    # 현재 코스피 - 색상 변경 (파스텔 블루/스카이 블루), 눈이 편안한 색상
    plt.plot(df_curr['Mapped_Date'], df_curr['Close'],
             label='현재 코스피 (2023-06-01~)',
             color='#87CEEB', linewidth=2) # SkyBlue

    # 4. 차트 꾸미기
    plt.title("코스피 비교: 현재 vs 1980년대 호황기", fontsize=16, fontweight='bold', color='white')
    kst = timezone(timedelta(hours=9))
    now_str = datetime.now(kst).strftime('%Y-%m-%d %H:%M')
    plt.xlabel(f"날짜 ({now_str} 기준)", fontsize=12, color='white')
    plt.ylabel("지수 포인트", fontsize=12, color='white')
    plt.grid(True, linestyle=':', alpha=0.4, color='gray')

    # 범례 설정
    plt.legend(loc='upper left', fontsize=12, facecolor='black', edgecolor='white')

    # 현재가 표시
    last_date = df_curr['Mapped_Date'].iloc[-1]
    last_price = df_curr['Close'].iloc[-1]

    # annotate 텍스트 설정 (화살표 제거 요청 반영)
    # 텍스트 위치는 계속 왼쪽 위 유지
    plt.annotate(f'현재: {last_price:.0f}',
                 xy=(last_date, last_price),
                 xytext=(last_date - pd.Timedelta(days=80), last_price + 150),
                 ha='center', # 가로 중앙 정렬
                 color='white', fontweight='bold',
                 fontsize=16) # 폰트 크기 유지

    # X축 날짜 포맷 설정 (가독성 향상)
    import matplotlib.dates as mdates
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig('kospi_chart.png') # 이미지 파일로 저장
    # plt.show() # CI 환경에서는 주석 처리하거나 조건부 실행 필요. 로컬 확인용으로 유지하되, CI에서는 에러가 날 수 있음.
    # 하지만 plt.savefig 후에 plt.show()를 호출하면 문제 없음 (backend 설정에 따라 다름)
    try:
        plt.show()
    except Exception as e:
        print(f"Skipping plt.show() due to error (likely no display environment): {e}")

# 함수 실행
if __name__ == "__main__":
    plot_kospi_comparison()