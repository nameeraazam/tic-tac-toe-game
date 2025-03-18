
import streamlit as st

# Custom CSS for black background, animations, and styling
st.markdown("""
    <style>
    body {
        background-color: black !important;
        color: white !important;
    }
    .stButton>button {
        height: 100px !important;
        width: 100px !important;
        font-size: 24px !important;
        border-radius: 10px !important;
        margin: 5px !important;
        background-color: #333333 !important;
        color: white !important;
        border: 2px solid #555555 !important;
    }
    .stButton>button:disabled {
        opacity: 1 !important;
        color: white !important;
    }
    .stButton>button:hover {
        background-color: #444444 !important;
    }
    .title {
        font-size: 48px !important;
        font-weight: bold;
        text-align: center;
        animation: glow 2s infinite alternate;
    }
    .status {
        font-size: 32px !important;
        text-align: center;
        animation: slide 2s infinite alternate;
    }
    @keyframes glow {
        0% { color: #ffffff; }
        100% { color: #00ff00; }
    }
    @keyframes slide {
        0% { transform: translateX(-10px); }
        100% { transform: translateX(10px); }
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize the board state in session state if it doesn't exist
if 'board' not in st.session_state:
    st.session_state.board = ["" for _ in range(9)]
    st.session_state.current_player = "X"
    st.session_state.winner = None
    st.session_state.game_over = False
    st.session_state.game_started = False

# Check for winner
def check_winner(board):
    winning_combos = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    
    for combo in winning_combos:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != "":
            return board[combo[0]]
    
    if "" not in board:
        return "Tie"
    return None

# Handle button click
def handle_click(index):
    if st.session_state.board[index] == "" and not st.session_state.game_over:
        st.session_state.board[index] = st.session_state.current_player
        
        # Check for winner
        winner = check_winner(st.session_state.board)
        if winner:
            if winner == "Tie":
                st.session_state.winner = "It's a tie!"
            else:
                st.session_state.winner = f"Player {winner} wins!"
            st.session_state.game_over = True
        else:
            # Switch player
            st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"

# Reset game
def reset_game():
    st.session_state.board = ["" for _ in range(9)]
    st.session_state.current_player = "X"
    st.session_state.winner = None
    st.session_state.game_over = False
    st.session_state.game_started = False

# Start game
def start_game():
    st.session_state.game_started = True

# App title with animation
st.markdown('<div class="title">Tic-Tac-Toe</div>', unsafe_allow_html=True)

# Start Game button
if not st.session_state.game_started:
    if st.button("Start Game", type="primary"):
        start_game()

# Game logic
if st.session_state.game_started:
    # Display game status with animation
    if st.session_state.winner:
        st.markdown(f'<div class="status">{st.session_state.winner}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="status">Player {st.session_state.current_player}\'s turn</div>', unsafe_allow_html=True)

    # Create the 3x3 grid using columns
    for row in range(3):
        cols = st.columns(3)
        for col in range(3):
            index = row * 3 + col
            with cols[col]:
                button_label = st.session_state.board[index] if st.session_state.board[index] else " "
                button_disabled = st.session_state.board[index] != "" or st.session_state.game_over
                button_color = "blue" if st.session_state.board[index] == "X" else "red" if st.session_state.board[index] == "O" else "gray"
                
                st.button(
                    button_label, 
                    key=f"btn_{index}",
                    on_click=handle_click,
                    args=(index,),
                    disabled=button_disabled,
                    use_container_width=True,
                    help=f"Position {index}",
                    type="primary" if st.session_state.board[index] else "secondary"
                )

    # Reset and End Game buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Reset Game", type="primary"):
            reset_game()
    with col2:
        if st.button("End Game", type="secondary"):
            reset_game()
