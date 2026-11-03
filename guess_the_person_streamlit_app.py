import streamlit as st
import random
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Guess the Person - Party Charades",
    page_icon="🎭",
    layout="centered",
    initial_sidebar_state="expanded"
)

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
    if "game_stage" not in st.session_state:
        st.session_state.game_stage = "home"  # 'home', 'setup', 'search_room', 'turn_shield', 'turn_active', 'round_summary', 'game_over'
    if "game_mode" not in st.session_state:
        st.session_state.game_mode = "pass_play"  # 'pass_play', 'create_room', 'search_room'
    if "room_code" not in st.session_state:
        st.session_state.room_code = ""
    if "players" not in st.session_state:
        st.session_state.players = ["Player 1", "Player 2", "Player 3"]
    if "scores" not in st.session_state:
        st.session_state.scores = {p: 0 for p in st.session_state.players}
    if "total_rounds" not in st.session_state:
        st.session_state.total_rounds = 3  # integer or 'Unlimited'
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
def build_deck():
    cards = []
    for cat in st.session_state.selected_categories:
        if cat in MASTER_DECKS:
            for c in MASTER_DECKS[cat]:
                cards.append({**c, "category": cat})
    for custom in st.session_state.custom_cards:
        cards.append({"name": custom["name"], "hint": custom.get("hint", "Custom Card"), "category": "Custom Deck ✨"})
    random.shuffle(cards)
    if not cards:
        cards = [{**c, "category": "Sports Legends ⚽"} for c in MASTER_DECKS["Sports Legends ⚽"]]
        random.shuffle(cards)
    return cards

def draw_next_card():
    if not st.session_state.deck:
        st.session_state.deck = build_deck()
    return st.session_state.deck.pop()

def start_match():
    st.session_state.scores = {p: 0 for p in st.session_state.players}
    st.session_state.current_round = 1
    st.session_state.current_player_idx = 0
    st.session_state.deck = build_deck()
    st.session_state.current_card = draw_next_card()
    st.session_state.round_history = []
    st.session_state.game_stage = "turn_shield"

def record_turn_result(success: bool):
    actor = st.session_state.players[st.session_state.current_player_idx]
    card = st.session_state.current_card
    
    if success:
        actor_pts = st.session_state.scoring["actor_correct"]
        guesser_pts = st.session_state.scoring["guesser_correct"]
    else:
        actor_pts = -abs(st.session_state.scoring["actor_fail"])
        guesser_pts = -abs(st.session_state.scoring["guesser_fail"])
        
    for p in st.session_state.players:
        if p == actor:
            st.session_state.scores[p] += actor_pts
        else:
            st.session_state.scores[p] += guesser_pts

    st.session_state.round_history.append({
        "round": st.session_state.current_round,
        "actor": actor,
        "person": card["name"],
        "category": card["category"],
        "success": success,
        "actor_delta": actor_pts,
        "guesser_delta": guesser_pts
    })

    # Advance player turn
    st.session_state.current_player_idx += 1
    if st.session_state.current_player_idx >= len(st.session_state.players):
        st.session_state.game_stage = "round_summary"
    else:
        st.session_state.current_card = draw_next_card()
        st.session_state.game_stage = "turn_shield"

def proceed_to_next_round():
    is_last = (st.session_state.total_rounds != "Unlimited" and 
               st.session_state.current_round >= int(st.session_state.total_rounds))
    if is_last:
        st.session_state.game_stage = "game_over"
    else:
        st.session_state.current_round += 1
        st.session_state.current_player_idx = 0
        st.session_state.current_card = draw_next_card()
        st.session_state.game_stage = "turn_shield"

# --- Sidebar Controls ---
with st.sidebar:
    st.title("🎭 Game Controls")
    
    # Active marks summary
    st.info(
        f"**Marks Scheme:**\n"
        f"- Actor Correct: **+{st.session_state.scoring['actor_correct']}**\n"
        f"- Guessers Correct: **+{st.session_state.scoring['guesser_correct']}**\n"
        f"- Actor Failed: **-{st.session_state.scoring['actor_fail']}**\n"
        f"- Guessers Failed: **-{st.session_state.scoring['guesser_fail']}**"
    )

    if st.session_state.game_stage not in ["home", "setup", "search_room"]:
        st.subheader("📊 Live Scores")
        sorted_scores = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
        for rank, (player, score) in enumerate(sorted_scores, 1):
            curr_actor = st.session_state.players[st.session_state.current_player_idx] if st.session_state.game_stage in ["turn_shield", "turn_active"] else None
            badge = " 🎭 (Acting)" if player == curr_actor else ""
            score_color = "green" if score >= 0 else "red"
            st.markdown(f"**#{rank} {player}{badge}**: :{score_color}[{score} pts]")

        st.divider()
        if st.button("🚪 Exit to Main Menu", use_container_width=True):
            st.session_state.game_stage = "home"
            st.rerun()

