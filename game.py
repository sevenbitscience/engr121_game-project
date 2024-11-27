"""
A skill based reaction-time game for the CPX

Written by Joey Milausnic
09/05/2024
"""

from random import randrange
from time import sleep
from adafruit_circuitplayground import cp

# Color Settings
cp.pixels.brightness = 0.3
player_color = (0,50,50)
goal_color = (0,100,0)
background_color = (10,0,0)

# Game variables
game_timer = 0
score = 9
player_position = 0
player_direction = 1
goal_position = [7, 0, 4]
button_state = False
last_button_state = False

def average_colors(color_1, color_2):
    return (((color_1[0]+color_2[0])/2), ((color_1[1]+color_2[1])/2), ((color_1[2]+color_2[2])/2))

def show_game():
    for p in range(10):
        if p == player_position:
            #cp.pixels[p] = average_colors(player_color, cp.pixels[p])
            cp.pixels[p] = player_color
        elif p in goal_position:
            cp.pixels[p] = goal_color
        else:
            cp.pixels[p] = background_color

def update_number_of_goals():
    if score < 3:
        numberOfGoals = 3
    elif score < 7:
        numberOfGoals = 2
    else:
        numberOfGoals = 1
    while len(goal_position) > numberOfGoals:
        goal_position.pop(0)
    while len(goal_position) < numberOfGoals:
        goal_position.append(randrange(0,10))

    print(f"goal_position={goal_position}, score={score}")

def show_score(good):
    score_color = (0,100,0)
    if not good:
        score_color = (100,0,0)

    for p in range(10):
        if p <= score-1:
            cp.pixels[p] = score_color
        else:
            cp.pixels[p] = (0,0,0)
    sleep(0.5)

def show_win_screen():
    # Reset the game

    #cp.play_file("winner.wav")
    for x in range(6):
        cp.start_tone(220*(x+1))
        cp.pixels.fill((100,0,0))
        sleep(0.1)
        cp.pixels.fill((0,100,0))
        sleep(0.1)
        cp.pixels.fill((0,0,100))
        sleep(0.1)
        cp.stop_tone()

# Write your funky method here
while True:
    show_game()


    # Get current button presses
    button_state = cp.button_a | cp.button_b
    if button_state > last_button_state and player_position in goal_position:
        # Player hit the goal

        # First check how many goals they hit
        # and update the goal positions
        for i in range(len(goal_position)):
            if goal_position[i] == player_position:
                goal_position[i] = randrange(0,10) % 10
                score += 1

        player_direction *= -1
        update_number_of_goals()
        if cp.switch: cp.play_tone(430+(20*score), 0.2)
        show_score(True)
    elif button_state > last_button_state:
        # Player missed the goal
        player_direction *= -1
        if score > 0: score -= 1
        update_number_of_goals()
        show_score(False)
        if cp.switch: cp.play_tone(230, 1)

    if score == 10:                 # Check for win condition
        score = 0
        show_win_screen()
        numberOfGoals = 3
        update_number_of_goals()

    # Move the player 
    if score < 3:                   # Easy difficulty
        if game_timer % 4 == 0:
            player_position = (player_position+player_direction)%10
    elif score < 7:                 # Middle difficulty
        if game_timer % 3 == 0:
            player_position = (player_position+player_direction)%10
    else:
        if game_timer % 2 == 0:     # Hard Difficulty
            player_position = (player_position+player_direction)%10


    # Update old input
    last_button_state = button_state 

    #print(cp.light)
    #cp.pixels.brightness = (cp.pixels.brightness + (cp.light/100)) / 2

    # Update timer
    game_timer = (game_timer + 1) % 60
