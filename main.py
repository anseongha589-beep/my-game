import streamlit as st
import streamlit.components.v1 as components
import time
import random
from pathlib import Path

st.set_page_config(
    page_title="ABANDONED HOSPITAL",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------------
# 키보드 입력 컴포넌트
# -------------------------------------
keyboard = components.declare_component(
    "hospital_keyboard",
    path=str(Path(__file__).parent / "keyboard")
)

# -------------------------------------
# 게임 설정
# -------------------------------------
GAME_TIME = 30 * 60

ROOMS = {
    "ward": {
        "name": "폐쇄 병동",
        "description": "오래된 침대와 먼지 쌓인 책상들이 놓여 있다.",
        "color": "#26343b",
        "objects": {
            "침대 위 메모": (1, 1),
            "벽의 달력": (4, 1),
            "낡은 책상": (1, 3),
            "잠긴 서랍장": (3, 3),
            "기록 보관실 문": (4, 4),
        },
    },
    "records": {
        "name": "기록 보관실",
        "description": "환자 기록이 가득한 어두운 보관실이다.",
        "color": "#302c3a",
        "objects": {
            "환자 기록 선반": (1, 1),
            "색깔 분류표": (3, 1),
            "잠긴 보관 서랍": (1, 3),
            "중앙 통제실 문": (4, 4),
        },
    },
    "control": {
        "name": "중앙 통제실",
        "description": "오래된 발전기와 작동하지 않는 모니터가 보인다.",
        "color": "#34352b",
        "objects": {
            "발전기": (1, 1),
            "스위치": (3, 1),
            "순서 메모": (1, 3),
            "지하 엘리베이터": (4, 4),
        },
    },
    "basement": {
        "name": "지하 출구",
        "description": "차가운 공기가 흐르는 지하 통로다.",
        "color": "#263238",
        "objects": {
            "배관 메모": (1, 1),
            "비상등": (3, 1),
            "문패": (1, 3),
            "최종 탈출문": (4, 4),
        },
    },
}

# 벽과 장애물
WALLS = {
    "ward": {(2, 0), (2, 1), (2, 2), (0, 4)},
    "records": {(2, 2), (2, 3), (3, 3), (0, 2)},
    "control": {(2, 0), (2, 1), (2, 2), (0, 3)},
    "basement": {(2, 2), (3, 2), (0, 1)},
}

# -------------------------------------
# 세션 상태
# -------------------------------------
def initialize_game():
    defaults = {
        "started": False,
        "finished": False,
        "escaped": False,
        "start_time": None,
        "remaining": GAME_TIME,
        "room": "ward",
        "player": [2, 4],
        "inventory": [],
        "notes": [],
        "investigated": [],
        "attempts": 0,
        "hints": 0,
        "message": "화면을 클릭하고 WASD로 이동하세요.",
        "last_key_id": None,
        "password_input": "",
        "password_target": None,
        "password_title": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


initialize_game()

# -------------------------------------
# 게임 유틸리티
# -------------------------------------
def add_note(note):
    if note not in st.session_state.notes:
        st.session_state.notes.append(note)


def has_item(item):
    return item in st.session_state.inventory


def add_item(item):
    if not has_item(item):
        st.session_state.inventory.append(item)


def remaining_time():
    if st.session_state.start_time is None:
        return GAME_TIME

    elapsed = int(time.time() - st.session_state.start_time)
    return max(0, GAME_TIME - elapsed)


def finish_game(escaped):
    st.session_state.finished = True
    st.session_state.escaped = escaped
    st.session_state.remaining = remaining_time()


def open_password(title, target):
    st.session_state.password_title = title
    st.session_state.password_target = target
    st.session_state.password_input = ""


def change_room(room):
    st.session_state.room = room
    st.session_state.player = [2, 4]
    st.session_state.message = f"{ROOMS[room]['name']}에 들어왔습니다."


# -------------------------------------
# 오브젝트 조사
# -------------------------------------
def investigate(name):
    room = st.session_state.room

    # 폐쇄 병동
    if room == "ward":

        if name == "침대 위 메모":
            add_note("침대 메모: 서랍의 비밀번호는 네 자리 숫자다.")
            st.session_state.message = "침대 밑에서 찢어진 메모를 발견했다."

        elif name == "벽의 달력":
            add_note("달력: 2월 4일에 붉은색으로 표시되어 있다. 암호 단서일까?")
            st.session_state.message = "달력에서 2월 4일을 발견했다."

        elif name == "낡은 책상":
            add_note("책상 메모: 서랍 암호는 날짜와 관련이 있다.")
            st.session_state.message = "책상 위에 낡은 기록이 놓여 있다."

        elif name == "잠긴 서랍장":
            open_password("폐쇄 병동 서랍 암호", "ward_drawer")

        elif name == "기록 보관실 문":
            if has_item("병동 열쇠"):
                change_room("records")
            else:
                st.session_state.message = "문이 잠겨 있다. 병동 열쇠가 필요하다."

    # 기록 보관실
    elif room == "records":

        if name == "환자 기록 선반":
            add_note("기록 선반: 파랑, 노랑, 빨강, 초록 순서로 읽으라는 표시가 있다.")
            st.session_state.message = "색깔 순서가 적힌 기록을 발견했다."

        elif name == "색깔 분류표":
            add_note("분류표: 파랑=5, 노랑=8, 빨강=3, 초록=1")
            st.session_state.message = "색깔별 숫자를 확인했다."

        elif name == "잠긴 보관 서랍":
            open_password("기록 보관실 서랍 암호", "records_drawer")

        elif name == "중앙 통제실 문":
            if has_item("비상 퓨즈"):
                change_room("control")
            else:
                st.session_state.message = "전원이 차단되어 문이 열리지 않는다."

    # 중앙 통제실
    elif room == "control":

        if name == "발전기":
            if has_item("비상 퓨즈"):
                add_note("발전기: 퓨즈를 장착하면 전원을 복구할 수 있다.")
                st.session_state.message = "발전기에서 퓨즈 장착부를 발견했다."
            else:
                st.session_state.message = "퓨즈가 없어 발전기를 작동시킬 수 없다."

        elif name == "스위치":
            open_password("발전기 작동 순서", "control_switch")

        elif name == "순서 메모":
            add_note("통제실 메모: 발전기 작동 순서는 3-1-4-2")
            st.session_state.message = "발전기 작동 순서가 적혀 있다."

        elif name == "지하 엘리베이터":
            if "전력 복구" in st.session_state.notes:
                change_room("basement")
            else:
                st.session_state.message = "엘리베이터에 전력이 공급되지 않는다."

    # 지하 출구
    elif room == "basement":

        if name == "배관 메모":
            add_note("배관 메모: 마지막 문에는 네 자리 숫자가 필요하다.")
            st.session_state.message = "배관 옆에서 메모를 발견했다."

        elif name == "비상등":
            add_note("비상등: 벽에 숫자 7이 희미하게 적혀 있다.")
            st.session_state.message = "비상등 아래 숫자 7을 발견했다."

        elif name == "문패":
            add_note("문패: 각 구역에서 숫자를 하나씩 찾아 순서대로 입력하라.")
            add_note("병동 숫자 7, 기록실 숫자 3, 통제실 숫자 1, 지하 숫자 9")
            st.session_state.message = "네 구역의 숫자를 순서대로 모아야 한다."

        elif name == "최종 탈출문":
            open_password("최종 탈출문 암호", "final_door")


# -------------------------------------
# 비밀번호 확인
# -------------------------------------
def check_password():
    answer = st.session_state.password_input.strip()
    target = st.session_state.password_target

    st.session_state.attempts += 1

    if target == "ward_drawer" and answer == "2417":
        add_item("병동 열쇠")
        st.session_state.message = "서랍이 열렸다! 병동 열쇠를 획득했다."
        add_note("서랍 안에서 병동 열쇠를 발견했다.")

    elif target == "records_drawer" and answer == "5831":
        add_item("비상 퓨즈")
        st.session_state.message = "비상 퓨즈를 획득했다!"
        add_note("보관 서랍에서 비상 퓨즈를 발견했다.")

    elif target == "control_switch" and answer == "3142":
        if has_item("비상 퓨즈"):
            add_note("전력 복구")
            st.session_state.message = "발전기가 작동했다. 엘리베이터 전원이 복구되었다."
        else:
            st.session_state.message = "비상 퓨즈가 없어 작동할 수 없다."

    elif target == "final_door" and answer == "7319":
        finish_game(True)
        st.session_state.message = "탈출에 성공했다!"

    else:
        st.session_state.message = "암호가 틀렸다. 단서를 다시 확인하자."

    st.session_state.password_target = None
    st.session_state.password_input = ""


# -------------------------------------
# 플레이어 이동
# -------------------------------------
def move_player(key):
    room = st.session_state.room
    x, y = st.session_state.player

    directions = {
        "w": (0, -1),
        "a": (-1, 0),
        "s": (0, 1),
        "d": (1, 0),
    }

    if key not in directions:
        return

    dx, dy = directions[key]
    nx, ny = x + dx, y + dy

    if not (0 <= nx <= 4 and 0 <= ny <= 4):
        return

    if (nx, ny) in WALLS[room]:
        st.session_state.message = "벽에 막혀 있다."
        return

    st.session_state.player = [nx, ny]


def nearby_object():
    room = st.session_state.room
    x, y = st.session_state.player

    for name, (ox, oy) in ROOMS[room]["objects"].items():
        distance = abs(x - ox) + abs(y - oy)
        if distance <= 1:
            return name

    return None


def interact():
    obj = nearby_object()

    if obj:
        investigate(obj)
    else:
        st.session_state.message = "주변에 조사할 물체가 없다."


# -------------------------------------
# CSS
# -------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

.stApp {
    background: #090d10;
    color: #d7e0e3;
    font-family: 'Share Tech Mono', monospace;
}

.block-container {
    max-width: 1200px;
    padding-top: 1.5rem;
}

h1, h2, h3 {
    color: #d9e3e5 !important;
}

.game-panel {
    background: #111a20;
    border: 1px solid #34434a;
    padding: 18px;
    border-radius: 8px;
    margin-bottom: 12px;
}

.game-title {
    color: #d6e4e7;
    font-size: 34px;
    letter-spacing: 5px;
    text-align: center;
}

.subtitle {
    color: #80949b;
    text-align: center;
    letter-spacing: 3px;
}

.status {
    color: #d8b66a;
    font-size: 18px;
}

.object-card {
    background: #202c32;
    border: 1px solid #56646a;
    border-radius: 5px;
    padding: 10px;
    text-align: center;
}

.player-card {
    background: #263f48;
    border: 2px solid #b7dce5;
    border-radius: 5px;
    padding: 12px;
    text-align: center;
    font-size: 22px;
}

.wall-card {
    background: #080b0d;
    border: 1px solid #151c20;
    padding: 12px;
    text-align: center;
}

.floor-card {
    background: #17242a;
    border: 1px solid #28383e;
    padding: 12px;
    text-align: center;
}

div.stButton > button {
    background: #263840;
    color: #e0e8ea;
    border: 1px solid #63747a;
    border-radius: 4px;
}

div.stButton > button:hover {
    background: #3b515a;
    color: white;
    border-color: #a4c1ca;
}

</style>
""", unsafe_allow_html=True)


# -------------------------------------
# 타이틀 화면
# -------------------------------------
if not st.session_state.started:

    st.markdown("<div class='game-title'>ABANDONED HOSPITAL</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>THE LAST ESCAPE</div>", unsafe_allow_html=True)

    st.write("")
    st.write("")

    st.image(
        "https://images.unsplash.com/photo-1518709268805-4e9042af9f23",
        use_container_width=True
    )

    st.markdown("""
    <div class='game-panel'>
    <h3>MISSION BRIEFING</h3>
    버려진 병원에서 눈을 떴다.<br><br>
    출입문은 잠겨 있고, 건물의 전력은 차단되어 있다.<br>
    곳곳에 숨겨진 단서를 찾아 암호를 풀고 탈출해야 한다.<br><br>
    <b>제한 시간: 30분</b><br>
    <b>목표: 네 개의 구역을 탐험하고 최종 출구를 찾아라.</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 조작 방법")
    st.markdown("""
    - `W` : 위로 이동
    - `A` : 왼쪽으로 이동
    - `S` : 아래로 이동
    - `D` : 오른쪽으로 이동
    - `E` : 주변 물체 조사
    """)

    if st.button("▶ 게임 시작", use_container_width=True):
        st.session_state.started = True
        st.session_state.start_time = time.time()
        st.rerun()

    st.stop()


# -------------------------------------
# 타이머
# -------------------------------------
@st.fragment(run_every="1s")
def timer_display():
    left = remaining_time()
    minutes = left // 60
    seconds = left % 60

    st.markdown(
        f"<div class='status'>⏱ REMAINING TIME : {minutes:02d}:{seconds:02d}</div>",
        unsafe_allow_html=True
    )

    if left <= 0 and not st.session_state.finished:
        finish_game(False)
        st.rerun()


# -------------------------------------
# 종료 화면
# -------------------------------------
if st.session_state.finished:

    st.markdown("<div class='game-title'>MISSION COMPLETE</div>", unsafe_allow_html=True)

    if st.session_state.escaped:
        st.success("탈출 성공! 당신은 버려진 병원에서 살아 나왔다.")

        elapsed = GAME_TIME - st.session_state.remaining
        grade = "S"

        if st.session_state.hints >= 3 or st.session_state.attempts >= 8:
            grade = "B"
        elif st.session_state.hints >= 1 or st.session_state.attempts >= 5:
            grade = "A"

        st.markdown(f"## 최종 등급: {grade}")
        st.metric("탈출 소요 시간", f"{elapsed // 60}분 {elapsed % 60}초")
        st.metric("암호 입력 횟수", st.session_state.attempts)
        st.metric("사용한 힌트", st.session_state.hints)

    else:
        st.error("시간이 모두 지났다. 탈출에 실패했다.")

    if st.button("다시 플레이", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.stop()


# -------------------------------------
# 게임 화면
# -------------------------------------
left, right = st.columns([2.2, 1])

with left:
    st.markdown("<div class='game-title'>ABANDONED HOSPITAL</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='subtitle'>{ROOMS[st.session_state.room]['name']}</div>",
        unsafe_allow_html=True
    )

with right:
    timer_display()

st.divider()

# 키보드 입력
key_event = keyboard(
    key="hospital_keys",
    default=None
)

if key_event and key_event != st.session_state.last_key_id:
    st.session_state.last_key_id = key_event

    key = key_event.get("key", "").lower() if isinstance(key_event, dict) else str(key_event).lower()

    if key in ["w", "a", "s", "d"]:
        move_player(key)
    elif key == "e":
        interact()

# -------------------------------------
# 지도
# -------------------------------------
room = st.session_state.room
player_x, player_y = st.session_state.player
objects = ROOMS[room]["objects"]
walls = WALLS[room]

st.markdown("### 🗺️ CURRENT AREA")
st.caption("화면을 클릭한 뒤 WASD로 이동하세요. 물체에 가까이 다가가 E를 누르세요.")

for y in range(5):
    cols = st.columns(5)

    for x in range(5):
        with cols[x]:

            if (x, y) == (player_x, player_y):
                st.markdown(
                    "<div class='player-card'>🧍<br>YOU</div>",
                    unsafe_allow_html=True
                )

            elif (x, y) in walls:
                st.markdown(
                    "<div class='wall-card'>⬛<br>벽</div>",
                    unsafe_allow_html=True
                )

            else:
                obj_name = None

                for name, pos in objects.items():
                    if pos == (x, y):
                        obj_name = name
                        break

                if obj_name:
                    st.markdown(
                        f"<div class='object-card'>🔎<br>{obj_name}</div>",
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        "<div class='floor-card'>·</div>",
                        unsafe_allow_html=True
                    )

# -------------------------------------
# 상호작용 안내
# -------------------------------------
st.write("")

obj = nearby_object()

if obj:
    st.info(f"🔎 가까이 있는 물체: **{obj}** — E키를 눌러 조사하세요.")
else:
    st.caption("주변에 조사할 수 있는 물체가 없습니다.")

st.markdown(f"**상태:** {st.session_state.message}")

# -------------------------------------
# 암호 입력
# -------------------------------------
if st.session_state.password_target:

    st.divider()
    st.markdown(f"### 🔐 {st.session_state.password_title}")

    st.text_input(
        "네 자리 암호를 입력하세요.",
        key="password_input",
        max_chars=4
    )

    if st.button("암호 확인", use_container_width=True):
        check_password()
        st.rerun()

# -------------------------------------
# 인벤토리와 기록
# -------------------------------------
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🎒 INVENTORY")

    if st.session_state.inventory:
        for item in st.session_state.inventory:
            st.write(f"🔑 {item}")
    else:
        st.caption("아직 획득한 아이템이 없습니다.")

with col2:
    st.markdown("### 📓 CLUE LOG")

    if st.session_state.notes:
        for note in st.session_state.notes:
            st.write(f"• {note}")
    else:
        st.caption("아직 발견한 단서가 없습니다.")

# -------------------------------------
# 힌트
# -------------------------------------
with st.expander("💡 힌트 확인"):
    st.write("각 구역의 메모와 주변 물체를 자세히 조사하세요.")

    if st.button("힌트 보기"):
        st.session_state.hints += 1

        hints = {
            "ward": "달력의 2월 4일과 병동 메모를 확인하세요. 첫 암호는 2417입니다.",
            "records": "색깔 순서는 파랑, 노랑, 빨강, 초록입니다. 숫자를 이어 붙이세요.",
            "control": "순서 메모에 적힌 네 숫자를 확인하세요. 퓨즈도 필요합니다.",
            "basement": "각 구역에서 찾은 숫자를 순서대로 연결하세요.",
        }

        st.warning(hints[st.session_state.room])

# -------------------------------------
# 구역 정보
# -------------------------------------
st.divider()
st.markdown("### 📍 AREA STATUS")

room_names = {
    "ward": "폐쇄 병동",
    "records": "기록 보관실",
    "control": "중앙 통제실",
    "basement": "지하 출구",
}

for key, name in room_names.items():
    if key == room:
        st.markdown(f"🔴 **{name} — 현재 위치**")
    else:
        st.markdown(f"⚫ {name}")