# ==========================================
# 1. SCREEN: HOME
# ==========================================
if st.session_state.game_stage == "home":
    st.markdown("<h1 style='text-align: center;'>🎭 Guess the Person</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Act. Guess. Score Big with Friends!</p>", unsafe_allow_html=True)
    st.write("---")

    col1, col2, col3 = st.columns(1)[0], None, None
    
    # Option 1: Pass & Play
    with st.container(border=True):
        st.subheader("📱 Pass & Play")
        st.write("Play locally on a single device passed around the room with privacy shield protection.")
        if st.button("Play Pass & Play", type="primary", use_container_width=True):
            st.session_state.game_mode = "pass_play"
            st.session_state.game_stage = "setup"
            st.rerun()

    # Option 2: Create Room
    with st.container(border=True):
        st.subheader("📡 Create Room")
        st.write("Generate a unique 5-letter Room Code, configure rules, and host friends.")
        if st.button("Host New Room", use_container_width=True):
            st.session_state.game_mode = "create_room"
            chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
            st.session_state.room_code = "".join(random.choices(chars, k=5))
            st.session_state.game_stage = "setup"
            st.rerun()

    # Option 3: Search / Join Room
    with st.container(border=True):
        st.subheader("🔍 Search / Join Room")
        st.write("Got a room code from a friend? Enter your nickname and join immediately.")
        if st.button("Join Room", use_container_width=True):
            st.session_state.game_stage = "search_room"
            st.rerun()

# ==========================================
# 2. SCREEN: SEARCH ROOM
# ==========================================
elif st.session_state.game_stage == "search_room":
    st.subheader("🔍 Join a Room")
    with st.container(border=True):
        player_name = st.text_input("Your Nickname", value="Alex", max_chars=15)
        entered_code = st.text_input("5-Letter Room Code", max_chars=5, placeholder="e.g. ACT88").strip().upper()
        
        st.caption("Settings such as decks, timers, and scoring are governed by the host.")
        
        col_back, col_join = st.columns(2)
        with col_back:
            if st.button("⬅️ Back to Menu", use_container_width=True):
                st.session_state.game_stage = "home"
                st.rerun()
        with col_join:
            if st.button("Connect & Play", type="primary", use_container_width=True):
                if not player_name:
                    st.error("Please enter your nickname.")
                elif len(entered_code) < 4:
                    st.error("Please enter a valid room code.")
                else:
                    st.session_state.players = ["Host", f"{player_name} (You)", "Player 3"]
                    st.session_state.game_mode = "search_room"
                    start_match()
                    st.rerun()

