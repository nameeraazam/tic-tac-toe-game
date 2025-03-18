
import streamlit as st

# Custom CSS to style the buttons
st.markdown("""
    <style>
    .stButton>button {
        height: 100px !important;
        width: 100px !important;
        font-size: 24px !important;
        border-radius: 10px !important;
        margin: 5px !important;
    }
    .stButton>button:disabled {
        opacity: 1 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize the board state in session state if it doesn't exist
if 'board' not in st.session_state:
    st.session_state.board = ["" for _ in range(9)]
    st.session_state.current_player = "X"
    st.session_state.winner = None
    st.session_state.game_over = False

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

# App title
st.title("Tic-Tac-Toe")

# Display game status
if st.session_state.winner:
    st.header(st.session_state.winner)
else:
    st.header(f"Player {st.session_state.current_player}'s turn")

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

# Reset button
if st.button("Reset Game", type="primary"):
    reset_game()
