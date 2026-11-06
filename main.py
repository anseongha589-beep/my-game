
import streamlit as st
import time
from datetime import datetime, timedelta

# ============================================================
# ABANDONED HOSPITAL
# 2D TOP-DOWN ESCAPE ROOM
# ============================================================

st.set_page_config(
    page_title="ABANDONED HOSPITAL",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------
# CSS
# ------------------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

.stApp {
    background: #090e16;
    color: #e1e8ed;
    font-family: 'Noto Sans KR', sans-serif;
}

[data-testid="stSidebar"] {
    background: #101923;
    border-right: 1px solid #283b48;
}

h1, h2, h3 {
    color: #e8f2f5 !important;
}

p, label {
    color: #bdcbd2;
}

div[data-testid="stMetric"] {
    background: #15222d;
    border: 1px solid #344b59;
    border-radius: 10px;
    padding: 15px;
}

div[data-testid="stMetricValue"] {
    color: #7bd8c8;
    font-family: 'Share Tech Mono', monospace;
}

div.stButton > button {
    background: #172832;
    color: #dce9ed;
    border: 1px solid #385360;
    border-radius: 8px;
    min-height: 42px;
    font-weight: 700;
}

div.stButton > button:hover {
    background: #244451;
    border-color: #75d6c5;
    color: white;
}

div.stButton > button:disabled {
    background: #111a22;
    color: #53636d;
}

div.stButton > button[kind="primary"] {
    background: #176b63;
    border-color: #4cc4ae;
    color: white;
}

.room-banner {
    background: linear-gradient(110deg, #14222d, #1b3039);
    border: 1px solid #3b5b65;
    border-radius: 12px;
    padding: 22px;
    margin-bottom: 15px;
}

.room-number {
    font-family: 'Share Tech Mono', monospace;
    color: #70cbbb;
    letter-spacing: 3px;
    font-size: 12px;
}

.room-name {
    font-size: 27px;
    font-weight: 900;
    color: #f1f7f8;
    margin-top: 7px;
}

.room-description {
    color: #aebfc7;
    line-height: 1.8;
    margin-top: 8px;
}

.map-tile {
    text-align: center;
    background: #182934;
    border: 1px solid #344c58;
    border-radius: 7px;
    padding: 9px 2px;
    min-height: 56px;
}

.map-wall {
    background: #26333c;
    border-color: #43525b;
}

.map-floor {
    background: #111c25;
    border-color: #1e303a;
}

.object-card {
    background: #172832;
    border: 1px solid #405964;
    border-radius: 10px;
    padding: 17px;
    margin: 10px 0;
}

.clue-card {
    background: #1a2b32;
    border-left: 4px solid #6ac8b5;
    padding: 15px;
    border-radius: 7px;
    margin: 8px 0;
}

.inventory-card {
    background: #182b34;
    border: 1px solid #41616a;
    border-radius: 9px;
    padding: 12px;
    text-align: center;
}

.danger-text {
    color: #ff7777;
    font-family: 'Share Tech Mono', monospace;
}

.timer {
    font-family: 'Share Tech Mono', monospace;
    font-size: 30px;
    font-weight: bold;
    color: #80dfc7;
}

hr {
    border-color: #2b404a;
}

.stProgress > div > div > div > div {
    background: #63c8b2;
}
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# GAME CONFIGURATION
# ------------------------------------------------------------

GAME_SECONDS = 30 * 60

ROOMS = {
    "ward": {
        "name": "폐쇄 병동",
        "number": "AREA 01",
        "icon": "🛏️",
        "description": "오래된 침대와 녹슨 가구가 놓여 있다. 벽에는 날짜가 적힌 달력이 걸려 있다.",
        "plaque": "7",
        "objects": {
            "bed": {
                "name": "낡은 침대",
                "icon": "🛏️",
                "position": (0, 1),
                "description": "매트리스 아래에서 접힌 메모를 발견했다.",
                "clue": "메모: '달력에서 표시된 날짜를 시간 순서대로 확인하라.'",
                "item": "환자 메모"
            },
            "calendar": {
                "name": "벽걸이 달력",
                "icon": "📅",
                "position": (0, 3),
                "description": "달력의 일부 날짜에 붉은 원이 그려져 있다.",
                "clue": "2일, 4일, 1일, 7일이 순서대로 표시되어 있다. 메모와 함께 생각해 보자.",
                "item": None
            },
            "desk": {
                "name": "낡은 책상",
                "icon": "🗄️",
                "position": (2, 0),
                "description": "책상 위에 오래된 업무 기록이 있다.",
                "clue": "기록: '이 병동의 모든 문은 네 자리 숫자로 잠겨 있다.'",
                "item": "업무 기록"
            },
            "cabinet": {
                "name": "잠긴 서랍장",
                "icon": "🔒",
                "position": (2, 4),
                "description": "숫자 네 자리로 잠긴 서랍장이다.",
                "clue": "숫자 암호를 입력해야 한다.",
                "item": None
            },
            "plaque": {
                "name": "병동 문패",
                "icon": "🔢",
                "position": (4, 0),
                "description": "벽에 붙은 오래된 병동 번호표다.",
                "clue": "번호: 7. 이 숫자는 마지막 출구 암호에 필요할지도 모른다.",
                "item": "병동 번호 기록"
            },
            "door": {
                "name": "기록 보관실 문",
                "icon": "🚪",
                "position": (4, 4),
                "description": "두꺼운 철문이다. 열쇠가 필요한 것 같다.",
                "clue": "서랍장에서 열쇠를 찾아야 한다.",
                "item": None
            }
        }
    },

    "records": {
        "name": "기록 보관실",
        "number": "AREA 02",
        "icon": "📚",
        "description": "수많은 환자 기록이 쌓여 있다. 벽면의 색깔 표와 오래된 서류가 눈에 띈다.",
        "plaque": "3",
        "objects": {
            "shelf": {
                "name": "환자 기록 선반",
                "icon": "📚",
                "position": (0, 1),
                "description": "특정 색으로 분류된 환자 기록이 있다.",
                "clue": "기록 메모: '파랑 → 노랑 → 빨강 → 초록 순서로 기록번호를 읽어라.'",
                "item": "분류 메모"
            },
            "chart": {
                "name": "색깔 분류표",
                "icon": "🎨",
                "position": (0, 3),
                "description": "네 가지 색깔 옆에 숫자가 기록되어 있다.",
                "clue": "파랑=5, 노랑=8, 빨강=3, 초록=1",
                "item": None
            },
            "drawer": {
                "name": "기록 잠금 서랍",
                "icon": "🔒",
                "position": (2, 0),
                "description": "네 자리 숫자 암호로 잠겨 있다.",
                "clue": "색깔 분류표의 순서를 이용하라.",
                "item": None
            },
            "plaque": {
                "name": "보관실 문패",
                "icon": "🔢",
                "position": (2, 4),
                "description": "벽에 붙은 보관실 번호표다.",
                "clue": "번호: 3. 마지막 출구 암호에 필요하다.",
                "item": "보관실 번호 기록"
            },
            "note": {
                "name": "낡은 진료 기록",
                "icon": "📜",
                "position": (4, 0),
                "description": "의사가 남긴 짧은 기록이다.",
                "clue": "기록: '전력 없이는 지하로 내려갈 수 없다. 퓨즈를 찾아라.'",
                "item": "진료 기록"
            },
            "door": {
                "name": "중앙 통제실 문",
                "icon": "🚪",
                "position": (4, 4),
                "description": "전자 잠금장치가 달린 문이다.",
                "clue": "통제실로 이동하려면 기록 서랍을 열어야 한다.",
                "item": None
            }
        }
    },

    "control": {
        "name": "중앙 통제실",
        "number": "AREA 03",
        "icon": "⚡",
        "description": "꺼진 모니터와 전기 장치가 가득하다. 이곳에서 지하 전력을 복구할 수 있을 것 같다.",
        "plaque": "1",
        "objects": {
            "generator": {
                "name": "비상 발전기",
                "icon": "⚡",
                "position": (0, 1),
                "description": "전원이 꺼져 있다. 퓨즈가 있어야 작동할 것 같다.",
                "clue": "전력 장치의 퓨즈 슬롯이 비어 있다.",
                "item": None
            },
            "switch": {
                "name": "제어 스위치",
                "icon": "🎛️",
                "position": (0, 3),
                "description": "네 개의 숫자 입력 버튼이 있는 제어 장치다.",
                "clue": "벽면의 스위치 순서 메모를 찾아야 한다.",
                "item": None
            },
            "memo": {
                "name": "스위치 순서 메모",
                "icon": "📝",
                "position": (2, 0),
                "description": "기계 뒤에 끼워진 작은 메모다.",
                "clue": "메모: '제어 순서는 3번째 → 1번째 → 4번째 → 2번째.'",
                "item": "제어 메모"
            },
            "plaque": {
                "name": "통제실 문패",
                "icon": "🔢",
                "position": (2, 4),
                "description": "벽의 낡은 번호표다.",
                "clue": "번호: 1. 마지막 출구 암호에 필요하다.",
                "item": "통제실 번호 기록"
            },
            "elevator": {
                "name": "지하 엘리베이터",
                "icon": "🛗",
                "position": (4, 4),
                "description": "지하로 내려가는 엘리베이터다.",
                "clue": "전력이 복구되면 작동할 것이다.",
                "item": None
            }
        }
    },

    "basement": {
        "name": "지하 출구",
        "number": "AREA 04",
        "icon": "🚪",
        "description": "차가운 지하 통로 끝에 마지막 철문이 있다. 이제 탈출할 시간이 얼마 남지 않았다.",
        "plaque": "9",
        "objects": {
            "pipe": {
                "name": "녹슨 배관",
                "icon": "🔧",
                "position": (0, 1),
                "description": "배관 표면에 여러 숫자가 긁혀 있다.",
                "clue": "메모: '각 구역의 문패 숫자를 처음부터 방문한 순서대로 나열하라.'",
                "item": "출구 암호 메모"
            },
            "light": {
                "name": "비상등",
                "icon": "💡",
                "position": (0, 3),
                "description": "희미하게 깜빡이는 비상등이다.",
                "clue": "전력이 복구된 후에야 밝게 켜진다.",
                "item": None
            },
            "plaque": {
                "name": "지하 출구 문패",
                "icon": "🔢",
                "position": (2, 0),
                "description": "마지막 구역의 문패다.",
                "clue": "번호: 9. 다른 구역의 문패 숫자와 함께 사용하자.",
                "item": "지하 번호 기록"
            },
            "exit": {
                "name": "최종 탈출문",
                "icon": "🚨",
                "position": (2, 4),
                "description": "네 자리 숫자 암호가 필요한 마지막 문이다.",
                "clue": "모든 구역의 문패 번호를 방문 순서대로 입력하라.",
                "item": None
            }
        }
    }
}


# ------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------

def init_state():
    defaults = {
        "started": False,
        "deadline": None,
        "room": "ward",
        "selected": None,
        "inventory": [],
        "examined": [],
        "unlocked": [],
        "notes": [],
        "hints_used": 0,
        "finished": False,
        "won": False,
        "expired": False,
        "attempts": 0,
        "events": [],
        "game_start": None
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()


def has_item(item):
    return item in st.session_state.inventory


def add_item(item):
    if item and not has_item(item):
        st.session_state.inventory.append(item)
        st.session_state.events.append(f"아이템 획득: {item}")


def add_note(note):
    if note not in st.session_state.notes:
        st.session_state.notes.append(note)


def unlock(name):
    if name not in st.session_state.unlocked:
        st.session_state.unlocked.append(name)


def elapsed_seconds():
    if not st.session_state.started or not st.session_state.deadline:
        return GAME_SECONDS

    return max(
        0,
        int((st.session_state.deadline - datetime.now()).total_seconds())
    )


def reset_game():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

    init_state()


def start_game():
    st.session_state.started = True
    st.session_state.game_start = datetime.now()
    st.session_state.deadline = datetime.now() + timedelta(
        seconds=GAME_SECONDS
    )
    st.session_state.room = "ward"
    st.session_state.selected = None
    st.rerun()


def lose_game():
    st.session_state.expired = True
    st.session_state.finished = True
    st.session_state.won = False


# ------------------------------------------------------------
# TIMER
# ------------------------------------------------------------

@st.fragment(run_every="1s")
def timer_display():
    if not st.session_state.started:
        return

    if st.session_state.finished:
        return

    remaining = elapsed_seconds()

    if remaining <= 0:
        lose_game()
        st.rerun()

    minutes = remaining // 60
    seconds = remaining % 60

    color = "#ff6969" if remaining <= 300 else "#80dfc7"

    st.markdown(
        f"""
        <div style="
            background:#14232e;
            border:1px solid #38515d;
            padding:12px;
            border-radius:10px;
            text-align:center;
        ">
            <div style="font-size:11px;letter-spacing:3px;color:#a9bdc5;">
                TIME REMAINING
            </div>
            <div style="
                font-family:monospace;
                font-size:34px;
                font-weight:bold;
                color:{color};
            ">
                {minutes:02d}:{seconds:02d}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# GAME LOGIC
# ------------------------------------------------------------

def examine_object(object_id):
    st.session_state.selected = object_id

    current = ROOMS[st.session_state.room]
    obj = current["objects"][object_id]

    unique = f"{st.session_state.room}_{object_id}"

    if unique not in st.session_state.examined:
        st.session_state.examined.append(unique)

    st.session_state.events.append(
        f"{current['name']} - {obj['name']} 조사"
    )


def check_password(kind, password):
    st.session_state.attempts += 1

    # FIRST ROOM
    if kind == "ward_cabinet":
        if password == "2417":
            unlock("ward_cabinet")
            add_item("기록 보관실 열쇠")
            st.success("잠금 해제 성공! 기록 보관실 열쇠를 획득했습니다.")
            return True

    # SECOND ROOM
    elif kind == "records_drawer":
        if password == "5831":
            unlock("records_drawer")
            add_item("비상 퓨즈")
            st.success("서랍이 열렸습니다! 비상 퓨즈를 획득했습니다.")
            return True

    # THIRD ROOM
    elif kind == "control_switch":
        if password == "3142" and has_item("비상 퓨즈"):
            unlock("control_switch")
            st.success("제어 장치가 활성화되었습니다!")
            return True

    # FINAL ROOM
    elif kind == "final_exit":
        if password == "7319":
            unlock("final_exit")
            st.session_state.finished = True
            st.session_state.won = True
            st.success("탈출 성공!")
            return True

    st.error("암호가 틀렸습니다. 단서를 다시 확인하세요.")
    return False


def use_hint():
    st.session_state.hints_used += 1


# ------------------------------------------------------------
# START SCREEN
# ------------------------------------------------------------

if not st.session_state.started:

    st.markdown("""
    <div style="
        padding:45px 25px;
        background:linear-gradient(120deg,#111e2b,#1b3038,#101a27);
        border:1px solid #45606a;
        border-radius:16px;
        text-align:center;
    ">
        <div style="
            font-family:monospace;
            color:#78d6c3;
            letter-spacing:6px;
            font-size:14px;
        ">
            SURVIVAL ESCAPE PROJECT
        </div>
        <h1 style="font-size:48px;margin-top:20px;">
            ABANDONED<br>HOSPITAL
        </h1>
        <p style="font-size:16px;color:#b9cbd0;">
            버려진 정신병원
        </p>
        <p style="color:#8299a2;">
            30분 안에 네 개의 구역을 통과하고 탈출하라.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    a, b, c = st.columns(3)

    with a:
        st.metric("난이도", "EXTREME")

    with b:
        st.metric("제한 시간", "30 MIN")

    with c:
        st.metric("탐험 구역", "4 AREAS")

    st.markdown("### 📖 PROLOGUE")

    st.markdown("""
    당신은 낡은 정신병원에서 눈을 떴다.

    주변에는 아무도 없고, 복도에는 비상등만 희미하게 켜져 있다.

    출입문은 잠겨 있고 휴대전화도 작동하지 않는다.

    누군가 남긴 메모와 오래된 기록만이 이곳에서 나갈 방법을 알려주고 있다.

    **30분 안에 네 개의 구역을 조사하고 최종 출구를 열어야 한다.**
    """)

    st.warning(
        "매우 어려운 난이도입니다. 단서를 꼼꼼하게 기록하세요. "
        "암호 입력에 실패하면 시도 횟수가 증가합니다."
    )

    if st.button(
        "▶ GAME START",
        type="primary",
        use_container_width=True
    ):
        start_game()

    st.stop()


# ------------------------------------------------------------
# GAME OVER SCREEN
# ------------------------------------------------------------

if st.session_state.finished:

    if st.session_state.won:
        st.markdown("""
        <div style="
            padding:40px;
            background:linear-gradient(120deg,#123d36,#1c5749);
            border:1px solid #58c6a6;
            border-radius:15px;
            text-align:center;
        ">
            <div style="font-size:55px;">🎉</div>
            <h1>ESCAPE SUCCESS</h1>
            <h2>탈출에 성공했습니다!</h2>
            <p>당신은 버려진 정신병원에서 무사히 탈출했습니다.</p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="
            padding:40px;
            background:linear-gradient(120deg,#421b23,#25151d);
            border:1px solid #a74c58;
            border-radius:15px;
            text-align:center;
        ">
            <div style="font-size:55px;">⏰</div>
            <h1>TIME OVER</h1>
            <h2>탈출 실패</h2>
            <p>제한 시간이 종료되었습니다.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    elapsed = (
        int((datetime.now() - st.session_state.game_start).total_seconds())
        if st.session_state.game_start else GAME_SECONDS
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("조사한 물건", f"{len(st.session_state.examined)}개")

    with col2:
        st.metric("암호 입력 횟수", f"{st.session_state.attempts}회")

    with col3:
        st.metric("사용한 힌트", f"{st.session_state.hints_used}회")

    if st.session_state.won:
        st.write(f"**탈출 소요 시간:** {elapsed // 60}분 {elapsed % 60}초")

        if elapsed <= 600 and st.session_state.hints_used == 0:
            st.success("S RANK — 완벽한 탈출!")
        elif elapsed <= 1200:
            st.success("A RANK — 훌륭한 탈출!")
        else:
            st.info("B RANK — 탈출 성공!")

    if st.button("🔄 다시 도전하기", type="primary", use_container_width=True):
        reset_game()
        st.rerun()

    st.stop()


# ------------------------------------------------------------
# MAIN GAME HEADER
# ------------------------------------------------------------

header1, header2 = st.columns([3, 1])

with header1:
    st.markdown("""
    <div>
        <div style="
            color:#72cbb8;
            letter-spacing:3px;
            font-family:monospace;
            font-size:12px;
        ">
            ABANDONED HOSPITAL / ESCAPE SYSTEM
        </div>
        <h1 style="margin-bottom:0;">🏥 버려진 정신병원</h1>
    </div>
    """, unsafe_allow_html=True)

with header2:
    timer_display()

st.write("")

# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------

with st.sidebar:

    st.markdown("## 🎒 INVENTORY")

    if st.session_state.inventory:
        for item in st.session_state.inventory:
            st.markdown(
                f"""
                <div class="inventory-card">
                    🔹 {item}
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.caption("획득한 아이템이 없습니다.")

    st.divider()

    st.markdown("## 🗺️ LOCATION")

    for key, room in ROOMS.items():
        if key == st.session_state.room:
            st.success(f"{room['icon']} {room['name']}")
        else:
            st.caption(f"{room['icon']} {room['name']}")

    st.divider()

    st.markdown("## 📓 NOTEBOOK")

    if st.session_state.notes:
        for note in st.session_state.notes:
            st.info(note)
    else:
        st.caption("아직 기록된 단서가 없습니다.")

    st.divider()

    st.markdown("## 📊 STATUS")
    st.metric("조사한 물건", len(st.session_state.examined))
    st.metric("아이템", len(st.session_state.inventory))
    st.metric("암호 시도", st.session_state.attempts)

    if st.button("게임 초기화", use_container_width=True):
        reset_game()
        st.rerun()


# ------------------------------------------------------------
# ROOM INFORMATION
# ------------------------------------------------------------

room_id = st.session_state.room
room = ROOMS[room_id]

st.markdown(
    f"""
    <div class="room-banner">
        <div class="room-number">{room['number']}</div>
        <div class="room-name">{room['icon']} {room['name']}</div>
        <div class="room-description">{room['description']}</div>
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# TOP-DOWN MAP
# ------------------------------------------------------------

st.subheader("🕹️ 2D ROOM EXPLORATION")
st.caption("방 안의 물건을 선택하면 조사할 수 있습니다.")

object_positions = {
    obj["position"]: object_id
    for object_id, obj in room["objects"].items()
}

for row in range(5):
    cols = st.columns(5)

    for col in range(5):
        with cols[col]:

            position = (row, col)

            if position in object_positions:

                object_id = object_positions[position]
                obj = room["objects"][object_id]

                unique = f"{room_id}_{object_id}"
                examined = unique in st.session_state.examined

                icon = obj["icon"]

                if object_id == "door":
                    if room_id == "ward" and has_item("기록 보관실 열쇠"):
                        icon = "🚪"
                    elif room_id == "records" and "records_drawer" in st.session_state.unlocked:
                        icon = "🚪"
                    else:
                        icon = "🔒"

                if object_id == "elevator":
                    icon = "🛗" if "control_switch" in st.session_state.unlocked else "🔒"

                if object_id == "exit":
                    icon = "🚪"

                label = f"{icon}\n{obj['name']}"

                if examined:
                    label = f"✓ {label}"

                if st.button(
                    label,
                    key=f"map_{room_id}_{object_id}",
                    use_container_width=True
                ):
                    examine_object(object_id)
                    st.rerun()

            else:
                if row == 0 or row == 4 or col == 0 or col == 4:
                    st.markdown(
                        "<div class='map-tile map-wall'>🧱</div>",
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        "<div class='map-tile map-floor'>·</div>",
                        unsafe_allow_html=True
                    )

st.caption("🧱 벽  ·  · 바닥  ·  ✓ 조사 완료")

# ------------------------------------------------------------
# OBJECT INTERACTION
# ------------------------------------------------------------

selected = st.session_state.selected

if selected and selected in room["objects"]:

    obj = room["objects"][selected]

    st.divider()

    st.markdown("## 🔍 물체 조사")

    st.markdown(
        f"""
        <div class="object-card">
            <div style="font-size:35px;">{obj['icon']}</div>
            <h3>{obj['name']}</h3>
            <p>{obj['description']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------- WARD ----------------

    if room_id == "ward":

        if selected in ["bed", "calendar", "desk", "plaque"]:
            st.markdown("### 📜 발견한 단서")
            st.info(obj["clue"])

            if obj["item"]:
                if st.button("단서 기록하기", key=f"note_{selected}"):
                    add_note(obj["clue"])
                    add_item(obj["item"])
                    st.success("단서를 기록했습니다.")

        elif selected == "cabinet":

            st.markdown("### 🔐 숫자 잠금장치")

            if "ward_cabinet" in st.session_state.unlocked:
                st.success("이미 열려 있습니다.")

            else:
                st.write("달력과 메모에서 네 자리 숫자를 찾아보세요.")

                code = st.text_input(
                    "암호 4자리",
                    max_chars=4,
                    key="ward_code"
                )

                if st.button("잠금 해제", key="ward_unlock", type="primary"):
                    if len(code) == 4 and code.isdigit():
                        check_password("ward_cabinet", code)
                    else:
                        st.error("숫자 4자리를 입력하세요.")

        elif selected == "door":

            if has_item("기록 보관실 열쇠"):

                if st.button("🔑 열쇠 사용하기", type="primary"):
                    st.session_state.room = "records"
                    st.session_state.selected = None
                    st.rerun()

            else:
                st.error("문이 잠겨 있습니다. 열쇠가 필요합니다.")


    # ---------------- RECORDS ----------------

    elif room_id == "records":

        if selected in ["shelf", "chart", "note", "plaque"]:
            st.markdown("### 📜 발견한 단서")
            st.info(obj["clue"])

            if obj["item"]:
                if st.button("단서 기록하기", key=f"note_{selected}"):
                    add_note(obj["clue"])
                    add_item(obj["item"])
                    st.success("단서를 기록했습니다.")

        elif selected == "drawer":

            if "records_drawer" in st.session_state.unlocked:
                st.success("서랍이 열려 있습니다. 퓨즈를 획득했습니다.")

            else:
                st.write("색깔 분류표와 환자 기록 메모를 비교하세요.")

                code = st.text_input(
                    "암호 4자리",
                    max_chars=4,
                    key="records_code"
                )

                if st.button("서랍 열기", key="records_unlock", type="primary"):
                    if len(code) == 4 and code.isdigit():
                        check_password("records_drawer", code)
                    else:
                        st.error("숫자 4자리를 입력하세요.")

        elif selected == "door":

            if "records_drawer" in st.session_state.unlocked:
                if st.button("통제실로 이동하기", type="primary"):
                    st.session_state.room = "control"
                    st.session_state.selected = None
                    st.rerun()
            else:
                st.error("먼저 잠금 서랍을 열어야 합니다.")


    # ---------------- CONTROL ROOM ----------------

    elif room_id == "control":

        if selected in ["generator", "memo", "plaque"]:

            st.markdown("### 📜 장치 조사")
            st.info(obj["clue"])

            if selected == "memo":
                if st.button("메모 기록하기"):
                    add_note(obj["clue"])
                    add_item("제어 메모")
                    st.success("메모를 획득했습니다.")

        elif selected == "switch":

            if "control_switch" in st.session_state.unlocked:
                st.success("전력 복구 완료!")

            elif not has_item("비상 퓨즈"):
                st.error("퓨즈가 없습니다. 기록 보관실을 다시 확인하세요.")

            else:
                st.write("제어 메모를 바탕으로 네 자리 순서를 입력하세요.")

                code = st.text_input(
                    "제어 암호",
                    max_chars=4,
                    key="control_code"
                )

                if st.button("전력 복구", key="control_unlock", type="primary"):
                    if len(code) == 4 and code.isdigit():
                        check_password("control_switch", code)
                    else:
                        st.error("숫자 4자리를 입력하세요.")

        elif selected == "elevator":

            if "control_switch" in st.session_state.unlocked:

                if st.button("⬇ 지하로 이동", type="primary"):
                    st.session_state.room = "basement"
                    st.session_state.selected = None
                    st.rerun()

            else:
                st.error("전력이 공급되지 않아 엘리베이터가 작동하지 않습니다.")


    # ---------------- BASEMENT ----------------

    elif room_id == "basement":

        if selected in ["pipe", "light", "plaque"]:

            st.markdown("### 📜 마지막 단서")
            st.info(obj["clue"])

            if obj["item"]:
                if st.button("마지막 단서 기록하기", key=f"note_{selected}"):
                    add_note(obj["clue"])
                    add_item(obj["item"])
                    st.success("단서를 기록했습니다.")

        elif selected == "exit":

            if "final_exit" in st.session_state.unlocked:
                st.success("출구가 열렸습니다.")

            else:
                st.markdown("### 🚨 최종 탈출 암호")

                st.write(
                    "네 구역의 문패 숫자를 처음부터 방문한 순서대로 입력하세요."
                )

                code = st.text_input(
                    "최종 암호 4자리",
                    max_chars=4,
                    key="final_code"
                )

                if st.button("🚪 최종 출구 열기", type="primary"):
                    if len(code) == 4 and code.isdigit():
                        check_password("final_exit", code)
                        st.rerun()
                    else:
                        st.error("숫자 4자리를 입력하세요.")


# ------------------------------------------------------------
# HINT SYSTEM
# ------------------------------------------------------------

st.divider()

with st.expander("💡 힌트 시스템 / 사용 시 기록됩니다"):

    st.write("힌트를 사용하면 최종 등급에 반영됩니다.")

    hints = {
        "ward": [
            "침대 아래 메모와 벽의 달력을 함께 확인하세요.",
            "달력에 표시된 네 날짜를 순서대로 읽어 보세요."
        ],
        "records": [
            "환자 기록 선반의 색깔 순서를 먼저 확인하세요.",
            "파랑, 노랑, 빨강, 초록의 숫자를 차례로 연결하세요."
        ],
        "control": [
            "비상 퓨즈를 먼저 확보해야 합니다.",
            "제어 메모에 적힌 3번째, 1번째, 4번째, 2번째 순서를 확인하세요."
        ],
        "basement": [
            "각 구역에 문패가 있습니다.",
            "병동부터 지하까지 문패 숫자를 순서대로 나열하세요."
        ]
    }

    if st.button("현재 구역 힌트 보기"):
        use_hint()

        current_hints = hints[room_id]

        level = min(
            st.session_state.hints_used - 1,
            len(current_hints) - 1
        )

        st.warning(current_hints[level])

        st.caption(
            f"사용한 힌트: {st.session_state.hints_used}회"
        )


# ------------------------------------------------------------
# EVENT LOG
# ------------------------------------------------------------

with st.expander("📋 최근 조사 기록"):

    if st.session_state.events:
        for event in st.session_state.events[-10:][::-1]:
            st.write("• " + event)
    else:
        st.caption("아직 조사 기록이 없습니다.")


# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------

st.divider()

st.markdown("""
<div style="text-align:center;padding:12px;">
    <div style="
        font-family:monospace;
        letter-spacing:3px;
        color:#72cbb8;
    ">
        ABANDONED HOSPITAL
    </div>
    <p style="color:#647985;font-size:11px;">
        2D ESCAPE GAME · VERSION 1.0
    </p>
    <p style="color:#647985;font-size:11px;">
        FICTIONAL GAME ENVIRONMENT
    </p>
</div>
""", unsafe_allow_html=True)
