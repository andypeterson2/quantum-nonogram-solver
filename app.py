# Import Flask and render_template
from flask import Flask, render_template
from helpers import *
# Create an instance of Flask
app = Flask(__name__)

# Define a route for the home page
@app.route("/")
def home():
    # Return the index.html file as a response
    return render_template("index.html")

@app.route("/nono")
def nono():
    return render_template("index2.html")

@app.route("/nonogram")
def nonograms():
    # Generate a random puzzle
    puzzle = generate_puzzle(ROWS, COLS)

    # Get the grid and clues from the puzzle object
    grid = puzzle["grid"]
    row_clues = puzzle["row_clues"]
    col_clues = puzzle["col_clues"]

    # Render the template with the grid and clues as arguments
    return render_template("nonogram.html", grid=grid, row_clues=row_clues, col_clues=col_clues)

# Run the app
if __name__ == "__main__":
    app.run(debug=True, port="5001")