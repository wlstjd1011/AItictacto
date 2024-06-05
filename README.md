# 인공지능과 함께하는 틱택토 게임

- 이 프로젝트는 파이게임(Pygame)을 사용하여 구현된 틱택토(Tic Tac Toe) 게임입니다. 이 게임은 다양한 수준의 AI를 포함하며, 랜덤 플레이와 강화 학습을 포함한 다양한 방법으로 학습된 AI를 제공합니다.
- 낮은 단계의 AI의 행동 방식이나 코드를 보며, AI의 학습에 필요한 요소가 무엇인지 확인할 수 있습니다.
- 게임 규칙을 제외한 다른 정보 없이도 AI는 게임을 승리하기 위한 최선의 방법을 찾습니다.

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

1. Docker를 설치한다.
2. Dockerfile을 build한다
   ```
   docker build -t watermelon:0.1 .
   ```
3. docker container를 실행한다
   ```
   docker run -it watermelon:0.1 /bin/bash
   ```
4. 게임을 실행한다. (검증x)
   ```
   python AItictactoe.py
   ```

wsl2환경에서는 pygame창이 바로 나오지 않지만, 디버깅 과정에서 다른 부분이 정상적으로 실행되는 것을 보면 보통의 Linux환경에서는 정상적으로 실행될 것으로 예상

## 사용 방법

1. 게임 스크립트를 실행합니다:
    ```sh
    python AItictactoe.py
    ```
2. 화면에 표시된 지시에 따라 플레이어 수, 선공 여부, AI 레벨 등을 선택합니다.

### 조작법

- 마우스를 사용하여 셀을 클릭하여 다음 수를 선택합니다.
- `B` 키를 눌러 시작 화면으로 돌아갑니다.
- `C` 키를 눌러 AI가 대신 움직이도록 합니다.
- `R` 키를 눌러 게임을 재설정합니다.
- `S` 키를 눌러 AI의 예측 점수를 표시하거나 숨깁니다.
- `Q` 키를 눌러 게임을 종료합니다.

# 코드 설명(AItictactoe.py)

#### randomplay, reinforceplay

각각 level3, level4학습을 위해 스스로 게임을 진행하는 횟수

### make_move

- Description : tictactoe에서 수를 놓음
  1. 현재 board 상태, 다음 수를 놓을 차례('O'또는 'X'), 수를 놓을 위치(row, col)에 따라 수를 놓음

### check_winner

- Description : 승자를 확인
  1. 현재 보드 상태에서 승자가 있는지 확인
  2. 승자가 있다면 승자 return 없다면 None을 return

### is_board_full

- Description : 현재 보드가 가득 찼는지 확인
  1. 가득 찼다면 True return, 아니라면 False return

 ### level1

- Description : 게임의 level1에서 컴퓨터가 다음 수를 놓는 방식
  1. 빈 자리 중 아무거나 선택

 ### create_random_weight

- Description : 9개 칸 각각에 대해 (0에서 1 사이의) random weight 생성
  1. level2의 학습에 필요
  2. level3의 학습에도 속도 증가를 위해 사용됨

 ### normalization_weight

- Description : 9개 칸 각각에 대한 weight를 weight의 합이 1이 되도록 만듬
  1. level2의 학습에 필요
  2. 서로 다른 weight를 합치기 전(평균으로 만들기 전), normalization
  
 ### average_weights

- Description : 2개의 weight의 평균
  1. level2의 학습에 필요
  2. normalization한 뒤 평균을 냄

 ### playTTTself_noob

- Description : 주어진 2개의 weight를 기준으로 서로 경기
  1. 차례를 바꿔가며 weight가 가장 높은 곳(가장 우선하는 곳)을 선택해 수를 놓음
  2. 이긴 쪽의 weight를 return, 비길 경우 평균 값을 return

 ### train_noob

- Description : level2의 컴퓨터가 학습
  1. 1024=2^10개의 weight그룹 10개, 총 10240개의 weight가 playTTTself_noob을 순서를 바꿔가며 게임 진행
  2. 최종적으로 남은 10개의 weight를 평균내 level2의 컴퓨터가 우선적으로 수를 놓을 weight 도출



 ### level2

- Description : level2의 컴퓨터를 상대로 선택했을때, 컴퓨터가 train_noob에서 구한 weight에 따라 행동
  1. print를 추가해 직접 weight를 확인하거나 level2 AI 상대로 게임을 진행하면 가운데, 모서리, 변 순서로 중요도가 높다는 것을 확인할 수 있음
  2. AI가 지점에 따른 중요도는 학습했지만, 상황에 따라 행동하지는 못함

 ### generate_allboards_boards