# ==========================================
# 3. SCREEN: SETUP
# ==========================================
elif st.session_state.game_stage == "setup":
    is_room = st.session_state.game_mode == "create_room"
    
    if is_room:
        st.subheader(f"📡 Hosting Room: `{st.session_state.room_code}`")
        st.caption("Share this code with your group so they can join!")
    else:
        st.subheader("📱 Pass & Play Setup")
        st.caption("Configure turns, custom marks, and categories.")

    with st.container(border=True):
        st.markdown("### 🧮 Custom Marks Scheme")
        preset_cols = st.columns(3)
        with preset_cols[0]:
            if st.button("Standard (+10/+5, -3/-3)", use_container_width=True):
                st.session_state.scoring = {"actor_correct": 10, "guesser_correct": 5, "actor_fail": 3, "guesser_fail": 3}
                st.rerun()
        with preset_cols[1]:
            if st.button("High Stakes (+5/+3, -3/-5)", use_container_width=True):
                st.session_state.scoring = {"actor_correct": 5, "guesser_correct": 3, "actor_fail": 3, "guesser_fail": 5}
                st.rerun()
        with preset_cols[2]:
            if st.button("No Penalty (0 on fail)", use_container_width=True):
                st.session_state.scoring = {"actor_correct": 10, "guesser_correct": 5, "actor_fail": 0, "guesser_fail": 0}
                st.rerun()

        sc_col1, sc_col2 = st.columns(2)
        with sc_col1:
            st.session_state.scoring["actor_correct"] = st.number_input(
                "Actor Correct (+pts)", min_value=0, max_value=50, value=st.session_state.scoring["actor_correct"]
            )
            st.session_state.scoring["actor_fail"] = st.number_input(
                "Actor Failed (-pts penalty)", min_value=0, max_value=50, value=st.session_state.scoring["actor_fail"]
            )
        with sc_col2:
            st.session_state.scoring["guesser_correct"] = st.number_input(
                "Guessers Correct (+pts)", min_value=0, max_value=50, value=st.session_state.scoring["guesser_correct"]
            )
            st.session_state.scoring["guesser_fail"] = st.number_input(
                "Guessers Failed (-pts penalty)", min_value=0, max_value=50, value=st.session_state.scoring["guesser_fail"]
            )

    with st.container(border=True):
        st.markdown("### 🔄 Number of Rounds")
        round_options = [1, 3, 5, 10, 15, 20, "Unlimited"]
        selected_r = st.radio("Choose total match rounds:", round_options, index=1, horizontal=True)
        st.session_state.total_rounds = selected_r

    with st.container(border=True):
        st.markdown("### 👥 Player Roster")
        st.caption("Each round consists of 1 turn per player as the actor.")
        
        # Display existing players
        for i, p in enumerate(st.session_state.players):
            c_name, c_del = st.columns([4, 1])
            with c_name:
                st.write(f"**{i+1}.** {p}")
            with c_del:
                if len(st.session_state.players) > 2:
                    if st.button("❌", key=f"del_p_{i}"):
                        st.session_state.players.pop(i)
                        st.rerun()

        new_p = st.text_input("Add new player name", max_chars=20)
        if st.button("➕ Add Player") and new_p.strip():
            if new_p.strip() not in st.session_state.players:
                st.session_state.players.append(new_p.strip())
                st.rerun()

    with st.container(border=True):
        st.markdown("### 🎴 Categories & Custom Personalities")
        selected_cats = st.multiselect(
            "Select Character Decks",
            options=list(MASTER_DECKS.keys()),
            default=list(MASTER_DECKS.keys())
        )
        st.session_state.selected_categories = selected_cats

        custom_p = st.text_input("Add Custom Person / Friend / Inside Joke", max_chars=30)
        if st.button("➕ Add Custom Personality") and custom_p.strip():
            st.session_state.custom_cards.append({"name": custom_p.strip(), "hint": "Custom party addition"})
            st.success(f"Added '{custom_p.strip()}' to custom deck!")

        if st.session_state.custom_cards:
            st.caption(f"Custom Cards ({len(st.session_state.custom_cards)}): " + ", ".join(c["name"] for c in st.session_state.custom_cards))

    col_btn_back, col_btn_start = st.columns(2)
    with col_btn_back:
        if st.button("⬅️ Back to Menu", use_container_width=True):
            st.session_state.game_stage = "home"
            st.rerun()
    with col_btn_start:
        if st.button("🚀 Start Match", type="primary", use_container_width=True):
            if len(st.session_state.players) < 2:
                st.error("Please add at least 2 players to play!")
            else:
                start_match()
                st.rerun()

