def is_legal_move(piece, start, end):
    # Define the row and column differences between the start and end positions.
    row_diff = abs(end[0] - start[0])
    col_diff = abs(end[1] - start[1])
    
    # Define the legal moves for each type of chess piece.
    if piece == 'king':
        # The king can move one step in any direction.
        return row_diff <= 1 and col_diff <= 1
    elif piece == 'queen':
        # The queen can move any number of steps in any direction.
        return row_diff == col_diff or start[0] == end[0] or start[1] == end[1]
    elif piece == 'rook':
        # The rook can move any number of steps horizontally or vertically.
        return start[0] == end[0] or start[1] == end[1]
    elif piece == 'bishop':
        # The bishop can move any number of steps diagonally.
        return row_diff == col_diff
    elif piece == 'knight':
        # The knight can move in an L-shape (2 steps in one direction and 1 step in a perpendicular direction).
        return (row_diff == 1 and col_diff == 2) or (row_diff == 2 and col_diff == 1)
    elif piece == 'pawn':
        # The pawn can move one step forward (assuming forward is in the positive row direction).
        # For simplicity, capturing and initial two-step moves are not considered.
        return row_diff == 1 and col_diff == 0
    else:
        # If an invalid piece type is provided, return False.
        return False

# Example usage
# piece_type = 'knight'
# start_position = (3, 3)  # Row 3, Column 3
# end_position = (5, 4)    # Row 5, Column 4
# print(is_legal_move(piece_type, start_position, end_position))

import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Define an endpoint to validate a chess move
@app.route('/validate_move', methods=['POST'])
def validate_move():
    # Get the move description from the client request
    move_description = request.json.get('move_description')

    # Use GPT-3 to extract move details from the natural language description
    prompt = f"Extract the piece, start position, and end position from the following chess move description: '{move_description}'\n\nPiece: "
    response = openai.Completion.create(engine="davinci", prompt=prompt, max_tokens=30)
    piece = response["choices"][0]["text"].strip()

    prompt += f"{piece}\nStart position: "
    response = openai.Completion.create(engine="davinci", prompt=prompt, max_tokens=10)
    start = response["choices"][0]["text"].strip()

    prompt += f"{start}\nEnd position: "
    response = openai.Completion.create(engine="davinci", prompt=prompt, max_tokens=10)
    end = response["choices"][0]["text"].strip()

    # Convert start and end positions to tuples
    start = tuple(map(int, start.split(',')))
    end = tuple(map(int, end.split(',')))

    # Check if the move is legal using the is_legal_move function
    legal = is_legal_move(piece, start, end)

    # Return the result to the client
    return jsonify({"legal": legal})

# Run the Flask app
if __name__ == '__main__':
    app.run()

# Don't forget to set your OpenAI API key as an environment variable
# export OPENAI_API_KEY=YOUR_API_KEY

