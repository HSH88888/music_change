// ===========================================
//  레슨 01 — 한 줄씩 쌓아가는 코딩 음악 입문
//  strudel.cc 에 붙여넣고 Ctrl+Enter
//  각 STEP 의 주석(//)을 하나씩 풀어가며 들어보세요
// ===========================================

setcpm(120/4)            // 120 BPM

// STEP 1. 킥 드럼: 한 마디에 4번 "쿵 쿵 쿵 쿵"
$KICK: s("bd*4").bank("RolandTR909")

// STEP 2. 스네어/클랩: 2, 4박에 "짝"   (~ 는 쉼표)
// $CLAP: s("~ cp ~ cp").bank("RolandTR909").gain(0.7)

// STEP 3. 하이햇: 8분음표로 "츠츠츠츠", 강약 주기
// $HAT: s("hh*8").bank("RolandTR909").gain("0.4 0.25")

// STEP 4. 베이스: A 마이너 스케일, <> 는 마디마다 바뀜
// $BASS: n("<0 -2 -5 -1>*8").scale("A1:minor").s("sawtooth").lpf(600).decay(0.2).sustain(0)

// STEP 5. 코드: Am → F → C → G
// $CHORD: chord("<Am F C G>").voicing().s("sawtooth").lpf(1500).attack(0.1).release(0.5).gain(0.3).room(0.5)

// STEP 6. 멜로디: 숫자는 스케일 음 번호 (0=라, 2=도, 4=미 ...)
// $MELODY: n("<[0 2 4 7] [6 4 2 ~] [4 ~ 2 0] [1 ~ ~ ~]>").scale("A4:minor").s("triangle").room(0.4).gain(0.6)

// 실험해보기
//  - setcpm 숫자를 바꿔 템포 변경
//  - "bd*4" → "bd(3,8)" 로 바꾸면 레게톤 느낌
//  - .lpf(600) 숫자를 200~3000 사이로 바꿔보기
//  - .bank("RolandTR808") 로 드럼머신 바꾸기
