import streamlit as st
import random
import time
from streamlit_autorefresh import st_autorefresh

# --- Page Configuration ---
st.set_page_config(
    page_title="Guess the Person - Party Charades",
    page_icon="🎭",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Thread-Safe Global Multi-Room Store for Realtime Cross-Device Sync ---
@st.cache_resource
def get_global_rooms():
    # Persistent dict across all connected browsers & users
    return {}

GLOBAL_ROOMS = get_global_rooms()

# --- Master Decks Data ---
MASTER_DECKS = {
    "Sports Legends ⚽": [
        {"name": "Lionel Messi", "hint": "8-time Ballon d’Or winner, Argentine football GOAT"},
        {"name": "Cristiano Ronaldo", "hint": "Portuguese striker, famous 'SIUUU' celebration"},
        {"name": "Virat Kohli", "hint": "Indian cricket maestro, master of chases & king of aggression"},
        {"name": "MS Dhoni", "hint": "Captain Cool, iconic helicopter shot & lightning stumpings"},
        {"name": "Sachin Tendulkar", "hint": "God of Cricket, 100 international centuries"},
        {"name": "Rohit Sharma", "hint": "The Hitman, record 3 ODI double-hundreds"},
        {"name": "LeBron James", "hint": "King James, 4-time NBA Champion, all-time scoring leader"},
        {"name": "Michael Jordan", "hint": "Chicago Bulls #23, Jumpman logo, basketball icon"},
        {"name": "Roger Federer", "hint": "Swiss maestro, elegant 1-handed backhand, 20 Grand Slams"},
        {"name": "Rafael Nadal", "hint": "King of Clay, intense fist pumps, 14 French Opens"},
        {"name": "Usain Bolt", "hint": "Fastest man alive, famous lightning bolt victory pose"},
        {"name": "Muhammad Ali", "hint": "'Float like a butterfly, sting like a bee'"}
    ],
    "Cinema & Characters 🎬": [
        {"name": "Shah Rukh Khan", "hint": "King of Romance, iconic open-arms pose"},
        {"name": "Amitabh Bachchan", "hint": "The Big B, legendary deep voice, angry young man"},
        {"name": "Iron Man / Tony Stark", "hint": "Billionaire superhero, snap: 'I am Iron Man'"},
        {"name": "Spider-Man / Peter Parker", "hint": "Shoots webs from wrists, 'With great power...'"},
        {"name": "Captain Jack Sparrow", "hint": "Staggering pirate captain, 'Where is the rum?!'"},
        {"name": "The Joker", "hint": "'Why so serious?', maniacal laugh, Batman villain"},
        {"name": "Wednesday Addams", "hint": "Deadpan stare, viral gothic rave dance"},
        {"name": "Barbie", "hint": "Perfect smile, 'Hi Barbie!', walks on permanent tiptoes"},
        {"name": "Charlie Chaplin", "hint": "Little Tramp, bowler hat, twirling cane, silent comedy"},
        {"name": "Deadpool", "hint": "Breaks 4th wall, dual katanas, witty mercenary"}
    ],
    "Leaders & Innovators 👑": [
        {"name": "Albert Einstein", "hint": "Sticky-out tongue photo, wild hair, E=mc²"},
        {"name": "APJ Abdul Kalam", "hint": "Missile Man of India, visionary scientist and President"},
        {"name": "Mahatma Gandhi", "hint": "Round spectacles, walking stick, leader of Ahimsa"},
        {"name": "Steve Jobs", "hint": "Black turtleneck, unveiled the original iPhone"},
        {"name": "Elon Musk", "hint": "Launches rockets to Mars, loves memes and Cybertrucks"},
        {"name": "Isaac Newton", "hint": "Apple fell on head, universal law of gravitation"},
        {"name": "Julius Caesar", "hint": "Roman laurel wreath, 'Et tu, Brute?'"}
    ],
    "Pop & Internet Icons 🌟": [
        {"name": "Michael Jackson", "hint": "King of Pop, Moonwalk, fedora hat, 'Hee-hee!'"},
        {"name": "Taylor Swift", "hint": "Eras Tour sensation, heartbreaks with acoustic guitar"},
        {"name": "Freddie Mercury", "hint": "Live Aid 'Ay-Oh!', mic stand in clenched fist"},
        {"name": "MrBeast", "hint": "YouTube creator giving away millions in cash and challenges"},
        {"name": "Gordon Ramsay", "hint": "'It\\'s raw!', slam two slices of bread: idiot sandwich"},
        {"name": "Khaby Lame", "hint": "Silent reaction shrug with outstretched palms"}
    ]
}

# --- State Initialization ---
def init_state():
    if "user_id" not in st.session_state:
        st.session_state.user_id = "user_" + str(int(time.time() * 1000)) + "_" + str(random.randint(100, 999))
    if "game_stage" not in st.session_state:
        st.session_state.game_stage = "home"
    if "game_mode" not in st.session_state:
        st.session_state.game_mode = "pass_play"  # 'pass_play' or 'online_room'
    if "room_code" not in st.session_state:
        st.session_state.room_code = ""
    if "player_name" not in st.session_state:
        st.session_state.player_name = "Player"
    if "local_players" not in st.session_state:
        st.session_state.local_players = ["Player 1", "Player 2", "Player 3"]
    if "local_scores" not in st.session_state:
        st.session_state.local_scores = {p: 0 for p in st.session_state.local_players}
    if "total_rounds" not in st.session_state:
        st.session_state.total_rounds = 3
    if "current_round" not in st.session_state:
        st.session_state.current_round = 1
    if "current_player_idx" not in st.session_state:
        st.session_state.current_player_idx = 0
    if "selected_categories" not in st.session_state:
        st.session_state.selected_categories = list(MASTER_DECKS.keys())
    if "custom_cards" not in st.session_state:
        st.session_state.custom_cards = []
    if "deck" not in st.session_state:
        st.session_state.deck = []
    if "current_card" not in st.session_state:
        st.session_state.current_card = None
    if "round_history" not in st.session_state:
        st.session_state.round_history = []
    if "scoring" not in st.session_state:
        st.session_state.scoring = {
            "actor_correct": 10,
            "guesser_correct": 5,
            "actor_fail": 3,
            "guesser_fail": 3
        }

init_state()

# --- Helper Functions ---
def build_deck(selected_cats, custom_cards):
    cards = []
    for cat in selected_cats:
        if cat in MASTER_DECKS:
            for c in MASTER_DECKS[cat]:
                cards.append({**c, "category": cat})
    for custom in custom_cards:
        cards.append({"name": custom["name"], "hint": custom.get("hint", "Custom Card"), "category": "Custom Deck ✨"})
    random.shuffle(cards)
    if not cards:
        cards = [{**c, "category": "Sports Legends ⚽"} for c in MASTER_DECKS["Sports Legends ⚽"]]
        random.shuffle(cards)
    return cards

def create_shared_room(code, host_id, host_name, rounds, scoring, categories, custom_cards):
    GLOBAL_ROOMS[code] = {
        "host_id": host_id,
        "state": "lobby",  # 'lobby', 'acting', 'round_summary', 'game_over'
        "rounds_total": rounds,
        "round_current": 1,
        "player_idx": 0,
        "scoring": scoring,
        "categories": categories,
        "custom_cards": custom_cards,
        "deck": build_deck(categories, custom_cards),
        "current_card": None,
        "players": [{"id": host_id, "name": host_name}],
        "scores": {host_id: 0},
        "history": [],
        "last_update": time.time()
    }

def draw_room_card(room):
    if not room["deck"]:
        room["deck"] = build_deck(room["categories"], room["custom_cards"])
    room["current_card"] = room["deck"].pop()

# --- Auto Sync Polling for Online Multiplayer ---
if st.session_state.game_mode == "online_room" and st.session_state.room_code in GLOBAL_ROOMS:
    # Refresh every 1.5 seconds to sync actions across different phones/computers
    st_autorefresh(interval=1500, key="multiplayer_sync")

# --- Sidebar Controls ---
with st.sidebar:
    st.title("🎭 Game Controls")
    
    if st.session_state.game_mode == "online_room" and st.session_state.room_code in GLOBAL_ROOMS:
        room = GLOBAL_ROOMS[st.session_state.room_code]
        st.success(f"📡 Connected to Room: **{st.session_state.room_code}**")
        st.info(
            f"**Marks Scheme:**\n"
            f"- Actor Correct: **+{room['scoring']['actor_correct']}**\n"
            f"- Guessers Correct: **+{room['scoring']['guesser_correct']}**\n"
            f"- Actor Failed: **-{room['scoring']['actor_fail']}**\n"
            f"- Guessers Failed: **-{room['scoring']['guesser_fail']}**"
        )
        st.subheader("📊 Live Room Scores")
        sorted_sc = sorted(room["players"], key=lambda p: room["scores"].get(p["id"], 0), reverse=True)
        actor_id = room["players"][room["player_idx"]]["id"] if room["players"] and room["state"] == "acting" else None
        
        for rank, p in enumerate(sorted_sc, 1):
            sc = room["scores"].get(p["id"], 0)
            is_actor = " 🎭 (Acting)" if p["id"] == actor_id else ""
            is_you = " ⭐ (You)" if p["id"] == st.session_state.user_id else ""
            color = "green" if sc >= 0 else "red"
            st.markdown(f"**#{rank} {p['name']}{is_you}{is_actor}**: :{color}[{sc} pts]")
    else:
        st.info(
            f"**Marks Scheme:**\n"
            f"- Actor Correct: **+{st.session_state.scoring['actor_correct']}**\n"
            f"- Guessers Correct: **+{st.session_state.scoring['guesser_correct']}**\n"
            f"- Actor Failed: **-{st.session_state.scoring['actor_fail']}**\n"
            f"- Guessers Failed: **-{st.session_state.scoring['guesser_fail']}**"
        )

    st.divider()
    if st.button("🚪 Exit to Main Menu", use_container_width=True):
        st.session_state.game_stage = "home"
        st.session_state.game_mode = "pass_play"
        st.session_state.room_code = ""
        st.rerun()

# ==========================================
# 1. SCREEN: HOME
# ==========================================
if st.session_state.game_stage == "home":
    st.markdown("<h1 style='text-align: center;'>🎭 Guess the Person</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Act. Guess. Score Big with Friends across devices!</p>", unsafe_allow_html=True)
    st.write("---")

    with st.container(border=True):
        st.subheader("📱 Pass & Play (Single Device)")
        st.write("Pass one phone around the room with a privacy shield.")
        if st.button("Start Pass & Play", type="primary", use_container_width=True):
            st.session_state.game_mode = "pass_play"
            st.session_state.game_stage = "setup"
            st.rerun()

    with st.container(border=True):
        st.subheader("📡 Create Online Room (Multi-Device)")
        st.write("Host a real-time room. Friends on other phones or laptops can join via room code!")
        if st.button("Host Online Room", use_container_width=True):
            st.session_state.game_mode = "online_room"
            chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
            st.session_state.room_code = "".join(random.choices(chars, k=5))
            st.session_state.game_stage = "setup"
            st.rerun()

    with st.container(border=True):
        st.subheader("🔍 Search / Join Room")
        st.write("Have a room code from a friend? Enter your nickname and join immediately.")
        if st.button("Join Room", use_container_width=True):
            st.session_state.game_mode = "online_room"
            st.session_state.game_stage = "search_room"
            st.rerun()

# ==========================================
# 2. SCREEN: SEARCH ROOM (JOIN ONLINE)
# ==========================================
elif st.session_state.game_stage == "search_room":
    st.subheader("🔍 Join an Online Room")
    with st.container(border=True):
        name_input = st.text_input("Your Player Nickname", value="Alex", max_chars=15)
        code_input = st.text_input("5-Letter Room Code", max_chars=5, placeholder="e.g. ACT88").strip().upper()
        
        col_back, col_join = st.columns(2)
        with col_back:
            if st.button("⬅️ Back to Menu", use_container_width=True):
                st.session_state.game_stage = "home"
                st.rerun()
        with col_join:
            if st.button("Connect & Join", type="primary", use_container_width=True):
                if not name_input.strip():
                    st.error("Please enter a nickname.")
                elif code_input not in GLOBAL_ROOMS:
                    st.error(f"Room '{code_input}' not found. Please double-check with the host!")
                else:
                    st.session_state.player_name = name_input.strip()
                    st.session_state.room_code = code_input
                    st.session_state.game_mode = "online_room"
                    
                    room = GLOBAL_ROOMS[code_input]
                    existing_p = [p for p in room["players"] if p["id"] == st.session_state.user_id]
                    if not existing_p:
                        room["players"].append({"id": st.session_state.user_id, "name": st.session_state.player_name})
                        room["scores"][st.session_state.user_id] = 0
                        room["last_update"] = time.time()
                    
                    st.session_state.game_stage = "online_lobby"
                    st.rerun()

# ==========================================
# 3. SCREEN: SETUP (PASS & PLAY OR HOST ROOM)
# ==========================================
elif st.session_state.game_stage == "setup":
    is_online = (st.session_state.game_mode == "online_room")
    
    if is_online:
        st.subheader(f"📡 Setting up Room: `{st.session_state.room_code}`")
        host_name = st.text_input("Your Host Nickname", value="Host", max_chars=15)
        st.session_state.player_name = host_name
    else:
        st.subheader("📱 Pass & Play Setup")

    with st.container(border=True):
        st.markdown("### 🧮 Custom Marks Scheme")
        p_cols = st.columns(3)
        with p_cols[0]:
            if st.button("Standard (+10/+5, -3/-3)", use_container_width=True):
                st.session_state.scoring = {"actor_correct": 10, "guesser_correct": 5, "actor_fail": 3, "guesser_fail": 3}
                st.rerun()
        with p_cols[1]:
            if st.button("High Stakes (+5/+3, -3/-5)", use_container_width=True):
                st.session_state.scoring = {"actor_correct": 5, "guesser_correct": 3, "actor_fail": 3, "guesser_fail": 5}
                st.rerun()
        with p_cols[2]:
            if st.button("No Penalty (0 on fail)", use_container_width=True):
                st.session_state.scoring = {"actor_correct": 10, "guesser_correct": 5, "actor_fail": 0, "guesser_fail": 0}
                st.rerun()

        sc1, sc2 = st.columns(2)
        with sc1:
            st.session_state.scoring["actor_correct"] = st.number_input("Actor Correct (+pts)", 0, 50, st.session_state.scoring["actor_correct"])
            st.session_state.scoring["actor_fail"] = st.number_input("Actor Failed (-pts)", 0, 50, st.session_state.scoring["actor_fail"])
        with sc2:
            st.session_state.scoring["guesser_correct"] = st.number_input("Guessers Correct (+pts)", 0, 50, st.session_state.scoring["guesser_correct"])
            st.session_state.scoring["guesser_fail"] = st.number_input("Guessers Failed (-pts)", 0, 50, st.session_state.scoring["guesser_fail"])

    with st.container(border=True):
        st.markdown("### 🔄 Number of Rounds")
        r_options = [1, 3, 5, 10, 15, 20, "Unlimited"]
        st.session_state.total_rounds = st.radio("Total rounds:", r_options, index=1, horizontal=True)

    with st.container(border=True):
        st.markdown("### 🎴 Categories")
        st.session_state.selected_categories = st.multiselect(
            "Select Decks",
            options=list(MASTER_DECKS.keys()),
            default=list(MASTER_DECKS.keys())
        )
        custom_p = st.text_input("Add Custom Personality / Inside Joke", max_chars=30)
        if st.button("➕ Add Custom") and custom_p.strip():
            st.session_state.custom_cards.append({"name": custom_p.strip(), "hint": "Custom party addition"})
            st.success(f"Added {custom_p.strip()}")

    if not is_online:
        with st.container(border=True):
            st.markdown("### 👥 Player Turn Order")
            for i, p in enumerate(st.session_state.local_players):
                c_name, c_del = st.columns([4, 1])
                with c_name:
                    st.write(f"**{i+1}.** {p}")
                with c_del:
                    if len(st.session_state.local_players) > 2 and st.button("❌", key=f"del_loc_{i}"):
                        st.session_state.local_players.pop(i)
                        st.rerun()
            new_p = st.text_input("Add Player", max_chars=20)
            if st.button("➕ Add Player") and new_p.strip() and new_p.strip() not in st.session_state.local_players:
                st.session_state.local_players.append(new_p.strip())
                st.rerun()

    c_back, c_start = st.columns(2)
    with c_back:
        if st.button("⬅️ Back", use_container_width=True):
            st.session_state.game_stage = "home"
            st.rerun()
    with c_start:
        start_txt = "Open Lobby & Wait for Players" if is_online else "🚀 Start Match"
        if st.button(start_txt, type="primary", use_container_width=True):
            if is_online:
                create_shared_room(
                    st.session_state.room_code,
                    st.session_state.user_id,
                    st.session_state.player_name,
                    st.session_state.total_rounds,
                    st.session_state.scoring,
                    st.session_state.selected_categories,
                    st.session_state.custom_cards
                )
                st.session_state.game_stage = "online_lobby"
                st.rerun()
            else:
                st.session_state.local_scores = {p: 0 for p in st.session_state.local_players}
                st.session_state.current_round = 1
                st.session_state.current_player_idx = 0
                st.session_state.deck = build_deck(st.session_state.selected_categories, st.session_state.custom_cards)
                st.session_state.current_card = st.session_state.deck.pop()
                st.session_state.round_history = []
                st.session_state.game_stage = "turn_shield"
                st.rerun()

# ==========================================
# 4. SCREEN: ONLINE LOBBY
# ==========================================
elif st.session_state.game_stage == "online_lobby":
    code = st.session_state.room_code
    if code not in GLOBAL_ROOMS:
        st.error("Room closed or expired.")
        st.session_state.game_stage = "home"
        st.rerun()

    room = GLOBAL_ROOMS[code]
    is_host = (room["host_id"] == st.session_state.user_id)

    # If match already started by host, automatically jump in!
    if room["state"] in ["acting", "round_summary", "game_over"]:
        st.session_state.game_stage = "online_gameplay"
        st.rerun()

    st.markdown(f"<h2 style='text-align:center;'>Room: <span style='color:#38BDF8; font-family:monospace;'>{code}</span></h2>", unsafe_allow_html=True)
    st.info("Share this 5-letter Room Code with your friends! They can open this app, tap **Search Room**, and join instantly from their phones.")

    with st.container(border=True):
        st.markdown(f"### 👥 Connected Players ({len(room['players'])})")
        for idx, p in enumerate(room["players"], 1):
            h_tag = " 👑 (Host)" if p["id"] == room["host_id"] else ""
            you_tag = " ⭐ (You)" if p["id"] == st.session_state.user_id else ""
            st.write(f"**{idx}.** {p['name']}{h_tag}{you_tag}")

    if is_host:
        if len(room["players"]) < 2:
            st.warning("Waiting for at least 1 more player to join before starting...")
        else:
            if st.button("🚀 Start Match for Everyone", type="primary", use_container_width=True):
                room["state"] = "acting"
                room["round_current"] = 1
                room["player_idx"] = 0
                draw_room_card(room)
                room["last_update"] = time.time()
                st.session_state.game_stage = "online_gameplay"
                st.rerun()
    else:
        st.info("⏳ Waiting for the Host to start the game...")

# ==========================================
# 5. SCREEN: ONLINE GAMEPLAY (REAL-TIME SYNCED)
# ==========================================
elif st.session_state.game_stage == "online_gameplay":
    code = st.session_state.room_code
    if code not in GLOBAL_ROOMS:
        st.error("Room closed.")
        st.session_state.game_stage = "home"
        st.rerun()

    room = GLOBAL_ROOMS[code]
    
    # State A: Acting Turn
    if room["state"] == "acting":
        actor = room["players"][room["player_idx"]]
        is_actor = (actor["id"] == st.session_state.user_id)
        card = room["current_card"]
        r_disp = f"Round {room['round_current']}" if room["rounds_total"] == "Unlimited" else f"Round {room['round_current']} of {room['rounds_total']}"

        st.markdown(f"<div style='text-align:center; font-weight:bold; color:#A78BFA;'>{r_disp} &bull; Turn {room['player_idx'] + 1} of {len(room['players'])}</div>", unsafe_allow_html=True)

        if is_actor:
            st.success("🎭 **IT'S YOUR TURN TO ACT!**")
            with st.container(border=True):
                st.caption(f"Category: {card['category']}")
                st.markdown(f"<h1 style='text-align: center; color: #38BDF8;'>{card['name']}</h1>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; color: gray;'><em>Clue: {card['hint']}</em></p>", unsafe_allow_html=True)
                st.caption("No speaking or mouthing words! Act it out silently.")

            col_fail, col_succ = st.columns(2)
            with col_fail:
                if st.button(f"❌ Failed (-{room['scoring']['actor_fail']}/-{room['scoring']['guesser_fail']})", use_container_width=True):
                    # Record fail
                    for p in room["players"]:
                        if p["id"] == actor["id"]:
                            room["scores"][p["id"]] -= abs(room["scoring"]["actor_fail"])
                        else:
                            room["scores"][p["id"]] -= abs(room["scoring"]["guesser_fail"])
                    room["history"].append({
                        "round": room["round_current"],
                        "actor": actor["name"],
                        "person": card["name"],
                        "success": False
                    })
                    room["player_idx"] += 1
                    if room["player_idx"] >= len(room["players"]):
                        room["state"] = "round_summary"
                    else:
                        draw_room_card(room)
                    room["last_update"] = time.time()
                    st.rerun()

            with col_succ:
                if st.button(f"✅ Got It! (+{room['scoring']['actor_correct']}/+{room['scoring']['guesser_correct']})", type="primary", use_container_width=True):
                    for p in room["players"]:
                        if p["id"] == actor["id"]:
                            room["scores"][p["id"]] += room["scoring"]["actor_correct"]
                        else:
                            room["scores"][p["id"]] += room["scoring"]["guesser_correct"]
                    room["history"].append({
                        "round": room["round_current"],
                        "actor": actor["name"],
                        "person": card["name"],
                        "success": True
                    })
                    room["player_idx"] += 1
                    if room["player_idx"] >= len(room["players"]):
                        room["state"] = "round_summary"
                    else:
                        draw_room_card(room)
                    room["last_update"] = time.time()
                    st.rerun()
        else:
            st.info(f"👀 **Guessing Mode:** Watch **{actor['name']}** act!")
            with st.container(border=True):
                st.markdown(f"<h3 style='text-align: center;'>Actor: <span style='color: #EC4899;'>{actor['name']}</span></h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; color: gray;'>Category: <strong>{card['category']}</strong></p>", unsafe_allow_html=True)
                st.write("Shout your guesses out loud to the actor! When someone gets it right, the actor will submit the score.")

    # State B: Round Summary
    elif room["state"] == "round_summary":
        st.balloons()
        st.markdown(f"<h2 style='text-align: center;'>🎉 Round {room['round_current']} Complete!</h2>", unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown("### 🏆 Leaderboard")
            sorted_p = sorted(room["players"], key=lambda p: room["scores"].get(p["id"], 0), reverse=True)
            for rank, p in enumerate(sorted_p, 1):
                trophy = "🥇" if rank == 1 else ("🥈" if rank == 2 else ("🥉" if rank == 3 else f"#{rank}"))
                sc = room["scores"].get(p["id"], 0)
                color = "green" if sc >= 0 else "red"
                st.markdown(f"{trophy} **{p['name']}** — :{color}[**{sc} pts**]")

        with st.expander("📜 Round History", expanded=True):
            curr_recap = [h for h in room["history"] if h["round"] == room["round_current"]]
            for h in curr_recap:
                st.write(f"{'✅' if h['success'] else '❌'} **{h['actor']}** acted *\"{h['person']}\"*")

        is_host = (room["host_id"] == st.session_state.user_id)
        is_final = (room["rounds_total"] != "Unlimited" and room["round_current"] >= int(room["rounds_total"]))

        if is_host:
            c1, c2 = st.columns(2)
            with c1:
                btn_lbl = "🏆 Crown Final Champions" if is_final else f"Start Round {room['round_current'] + 1} ➡️"
                if st.button(btn_lbl, type="primary", use_container_width=True):
                    if is_final:
                        room["state"] = "game_over"
                    else:
                        room["round_current"] += 1
                        room["player_idx"] = 0
                        room["state"] = "acting"
                        draw_room_card(room)
                    room["last_update"] = time.time()
                    st.rerun()
            with c2:
                if not is_final and st.button("🏁 End Match Now", use_container_width=True):
                    room["state"] = "game_over"
                    room["last_update"] = time.time()
                    st.rerun()
        else:
            st.info("⏳ Waiting for host to advance to the next round...")

    # State C: Final Game Over
    elif room["state"] == "game_over":
        st.balloons()
        sorted_p = sorted(room["players"], key=lambda p: room["scores"].get(p["id"], 0), reverse=True)
        winner = sorted_p[0]
        
        st.markdown("<h1 style='text-align: center;'>👑 Match Over!</h1>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(f"<h2 style='text-align: center; color: #F59E0B;'>🏆 Champion: {winner['name']}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; font-size: 22px; font-weight: bold;'>Score: {room['scores'].get(winner['id'], 0)} Points</p>", unsafe_allow_html=True)

        if room["host_id"] == st.session_state.user_id:
            if st.button("🔄 Play Again with Same Room", type="primary", use_container_width=True):
                room["round_current"] = 1
                room["player_idx"] = 0
                for p in room["players"]:
                    room["scores"][p["id"]] = 0
                room["history"] = []
                room["deck"] = build_deck(room["categories"], room["custom_cards"])
                draw_room_card(room)
                room["state"] = "acting"
                room["last_update"] = time.time()
                st.rerun()

# ==========================================
# 6. PASS & PLAY LOCAL GAMEPLAY
# ==========================================
elif st.session_state.game_stage == "turn_shield":
    actor = st.session_state.local_players[st.session_state.current_player_idx]
    round_disp = f"Round {st.session_state.current_round}" if st.session_state.total_rounds == "Unlimited" else f"Round {st.session_state.current_round} of {st.session_state.total_rounds}"
    
    st.markdown(f"<h3 style='text-align: center;'>{round_disp}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: gray;'>Turn {st.session_state.current_player_idx + 1} of {len(st.session_state.local_players)}</p>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("<h2 style='text-align: center;'>🙈 Privacy Shield</h2>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; color: #EC4899;'>Pass device to: {actor}</h3>", unsafe_allow_html=True)
        st.write("Other players look away!")
        if st.button("👁️ Reveal Card & Act", type="primary", use_container_width=True):
            st.session_state.game_stage = "turn_active"
            st.rerun()

elif st.session_state.game_stage == "turn_active":
    actor = st.session_state.local_players[st.session_state.current_player_idx]
    card = st.session_state.current_card
    
    st.markdown(f"**Acting Now:** 🎭 **{actor}**")
    with st.container(border=True):
        st.caption(f"Category: {card['category']}")
        st.markdown(f"<h1 style='text-align: center; color: #38BDF8;'>{card['name']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: gray;'><em>Clue: {card['hint']}</em></p>", unsafe_allow_html=True)

    col_fail, col_success = st.columns(2)
    with col_fail:
        if st.button(f"❌ Failed (-{st.session_state.scoring['actor_fail']}/-{st.session_state.scoring['guesser_fail']})", use_container_width=True):
            for p in st.session_state.local_players:
                if p == actor:
                    st.session_state.local_scores[p] -= abs(st.session_state.scoring["actor_fail"])
                else:
                    st.session_state.local_scores[p] -= abs(st.session_state.scoring["guesser_fail"])
            st.session_state.current_player_idx += 1
            if st.session_state.current_player_idx >= len(st.session_state.local_players):
                st.session_state.game_stage = "round_summary"
            else:
                st.session_state.current_card = st.session_state.deck.pop() if st.session_state.deck else build_deck(st.session_state.selected_categories, st.session_state.custom_cards).pop()
                st.session_state.game_stage = "turn_shield"
            st.rerun()

    with col_success:
        if st.button(f"✅ Got It! (+{st.session_state.scoring['actor_correct']}/+{st.session_state.scoring['guesser_correct']})", type="primary", use_container_width=True):
            for p in st.session_state.local_players:
                if p == actor:
                    st.session_state.local_scores[p] += st.session_state.scoring["actor_correct"]
                else:
                    st.session_state.local_scores[p] += st.session_state.scoring["guesser_correct"]
            st.session_state.current_player_idx += 1
            if st.session_state.current_player_idx >= len(st.session_state.local_players):
                st.session_state.game_stage = "round_summary"
            else:
                st.session_state.current_card = st.session_state.deck.pop() if st.session_state.deck else build_deck(st.session_state.selected_categories, st.session_state.custom_cards).pop()
                st.session_state.game_stage = "turn_shield"
            st.rerun()

elif st.session_state.game_stage == "round_summary":
    st.balloons()
    st.markdown(f"<h2 style='text-align: center;'>🎉 Round {st.session_state.current_round} Complete!</h2>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("### 🏆 Leaderboard")
        sorted_sc = sorted(st.session_state.local_scores.items(), key=lambda x: x[1], reverse=True)
        for rank, (player, score) in enumerate(sorted_sc, 1):
            trophy = "🥇" if rank == 1 else ("🥈" if rank == 2 else ("🥉" if rank == 3 else f"#{rank}"))
            color = "green" if score >= 0 else "red"
            st.markdown(f"{trophy} **{player}** — :{color}[**{score} pts**]")

    is_final = (st.session_state.total_rounds != "Unlimited" and st.session_state.current_round >= int(st.session_state.total_rounds))
    c1, c2 = st.columns(2)
    with c1:
        lbl = "🏆 View Final Winners" if is_final else f"Start Round {st.session_state.current_round + 1} ➡️"
        if st.button(lbl, type="primary", use_container_width=True):
            if is_final:
                st.session_state.game_stage = "game_over"
            else:
                st.session_state.current_round += 1
                st.session_state.current_player_idx = 0
                st.session_state.current_card = st.session_state.deck.pop() if st.session_state.deck else build_deck(st.session_state.selected_categories, st.session_state.custom_cards).pop()
                st.session_state.game_stage = "turn_shield"
            st.rerun()
    with c2:
        if not is_final and st.button("🏁 End Match Now", use_container_width=True):
            st.session_state.game_stage = "game_over"
            st.rerun()

elif st.session_state.game_stage == "game_over":
    st.balloons()
    sorted_sc = sorted(st.session_state.local_scores.items(), key=lambda x: x[1], reverse=True)
    w_name, w_score = sorted_sc[0]
    st.markdown("<h1 style='text-align: center;'>👑 Match Over!</h1>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(f"<h2 style='text-align: center; color: #F59E0B;'>🏆 Winner: {w_name}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-size: 22px; font-weight: bold;'>Score: {w_score} Points</p>", unsafe_allow_html=True)
    if st.button("🔄 Play Again", type="primary", use_container_width=True):
        st.session_state.local_scores = {p: 0 for p in st.session_state.local_players}
        st.session_state.current_round = 1
        st.session_state.current_player_idx = 0
        st.session_state.deck = build_deck(st.session_state.selected_categories, st.session_state.custom_cards)
        st.session_state.current_card = st.session_state.deck.pop()
        st.session_state.game_stage = "turn_shield"
        st.rerun()