- Description : level3, level4에 맞는 상황별 행동을 학습하기 위해 어떤 상황에서 발생하는 승, 패, 무 저장공간
  1. 현재 보드 상황 저장(선공 포함)
  2. 보드 상황에 따른 승, 패, 무를 0으로 initialize
  3. dictionary 형식으로 상황을 주면 승, 패, 무를 알 수 있도록 함.


 ### playTTTself_play_random

- Description : random하게 스스로 Tic-Tac-Toe를 플레이하고, 상황에 따른 결과를 저장
  1. 재귀적으로 승부가 날 때까지 진행(무승부 포함)
  2. 게임을 진행하며 있었던 모든 상황을 기록
  3. 승부가 나면, generate_allboards_boards로 생성한 allboards에 게임을 진행하며 있었던 상황에 승부에 대해 기록

 ### playTTTself_play_random

- Description : random하게 스스로 Tic-Tac-Toe를 플레이하고, 상황에 따른 결과를 저장
  1. 빈 칸 중 무작위로 다음 수를 선택
  2. 결정한 수를 보드에 놓고 승부를 확인
  3. 재귀적으로 승부가 날 때까지 진행(무승부 포함)
  4. 승부가 나면, generate_allboards_boards로 생성한 allboards에 게임을 진행하며 있었던 상황에 승부에 대해 기록

 ### update_allboards

- Description : allboards를 업데이트
  1. 컴퓨터 스스로 진행한 Tic-Tac-Toe에서 각 상황에서의 승, 패, 무를 기록

 ### train_play_random

- Description : level3를 위해 playTTTself_play_random으로 학습
  1. 'O', 'X'가 각각 선공으로 randomplay번 진행(기본 100000)

 ### level3

- Description : level3의 컴퓨터를 상대로 선택했을때, 컴퓨터가 level3boards에 저장된 정보를 기반으로 행동
  1. 컴퓨터는 고를 수 있는 선택지 중 자신의 승이 많아지고 패가 적어지게 선택
  2. 다음 수로 승리하는 경우는 승리는 모든 경우, 패는 0이 되므로 승리할 기회를 놓치지 않음
  3. 학습할 때 무작위로 학습했기 때문에, 상대가 무작위로 움직일 것으로 예상하고 선택하는 문제가 있음


 ### playTTTself_play_reinforce

- Description : Tic-Tac-Toe를 플레이하며 강화학습
  1. alpha(0.2)확률로 다음 수를 무작위로 선택
  2. 1-alpha(0,8)확률로 지금까지 학습한 승률 마진((승-패)/전체)가 가장 높은 수 선택
  3. 결정한 수를 보드에 놓고 승부를 확인
  4. 재귀적으로 승부가 날 때까지 진행(무승부 포함)
  5. 승부가 나면, generate_allboards_boards로 생성한 allboards에 게임을 진행하며 있었던 상황에 승부에 대해 기록

### train_play_reinforce

- Description : level4를 위해 playTTTself_play_reinforce으로 학습
  1. 'O', 'X'가 각각 선공으로 reinforceplay번 진행(기본 100000)

### level4

- Description : level4의 컴퓨터를 상대로 선택했을때, 컴퓨터가 level4boards에 저장된 정보를 기반으로 행동
  1. 가능한 다음 수 중 가장 승률이 높은 것 선택
  2. 실행 결과, level4의 컴퓨터를 상대로는 이길 수 없음
  3. 플레이어가 실수로 승리의 기회를 주는 경우 AI가 승리
  4. 개발 과정에서 alpha=0.1일때는 첫 수를 가운데에 두지 않는 사이드라인에 취약했으나, alpha=0.2로 수정 후 해결
  5. 보통 학습에서 100000 중 약 54%가 무승부, 37%가 선공 승리, 9%가 선공 패배
  6. 10000번 중에서는 32%정도가 무승부, 50000번은 53%, 200000에서는 54.5%인 것을 보면 100000 또는 그보다 약간 더 큰 수가 적절
  7. 게임에서 보여주는 AI의 분석, 선택은 level4 기반

### line 288~315

- Description : pygame 기본 설정
  
### draw_board

- Description : 게임 진행 중의 화면.
  1. 게임 진행 중의 게임판
  2. 게임 중 사용할 수 있는 단축키(오른쪽)
  3. AI가 평가하는 현재 상황(현재 상황에서 승, 패, 무)

### selectfirst, selectlevel, selectplayer

- Description : 게임의 모드 선택

### 444~729 while loop

- Description : 게임 진행.