# ==========================================
# 4. SCREEN: TURN - PRIVACY SHIELD
# ==========================================
elif st.session_state.game_stage == "turn_shield":
    current_actor = st.session_state.players[st.session_state.current_player_idx]
    round_disp = f"Round {st.session_state.current_round}" if st.session_state.total_rounds == "Unlimited" else f"Round {st.session_state.current_round} of {st.session_state.total_rounds}"
    
    st.markdown(f"<h3 style='text-align: center;'>{round_disp}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: gray;'>Turn {st.session_state.current_player_idx + 1} of {len(st.session_state.players)}</p>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("<h2 style='text-align: center;'>🙈 Privacy Shield</h2>", unsafe_allow_html=True)
        st.markdown(
            f"<h3 style='text-align: center; color: #EC4899;'>Pass device to: {current_actor}</h3>",
            unsafe_allow_html=True
        )
        st.write("Other players must look away so they don't see the secret personality card.")
        
        st.info("Rule: Gestures and actions only! No talking or spelling letters.")

        if st.button("👁️ Reveal Card & Start Acting", type="primary", use_container_width=True):
            st.session_state.game_stage = "turn_active"
            st.rerun()

# ==========================================
# 5. SCREEN: TURN - ACTIVE ACTING
# ==========================================
elif st.session_state.game_stage == "turn_active":
    current_actor = st.session_state.players[st.session_state.current_player_idx]
    card = st.session_state.current_card
    
    st.markdown(f"**Acting Now:** 🎭 **{current_actor}**")
    
    with st.container(border=True):
        st.caption(f"Category: {card['category']}")
        st.markdown(f"<h1 style='text-align: center; color: #38BDF8;'>{card['name']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: gray;'><em>Clue: {card['hint']}</em></p>", unsafe_allow_html=True)

    col_fail, col_success = st.columns(2)
    with col_fail:
        fail_label = f"❌ Failed / Pass (-{st.session_state.scoring['actor_fail']}/-{st.session_state.scoring['guesser_fail']})"
        if st.button(fail_label, use_container_width=True):
            record_turn_result(success=False)
            st.rerun()

    with col_success:
        succ_label = f"✅ Got It! (+{st.session_state.scoring['actor_correct']}/+{st.session_state.scoring['guesser_correct']})"
        if st.button(succ_label, type="primary", use_container_width=True):
            record_turn_result(success=True)
            st.rerun()

# ==========================================
# 6. SCREEN: ROUND SUMMARY
# ==========================================
elif st.session_state.game_stage == "round_summary":
    st.balloons()
    st.markdown(f"<h2 style='text-align: center;'>🎉 Round {st.session_state.current_round} Complete!</h2>", unsafe_allow_html=True)

    # Standings table
    with st.container(border=True):
        st.markdown("### 🏆 Leaderboard")
        sorted_scores = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
        for rank, (player, score) in enumerate(sorted_scores, 1):
            trophy = "🥇" if rank == 1 else ("🥈" if rank == 2 else ("🥉" if rank == 3 else f"#{rank}"))
            color = "green" if score >= 0 else "red"
            st.markdown(f"{trophy} **{player}** — :{color}[**{score} pts**]")

    # Turn history for this round
    with st.expander("📜 View Round Recap", expanded=True):
        current_recap = [h for h in st.session_state.round_history if h["round"] == st.session_state.current_round]
        for item in current_recap:
            res_icon = "✅" if item["success"] else "❌"
            st.write(
                f"{res_icon} **{item['actor']}** acted *\"{item['person']}\"* ({item['category']}) → "
                f"Actor: `{'+' if item['actor_delta'] > 0 else ''}{item['actor_delta']}`, Guessers: `{'+' if item['guesser_delta'] > 0 else ''}{item['guesser_delta']}`"
            )

    is_final = (st.session_state.total_rounds != "Unlimited" and 
                st.session_state.current_round >= int(st.session_state.total_rounds))

    col_next, col_finish = st.columns(2)
    with col_next:
        next_label = "🏆 View Final Winners" if is_final else f"Start Round {st.session_state.current_round + 1} ➡️"
        if st.button(next_label, type="primary", use_container_width=True):
            proceed_to_next_round()
            st.rerun()

    with col_finish:
        if not is_final:
            if st.button("🏁 End Match Now", use_container_width=True):
                st.session_state.game_stage = "game_over"
                st.rerun()

# ==========================================
# 7. SCREEN: GAME OVER
# ==========================================
elif st.session_state.game_stage == "game_over":
    st.balloons()
    sorted_scores = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
    winner_name, winner_score = sorted_scores[0]

    st.markdown("<h1 style='text-align: center;'>👑 Match Over!</h1>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(f"<h2 style='text-align: center; color: #F59E0B;'>🏆 Winner: {winner_name}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-size: 22px; font-weight: bold;'>Score: {winner_score} Points</p>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("### Final Standings")
        for rank, (player, score) in enumerate(sorted_scores, 1):
            medals = {1: "🥇 1st Place", 2: "🥈 2nd Place", 3: "🥉 3rd Place"}
            label = medals.get(rank, f"#{rank}")
            st.write(f"**{label}**: {player} — `{score} pts`")

    col_again, col_home = st.columns(2)
    with col_again:
        if st.button("🔄 Play Again", type="primary", use_container_width=True):
            start_match()
            st.rerun()
    with col_home:
        if st.button("🏠 Main Menu", use_container_width=True):
            st.session_state.game_stage = "home"
            st.rerun()