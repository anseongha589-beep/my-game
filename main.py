
import streamlit as st
import random
from datetime import datetime

# ==========================================
# CASE FILE : 미제사건 연구소
# ==========================================

st.set_page_config(
    page_title="CASE FILE | 미제사건 연구소",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- 디자인 ----------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

.stApp {
    background: #0b1020;
    color: #e6eaf2;
}

[data-testid="stSidebar"] {
    background: #10182a;
    border-right: 1px solid #26344c;
}

[data-testid="stSidebar"] * {
    color: #dce5f4;
}

h1, h2, h3 {
    color: #edf3ff !important;
    font-weight: 800 !important;
}

p, label, li {
    color: #c4cede;
}

div[data-testid="stMetric"] {
    background: #141f34;
    border: 1px solid #2a3a54;
    padding: 18px;
    border-radius: 12px;
}

div[data-testid="stMetricValue"] {
    color: #67d5e8;
}

div.stButton > button {
    background: #172943;
    color: #e9f2ff;
    border: 1px solid #36516f;
    border-radius: 9px;
    min-height: 43px;
    font-weight: 700;
    transition: 0.2s;
}

div.stButton > button:hover {
    background: #244366;
    border-color: #67d5e8;
    color: white;
}

div.stButton > button[kind="primary"] {
    background: #087e91;
    border: 1px solid #16b8c7;
    color: white;
}

.case-banner {
    background: linear-gradient(110deg, #14243b, #182e49, #102132);
    border: 1px solid #31506e;
    padding: 27px;
    border-radius: 15px;
    margin-bottom: 22px;
}

.case-number {
    font-family: 'DM Mono', monospace;
    color: #67d5e8;
    font-size: 13px;
    letter-spacing: 3px;
}

.case-title {
    color: #ffffff;
    font-size: 31px;
    font-weight: 900;
    margin-top: 8px;
}

.case-desc {
    color: #bdcce0;
    line-height: 1.8;
    margin-top: 10px;
}

.panel {
    background: #141f32;
    border: 1px solid #2a3b53;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 13px;
}

.evidence {
    background: #182b40;
    border-left: 4px solid #67d5e8;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 12px;
}

.suspect {
    background: #172238;
    border: 1px solid #354762;
    padding: 18px;
    border-radius: 12px;
    min-height: 170px;
}

.tag {
    color: #67d5e8;
    font-size: 12px;
    font-family: 'DM Mono', monospace;
    letter-spacing: 1px;
}

.muted {
    color: #8495ad;
    font-size: 13px;
}

hr {
    border-color: #293b55;
}

.stProgress > div > div > div > div {
    background: #20b9ca;
}

div[data-testid="stAlert"] {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# ---------- 사건 데이터 ----------

EVIDENCE = {
    "ev1": {
        "name": "진열대 점검 기록",
        "place": "전시실",
        "type": "현장 증거",
        "description": """
전시실의 점검 기록을 확인했다.

다이아몬드가 마지막으로 정상 확인된 시각은
오후 7시 40분이다.

그 이후의 전시품 상태 확인 기록에는
평소와 다른 내용이 적혀 있다.
""",
        "importance": "사건 발생 시간대를 좁히는 데 도움이 된다."
    },
    "ev2": {
        "name": "출입 기록 사본",
        "place": "관리실",
        "type": "기록 증거",
        "description": """
박물관 내부 출입 기록을 조사했다.

한유진 큐레이터의 출입 기록은
오후 8시 12분으로 확인된다.

그러나 한유진은 자신의 진술에서
오후 7시 30분에 퇴근했다고 말했다.
""",
        "importance": "용의자의 진술과 객관적인 기록이 일치하는지 확인할 수 있다."
    },
    "ev3": {
        "name": "목격자 메모",
        "place": "안내데스크",
        "type": "목격 증거",
        "description": """
안내 직원이 작성한 메모를 발견했다.

오후 8시 무렵 전시실 근처에서
파란색 서류철을 들고 있는 사람을 보았다고 한다.

얼굴은 정확히 확인하지 못했다.
""",
        "importance": "사건 당시 현장 주변에 있었던 사람을 조사할 필요가 있다."
    },
    "ev4": {
        "name": "수정된 전시품 목록",
        "place": "자료실",
        "type": "문서 증거",
        "description": """
전시품 관리 목록의 수정 내역을 발견했다.

사건 당일 오후 8시 5분,
다이아몬드의 관리 상태가 수정되었다.

수정 담당자란에는 한유진의 이름이 남아 있다.
""",
        "importance": "사건 당일 문서 수정에 관여한 사람을 확인할 수 있다."
    },
    "ev5": {
        "name": "당일 업무 인수인계서",
        "place": "관리실",
        "type": "문서 증거",
        "description": """
당일 업무 인수인계서를 발견했다.

한유진은 오후 7시에 업무를 마쳤다고 기록했지만,
오후 8시 5분에 수정된 전시품 목록에는
본인의 이름이 남아 있다.

두 기록 사이에 시간적 모순이 존재한다.
""",
        "importance": "한유진의 퇴근 시각에 대한 추가 확인이 필요하다."
    }
}

LOCATIONS = {
    "전시실": {
        "icon": "💎",
        "description": "다이아몬드가 사라진 사건 현장이다.",
        "evidence": ["ev1"]
    },
    "관리실": {
        "icon": "🗄️",
        "description": "박물관의 출입 기록과 업무 문서가 보관된 곳이다.",
        "evidence": ["ev2", "ev5"]
    },
    "안내데스크": {
        "icon": "📝",
        "description": "당일 안내 직원의 기록과 목격자 메모를 확인할 수 있다.",
        "evidence": ["ev3"]
    },
    "자료실": {
        "icon": "📂",
        "description": "전시품 목록과 과거 관리 자료가 보관된 곳이다.",
        "evidence": ["ev4"]
    }
}

SUSPECTS = {
    "한유진": {
        "job": "박물관 큐레이터",
        "age": 32,
        "icon": "👩‍💼",
        "description": "전시품 관리와 전시 기획을 담당한다.",
        "motive": "전시품 관리 업무에 직접 관여했다.",
        "statement": "저는 오후 7시 30분에 퇴근했습니다. 이후에는 박물관에 없었습니다.",
        "questions": {
            "사건 당일 어디에 있었습니까?":
                "오후 7시 30분에 퇴근했습니다. 그 이후에는 개인적인 약속이 있었습니다.",
            "전시품 목록을 수정했습니까?":
                "당일 목록을 확인한 것은 맞지만, 마지막 수정 시각은 기억나지 않습니다.",
            "전시실에 다시 들어간 적이 있습니까?":
                "퇴근한 뒤에는 전시실에 들어간 적이 없습니다."
        }
    },
    "박도윤": {
        "job": "야간 경비원",
        "age": 45,
        "icon": "🧑‍✈️",
        "description": "박물관 야간 순찰과 시설 관리를 담당한다.",
        "motive": "사건 당시 건물 내부에 있었다.",
        "statement": "저는 평소처럼 야간 순찰 업무를 하고 있었습니다.",
        "questions": {
            "사건 당일 어디에 있었습니까?":
                "저녁 8시에는 동쪽 전시 구역을 확인하고 있었습니다.",
            "전시실에서 이상한 점을 발견했습니까?":
                "당시에는 특별히 이상한 점을 발견하지 못했습니다.",
            "다른 용의자를 본 적이 있습니까?":
                "정확히 누구인지는 모르지만 직원 한 명이 서류를 들고 이동하는 것을 봤습니다."
        }
    },
    "최서연": {
        "job": "환경 관리 직원",
        "age": 29,
        "icon": "👩‍🔧",
        "description": "박물관 내부 청소와 시설 환경 관리를 담당한다.",
        "motive": "사건 시간에 전시실 주변을 지나갔다.",
        "statement": "저는 정해진 업무 구역에서 청소를 하고 있었습니다.",
        "questions": {
            "사건 당일 어디에 있었습니까?":
                "오후 8시 무렵에는 안내데스크 근처를 지나고 있었습니다.",
            "전시실에 들어갔습니까?":
                "청소 업무 때문에 전시실 근처에는 갔지만 오래 머물지는 않았습니다.",
            "이상한 사람을 봤습니까?":
                "파란색 서류철을 들고 있는 사람을 본 것 같습니다."
        }
    },
    "이민재": {
        "job": "문화 전문 기자",
        "age": 35,
        "icon": "🧑‍💻",
        "description": "박물관 특별 전시를 취재하기 위해 방문했다.",
        "motive": "사건 당일 박물관을 방문한 외부인이다.",
        "statement": "저는 취재를 마치고 안내데스크 주변에 있었습니다.",
        "questions": {
            "사건 당일 어디에 있었습니까?":
                "저녁 8시에는 안내데스크 근처에서 취재 자료를 정리하고 있었습니다.",
            "전시실에 들어갔습니까?":
                "공식 관람 시간에 전시실을 방문했지만 사건 시간에는 들어가지 않았습니다.",
            "파란색 서류철을 본 적 있습니까?":
                "박물관 직원들이 서류철을 가지고 다니는 모습은 봤습니다."
        }
    }
}


# ---------- 세션 초기화 ----------

def init_game():
    defaults = {
        "page": "사건 브리핑",
        "collected": [],
        "visited": [],
        "questioned": [],
        "solved": False,
        "accused": None,
        "submitted": False,
        "report": "",
        "score": 0,
        "used_hints": 0
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_game()


def reset_game():
    for key in [
        "page", "collected", "visited", "questioned",
        "solved", "accused", "submitted", "report",
        "score", "used_hints"
    ]:
        if key in st.session_state:
            del st.session_state[key]
    init_game()


def page_title(title, subtitle):
    st.markdown(f"""
    <div style="margin-bottom:22px;">
        <div class="tag">CASE FILE / INVESTIGATION SYSTEM</div>
        <h1 style="margin-bottom:3px;">{title}</h1>
        <div class="muted">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


def add_evidence(evidence_id):
    if evidence_id not in st.session_state.collected:
        st.session_state.collected.append(evidence_id)


# ---------- 사이드바 ----------

with st.sidebar:
    st.markdown("""
    <div style="padding:12px 0 20px 0;">
        <div style="font-family:monospace;color:#67d5e8;letter-spacing:3px;">
            INVESTIGATION SYSTEM
        </div>
        <div style="font-size:26px;font-weight:900;color:white;">
            🔎 CASE FILE
        </div>
        <div class="muted">미제사건 연구소</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("#### 📁 CURRENT CASE")
    st.markdown("**CF-2026-001**")
    st.caption("사라진 다이아몬드")

    progress = len(st.session_state.collected) / len(EVIDENCE)

    st.progress(progress)
    st.caption(f"증거 수집 {len(st.session_state.collected)} / {len(EVIDENCE)}")

    st.divider()

    pages = [
        "사건 브리핑",
        "현장 조사",
        "증거 보관함",
        "용의자 목록",
        "용의자 심문",
        "최종 추리",
        "수사 결과"
    ]

    selected_page = st.radio(
        "수사 메뉴",
        pages,
        index=pages.index(st.session_state.page)
        if st.session_state.page in pages else 0
    )

    st.session_state.page = selected_page

    st.divider()

    st.markdown("#### 📊 INVESTIGATION STATUS")
    st.metric("확보한 증거", f"{len(st.session_state.collected)}개")
    st.metric("조사한 장소", f"{len(st.session_state.visited)}개")
    st.metric("심문한 용의자", f"{len(st.session_state.questioned)}명")

    st.caption("CASE FILE v1.0")


# ---------- 상단 상태 표시 ----------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("사건 번호", "CF-001")

with col2:
    st.metric("수집 증거", f"{len(st.session_state.collected)} / 5")

with col3:
    st.metric("조사 장소", f"{len(st.session_state.visited)} / 4")

with col4:
    st.metric("심문 완료", f"{len(st.session_state.questioned)} / 4")

st.divider()


# ==========================================
# PAGE 1. 사건 브리핑
# ==========================================

if st.session_state.page == "사건 브리핑":

    page_title("사건 브리핑", "MISSION BRIEFING / 사건 개요")

    st.markdown("""
    <div class="case-banner">
        <div class="case-number">CASE NO. CF-2026-001</div>
        <div class="case-title">💎 사라진 다이아몬드</div>
        <div class="case-desc">
            평화로운 박물관의 특별 전시실에서 전시 중이던
            다이아몬드가 사라졌다.<br>
            사건이 발생한 시간에는 박물관 직원과 외부 방문객 등
            여러 사람이 건물 안에 있었다.<br><br>
            당신은 사건을 맡은 담당 수사관이다.
            모든 증거와 진술을 분석해 진실을 밝혀내야 한다.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📋 사건 정보")

    a, b = st.columns(2)

    with a:
        st.markdown("""
        <div class="panel">
            <div class="tag">LOCATION</div>
            <h3>국립 문화 박물관</h3>
            <p>특별 전시실</p>
        </div>
        """, unsafe_allow_html=True)

    with b:
        st.markdown("""
        <div class="panel">
            <div class="tag">INCIDENT TIME</div>
            <h3>오후 7:40 ~ 8:20</h3>
            <p>사건 추정 발생 시간</p>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("🚨 수사 목표")

    goals = [
        "사건 현장의 증거를 수집한다.",
        "용의자 4명의 진술을 확보한다.",
        "증거와 진술의 모순을 발견한다.",
        "범인을 지목하고 논리적인 근거를 제출한다."
    ]

    for i, goal in enumerate(goals, 1):
        st.markdown(f"**{i}.** {goal}")

    st.info("주의: 모든 용의자가 의심스러워 보일 수 있습니다. 추측보다는 증거를 우선하십시오.")

    if st.button("🔎 수사 시작하기", type="primary", use_container_width=True):
        st.session_state.page = "현장 조사"
        st.rerun()


# ==========================================
# PAGE 2. 현장 조사
# ==========================================

elif st.session_state.page == "현장 조사":

    page_title("현장 조사", "SCENE INVESTIGATION / 사건 현장")

    st.markdown("조사할 장소를 선택하세요. 각 장소에서 새로운 증거를 발견할 수 있습니다.")

    cols = st.columns(2)

    for i, (name, info) in enumerate(LOCATIONS.items()):
        with cols[i % 2]:
            with st.container(border=True):
                st.markdown(f"### {info['icon']} {name}")
                st.write(info["description"])

                if name in st.session_state.visited:
                    st.success("조사 완료")
                else:
                    st.caption("아직 조사하지 않은 장소")

                if st.button(
                    f"{name} 조사하기",
                    key=f"location_{name}",
                    use_container_width=True
                ):
                    st.session_state.visited.append(name)

                    for evidence_id in info["evidence"]:
                        add_evidence(evidence_id)

                    st.rerun()

    if st.session_state.visited:
        st.divider()
        st.subheader("📌 조사 기록")

        for place in st.session_state.visited:
            st.write(f"✓ {place} 조사 완료")

    if len(st.session_state.collected) == len(EVIDENCE):
        st.success("모든 증거를 수집했습니다! 이제 증거 보관함에서 분석하세요.")


# ==========================================
# PAGE 3. 증거 보관함
# ==========================================

elif st.session_state.page == "증거 보관함":

    page_title("증거 보관함", "EVIDENCE ARCHIVE / 확보 자료")

    st.write(f"현재까지 확보한 증거: {len(st.session_state.collected)}개")

    if not st.session_state.collected:
        st.warning("아직 확보한 증거가 없습니다. 현장 조사를 먼저 진행하세요.")

    for evidence_id in st.session_state.collected:
        ev = EVIDENCE[evidence_id]

        with st.container(border=True):
            st.markdown(f"### 📄 {ev['name']}")
            st.markdown(
                f"<span class='tag'>{ev['type']} · {ev['place']}</span>",
                unsafe_allow_html=True
            )
            st.markdown(ev["description"])
            st.info(f"수사 메모: {ev['importance']}")

    st.divider()

    st.subheader("🧠 증거 분석 메모")

    note = st.text_area(
        "직접 추리 내용을 작성해 보세요.",
        placeholder="예: 한유진의 퇴근 시각과 출입 기록이 서로 일치하지 않는다.",
        height=130,
        key="investigation_note"
    )

    st.caption("메모는 현재 세션에서만 유지됩니다.")


# ==========================================
# PAGE 4. 용의자 목록
# ==========================================

elif st.session_state.page == "용의자 목록":

    page_title("용의자 목록", "SUSPECT DATABASE / 인물 정보")

    st.write("사건과 관련된 인물 4명입니다. 모든 인물의 진술을 비교해 보세요.")

    names = list(SUSPECTS.keys())

    for start in range(0, len(names), 2):
        cols = st.columns(2)

        for i, name in enumerate(names[start:start + 2]):
            data = SUSPECTS[name]

            with cols[i]:
                with st.container(border=True):
                    st.markdown(
                        f"<div class='suspect'>"
                        f"<div class='tag'>SUSPECT PROFILE</div>"
                        f"<h2>{data['icon']} {name}</h2>"
                        f"<p><b>직업:</b> {data['job']}</p>"
                        f"<p><b>나이:</b> {data['age']}세</p>"
                        f"<p>{data['description']}</p>"
                        f"</div>",
                        unsafe_allow_html=True
                    )

                    st.markdown("**기본 진술**")
                    st.info(data["statement"])

                    if name in st.session_state.questioned:
                        st.success("심문 완료")
                    else:
                        st.caption("아직 심문하지 않았습니다.")


# ==========================================
# PAGE 5. 용의자 심문
# ==========================================

elif st.session_state.page == "용의자 심문":

    page_title("용의자 심문", "INTERROGATION ROOM / 진술 확보")

    suspect_name = st.selectbox(
        "심문할 용의자를 선택하세요.",
        list(SUSPECTS.keys())
    )

    suspect = SUSPECTS[suspect_name]

    with st.container(border=True):
        st.markdown(f"## {suspect['icon']} {suspect_name}")
        st.write(f"**직업:** {suspect['job']}")
        st.write(suspect["description"])
        st.info(f"첫 진술: {suspect['statement']}")

    st.subheader("💬 질문 선택")

    question = st.selectbox(
        "질문할 내용을 선택하세요.",
        list(suspect["questions"].keys()),
        key=f"question_{suspect_name}"
    )

    if st.button("질문하기", type="primary", use_container_width=True):
        st.session_state[f"answer_{suspect_name}"] = suspect["questions"][question]
        st.session_state.questioned.append(suspect_name) \
            if suspect_name not in st.session_state.questioned else None

    answer = st.session_state.get(f"answer_{suspect_name}")

    if answer:
        st.markdown("### 🗣️ 용의자의 답변")
        st.markdown(
            f"""
            <div class="panel">
                <div class="tag">SUSPECT STATEMENT</div>
                <h3>{suspect_name}</h3>
                <p>{answer}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    st.subheader("📌 심문 진행 상황")

    for name in SUSPECTS:
        status = "완료" if name in st.session_state.questioned else "미완료"
        st.write(f"{'🟢' if status == '완료' else '⚪'} {name} : {status}")


# ==========================================
# PAGE 6. 최종 추리
# ==========================================

elif st.session_state.page == "최종 추리":

    page_title("최종 추리", "FINAL DEDUCTION / 범인 지목")

    st.warning(
        "최종 지목을 제출하면 결과가 확정됩니다. "
        "제출하기 전에 증거와 진술을 충분히 확인하세요."
    )

    st.subheader("1. 범인 선택")

    accused = st.radio(
        "당신이 생각하는 범인은 누구입니까?",
        list(SUSPECTS.keys()),
        format_func=lambda x: f"{SUSPECTS[x]['icon']} {x}",
        key="final_accused"
    )

    st.divider()

    st.subheader("2. 핵심 증거 선택")

    st.write("범인을 지목하는 데 사용한 증거를 선택하세요.")

    selected_evidence = []

    for evidence_id in st.session_state.collected:
        ev = EVIDENCE[evidence_id]

        if st.checkbox(
            f"{ev['name']} ({ev['place']})",
            key=f"final_{evidence_id}"
        ):
            selected_evidence.append(evidence_id)

    st.divider()

    st.subheader("3. 최종 수사 보고서")

    report = st.text_area(
        "왜 이 사람이 범인이라고 생각합니까?",
        placeholder="수집한 증거와 용의자의 진술을 근거로 논리적으로 작성하세요.",
        height=180,
        key="final_report"
    )

    st.caption("근거가 구체적일수록 높은 점수를 받을 수 있습니다.")

    if st.button(
        "🚨 최종 지목 제출",
        type="primary",
        use_container_width=True
    ):
        if len(st.session_state.collected) == 0:
            st.error("먼저 현장을 조사하고 증거를 수집하세요.")

        elif not selected_evidence:
            st.error("최소 하나의 증거를 선택하세요.")

        elif len(report.strip()) < 10:
            st.error("수사 보고서를 10자 이상 작성하세요.")

        else:
            correct = accused == "한유진"

            key_evidence = {"ev2", "ev4", "ev5"}
            used_key = len(key_evidence.intersection(selected_evidence))

            score = 0

            if correct:
                score += 50

            score += min(used_key * 15, 45)

            if len(report.strip()) >= 50:
                score += 5

            score = min(score, 100)

            st.session_state.accused = accused
            st.session_state.submitted = True
            st.session_state.solved = correct
            st.session_state.score = score
            st.session_state.report = report
            st.session_state.selected_evidence = selected_evidence
            st.session_state.page = "수사 결과"

            st.rerun()


# ==========================================
# PAGE 7. 수사 결과
# ==========================================

elif st.session_state.page == "수사 결과":

    page_title("수사 결과", "CASE RESULT / 사건 종결 보고서")

    if not st.session_state.submitted:
        st.warning("아직 최종 추리를 제출하지 않았습니다.")
        st.stop()

    if st.session_state.solved:
        st.success("CASE SOLVED — 사건 해결!")
        st.markdown("""
        <div class="case-banner">
            <div class="case-number">INVESTIGATION SUCCESSFUL</div>
            <div class="case-title">🎉 사건 해결</div>
            <div class="case-desc">
                당신의 추리는 정답이었습니다.<br>
                수집한 증거를 통해 사건의 핵심 모순을 밝혀냈습니다.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("CASE FAILED — 범인을 잘못 지목했습니다.")
        st.markdown("""
        <div class="case-banner">
            <div class="case-number">INVESTIGATION FAILED</div>
            <div class="case-title">🔍 사건 미해결</div>
            <div class="case-desc">
                범인 지목이 정확하지 않았습니다.<br>
                사건의 진실과 증거를 다시 확인해 보세요.
            </div>
        </div>
        """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("최종 점수", f"{st.session_state.score}점")

    with c2:
        st.metric("수집 증거", f"{len(st.session_state.collected)}개")

    with c3:
        st.metric("심문 인물", f"{len(st.session_state.questioned)}명")

    st.divider()

    st.subheader("📋 수사 결과 보고서")

    st.write(f"**당신의 지목:** {st.session_state.accused}")
    st.write(f"**실제 범인:** 한유진")
    st.write(f"**수사 판정:** {'성공' if st.session_state.solved else '실패'}")

    st.markdown("**제출한 수사 보고서**")
    st.markdown(
        f"""
        <div class="panel">
            {st.session_state.report}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("🔎 핵심 증거 해설")

    st.markdown("""
    **첫 번째: 출입 기록 사본**

    한유진은 오후 7시 30분에 퇴근했다고 진술했지만,
    출입 기록에는 오후 8시 12분의 기록이 남아 있었다.

    **두 번째: 수정된 전시품 목록**

    오후 8시 5분에 수정된 문서의 담당자는 한유진이었다.

    **세 번째: 업무 인수인계서**

    업무를 마쳤다는 기록과 실제 문서 수정 기록 사이에
    시간적 모순이 존재한다.

    이 기록들을 종합하면 한유진의 진술은 신뢰하기 어렵다.
    """)

    st.divider()

    if st.button("🔄 새로운 수사 시작", type="primary", use_container_width=True):
        reset_game()
        st.rerun()


# ---------- 하단 ----------

st.divider()

st.markdown("""
<div style="text-align:center;padding:15px;">
    <div class="tag">CASE FILE INVESTIGATION SYSTEM</div>
    <p class="muted">FICTIONAL MYSTERY PROJECT · VERSION 1.0</p>
    <p class="muted">모든 사건과 인물은 창작된 허구입니다.</p>
</div>
""", unsafe_allow_html=True)
