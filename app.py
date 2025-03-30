from flask import Flask, render_template, request
from yahtzee import Turn, YahtzeeScorer, GameState

app = Flask(__name__)
game_state = GameState()  # Create a GameState object

@app.route("/", methods=["GET", "POST"])
def yahtzee():
    global game_state  # Access the global game_state object

    dice_images = [
        "dice-0.png",
        "dice-0.png",
        "dice-0.png",
        "dice-0.png",
        "dice-0.png"
    ]

    game_over = False  # Initialize game_over
    grand_total = 0  # Initialize grand_total

    if request.method == "POST":
        action = request.form.get("action")  # Get the form action

        if action == "roll":
            hold = request.form.getlist("hold")  # Get the list of held dice indices
            print(f"Held dice: {hold}")  # Print the held dice for debugging

            # Convert held indices to a list of booleans
            hold_list = [False] * 5
            for die_index in map(int, hold):
                hold_list[die_index] = True

            # Roll the dice
            dice_values = game_state.turn.roll_dice(hold_list)

            # Update dice images based on rolled values
            if dice_values is not None:
                dice_images = [f"dice-{value}.png" for value in dice_values]
                game_state.current_roll = dice_values  # Store dice values
                game_state.held_dice = [int(i) for i in hold]  # Store held indices

            if game_state.turn.rolls == 3:
                # Do not reset turn here
                pass

        elif action == "score":
            # Get the selected category from the form
            category = request.form.get("category")

            # Calculate score for the selected category
            if category:
                score = YahtzeeScorer.calculate_score(
                    game_state.current_roll, category
                )  # Use current_roll
                game_state.update_score(category, score)

            game_state.resetTurn()
            #game_state.turn = Turn()  # Reset turn after scoring
            #game_state.held_dice = []  # Reset held dice
        elif action == "new_game":

            #abandon_game = request.form.get("abandon_game")
            #if abandon_game == "true" or game_state.is_game_over():
                game_state = GameState()  # Create a new GameState object
        elif action == "forceNew": 
            game_state = GameState()  # Create a new GameState object

        game_over = game_state.is_game_over()  # Check if game is over
        if game_over:
            grand_total = game_state.calculate_grand_total()  # Calculate grand total


    else:
        # Initial roll
        dice_values = game_state.turn.roll_dice()
        # Update dice images based on rolled values
        if dice_values is not None:
            dice_images = [f"dice-{value}.png" for value in dice_values]
            game_state.current_roll = dice_values  # Store initial roll

    # Calculate available categories
    available_categories = YahtzeeScorer.get_available_categories(
        game_state.current_roll, game_state.scores
    )

    # Calculate potential scores
    potential_scores = {}
    for category in available_categories:
        potential_scores[category] = YahtzeeScorer.calculate_score(
            game_state.current_roll, category
        )

    return render_template(
        "yahtzee.html",
        dice_images=dice_images,
        scores=game_state.scores,
        turn=game_state.turn,
        bonus=game_state.calculate_upper_section_bonus(),
        game_over=game_over,
        grand_total=grand_total,
        available_categories=available_categories,
        potential_scores=potential_scores,  # Pass potential scores
        game_state=game_state,
    )

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')