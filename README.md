# 인공지능과 함께하는 틱택토 게임

이 프로젝트는 파이게임(Pygame)을 사용하여 구현된 틱택토(Tic Tac Toe) 게임입니다. 이 게임은 다양한 수준의 AI를 포함하며, 랜덤 플레이와 강화 학습을 포함한 다양한 방법으로 학습된 AI를 제공합니다.

# Reference

[1] https://github.com/pygame/pygame "pygame"

## 기능

- 2인 플레이 모드
- 다양한 수준의 AI와 대결할 수 있는 1인 플레이 모드:
  - 레벨 1: 랜덤 움직임
  - 레벨 2: 사전 학습된 가중치를 기반으로 한 움직임
  - 레벨 3: 랜덤 플레이 통계를 기반으로 한 움직임
  - 레벨 4: 강화 학습을 기반으로 한 움직임
- AI의 예측 점수를 확인할 수 있는 옵션
- AI가 플레이어 대신 최선의 수를 놓는 옵션

## 지원 Operating Systems
|OS| 지원 여부 |
|-----|--------|
|windows | :o:  |
| Linux  | :x: |
|MacOS  | :x:  |

## 설치 방법

### Windows

1. python3.12를 설치한다(3.10 이상이면 된다.)
2. swiging을 설치한다
```
1. https://sourceforge.net/projects/swig/files/swigwin/swigwin-3.0.2/swigwin-3.0.2.zip/download 에서 파일 다운로드

2. C:\ 경로에 압축해제

3. 시작 > 시스템 환경변수 > 환경 변수... > 시스템 변수, Path, 편집 > 새로만들기, 편집 C:\swigwin-3.0.2 추가 
```
3. Microsoft Visual c++ Build Tools 설치
```
1. https://visualstudio.microsoft.com/ko/visual-cpp-build-tools/ 에서   Build Tools 다운로드 후 실행

2. Visual Studio Installer가 실행 된 경우 해당 버전의 "수정(Modify)" 클릭

3. Desktop & Mobile 에서 c++ build Tools 체크 표시 이후 설치

4. 시스템 재부팅

```
4. powershell 창에서 아래 pip3 library를 설치

```
pip3 install pygame
```

5. 재부팅 이후 python3 AItictactoe.py를 실행하면 게임 창이 뜨면서 실행됨.

### Linux

1. Docker 실행

## 사용 방법

1. 게임 스크립트를 실행합니다:
    ```sh
    python AItictactoe.py
    ```
2. 화면에 표시된 지시에 따라 플레이어 수, 선공 여부, AI 레벨 등을 선택합니다.

### 조작법

- 마우스를 사용하여 셀을 클릭하여 움직임을 만듭니다.
- `B` 키를 눌러 시작 화면으로 돌아갑니다.
- `C` 키를 눌러 AI가 대신 움직이도록 합니다.
- `R` 키를 눌러 게임을 재설정합니다.
- `S` 키를 눌러 AI의 예측 점수를 표시하거나 숨깁니다.
- `Q` 키를 눌러 게임을 종료합니다.

