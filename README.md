## ETTTP Project 👾

![UI](https://github.com/user-attachments/assets/a14fa132-1678-4104-a302-731e45400042)
TCP/IP 기반으로 구현한 파이썬 Tic-Tac-Toe 프로그램입니다.

## 기술 스택
- Python 3.x
- tkinter (GUI)
- Socket Programming
- Threading

## 주요 기능

**Rules**
- 3x3 보드에서 진행되는 틱택토 게임
- 서버와 클라이언트가 번갈아가며 수를 둠
- 한 줄을 먼저 완성하는 플레이어가 승리

**Network**
- TCP/IP 기반 통신
- 커스텀 ETTTP 프로토콜 사용
- 실시간 게임 상태 동기화

**UI**
- 게임 보드 표시
- 현재 턴 표시 ("Ready" / "Hold")
- 게임 결과 표시
- 디버그 메시지 입력 기능

## 프로젝트 구조
```
ETTTP/
├── ETTTP_Server.py     # 서버
├── ETTTP_Client.py     # 클라이언트
├── ETTTP_TicTacToe.py  # 게임 로직 및 UI
└── README.md           # 프로젝트 문서
```

## 실행 방법

```
# 1. 서버 실행
$ python ETTTP_Server.py

# 2. 클라이언트 실행
$ python ETTTP_Client.py
```

## Protocol

**메세지 포맷**
```
[TYPE] ETTTP/1.0
Host:[IP_ADDRESS]
[COMMAND]:[VALUE]
```
**메세지 타입**
- `SEND`: 게임 동작 전송
- `ACK`: 수신 확인
- `RESULT`: 게임 결과 전송

## 개발 환경 설정
- Python 3.x 설치
- tkinter 라이브러리 설치 확인
