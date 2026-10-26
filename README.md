# music_change — 코드로 음악 만들기 (Strudel)

영상 속 화면은 **[Strudel](https://strudel.cc)** 이라는 무료 웹 라이브코딩 도구입니다.
설치 없이 브라우저에서 바로 코드를 쳐서 음악을 만들 수 있어요.

## 시작하는 법 (3분)

1. 브라우저(크롬 권장)에서 <https://strudel.cc> 접속
2. 에디터 내용을 전부 지우고, 이 저장소의 `tracks/` 폴더 파일 하나를 복사해 붙여넣기
3. **Ctrl + Enter** (맥: Cmd + Enter) → 재생 / 코드 수정 후 다시 누르면 즉시 반영
4. **Ctrl + .** → 정지

## 파일

| 파일 | 내용 |
|---|---|
| `tracks/01_basics.js` | 한 줄씩 따라 하는 입문 레슨 (드럼 → 베이스 → 코드 → 멜로디) |
| `tracks/02_midnight_drive.js` | 영상과 같은 구성(DRUM / BASS / SYNTH / SUB / PAD)의 완성곡 예제 |

## 영상 코드 읽는 법 (핵심 문법 요약)

| 코드 | 뜻 |
|---|---|
| `setcpm(130/4)` | 템포. 130 BPM, 4박 = 1사이클 |
| `$DRUM: ...` | 이름 붙인 트랙(레이어). 여러 개가 동시에 재생됨 |
| `s("bd sd hh")` | 소리(sample) 재생. bd=킥, sd=스네어, hh=하이햇, cp=클랩 |
| `"bd(3,8)"` | 유클리드 리듬: 8칸에 3번 고르게 |
| `"hh*8"` | 한 사이클에 8번 반복 |
| `"<a b>"` | 사이클마다 번갈아 가며 하나씩 |
| `"[a b]"` | 한 칸을 쪼개서 a, b 를 빠르게 |
| `-` 또는 `~` | 쉼표 |
| `@4` | 그 음을 4칸 길이로 늘림 |
| `n("0 2 4").scale("C3:minor")` | 스케일의 0,2,4번째 음 (도-미♭-솔) |
| `chord("Cm7").voicing()` | 코드를 자동으로 보이싱 |
| `.bank("RolandTR909")` | 드럼머신 종류 선택 |
| `.lpf(800)` | 로우패스 필터 (숫자 낮을수록 먹먹) |
| `.room(0.5)` | 리버브 |
| `.attack / .decay / .sustain / .release` | 소리 엔벨로프(ADSR) |
| `.gain(0.8)` | 볼륨 |
| `.pan(0.5)` | 좌우 위치 (0=왼쪽, 1=오른쪽) |
| `.juxBy(0.5, x => x.late(0.01))` | 오른쪽 채널만 살짝 변형 → 스테레오 넓게 |
| `.distort(0.8)` | 디스토션 |
| `.orbit(2)` | 이펙트 버스 분리 (리버브 등이 섞이지 않게) |

## 커버곡 만드는 요령

1. 원곡 **키와 BPM** 찾기 (검색: "곡명 key bpm", 예: tunebat.com)
2. `setcpm(BPM/4)`, `const KEY = "C3:minor"` 처럼 맞춰두기
3. **드럼 → 베이스 → 코드 → 멜로디** 순서로 한 레이어씩 귀로 따서 추가
4. 멜로디는 스케일 숫자(`n("0 2 4")`)로 쓰면 키를 바꿔도 그대로 따라옴

## 더 배우기

- 공식 튜토리얼(한 단계씩 인터랙티브): <https://strudel.cc/workshop/getting-started/>
- 함수 레퍼런스: <https://strudel.cc/learn/>

## 들어보기

`renders/midnight_drive.mp3` 는 `tracks/02_midnight_drive.js` 를 파이썬으로 합성해 미리 들어볼 수 있게 만든 파일입니다
(Strudel 실제 소리와는 음색이 조금 다릅니다). 다시 만들려면:

```bash
pip install numpy scipy
python3 render/render_midnight_drive.py out.wav
```
