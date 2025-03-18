import streamlit as st

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
            if st.session_state.board[index] == "X":
                button_color = "blue"
            elif st.session_state.board[index] == "O":
                button_color = "red"
            else:
                button_color = "gray"
                
            st.button(
                st.session_state.board[index] if st.session_state.board[index] else " ", 
                key=f"btn_{index}",
                on_click=handle_click,
                args=(index,),
                use_container_width=True,
                help=f"Position {index}",
                type="primary" if st.session_state.board[index] else "secondary"
            )

# Reset button
if st.button("Reset Game", type="primary"):
    reset_game()
