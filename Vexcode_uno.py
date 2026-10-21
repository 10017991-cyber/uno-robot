import random
from vex import *

# Initialize EXP Brain
brain = Brain()

# --- HARDWARE SETUP ---
motor_1 = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
motor_5 = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True)

SCREEN_ROWS = 5
SCREEN_COLS = 16



# --- ROBOT ROUTINE HELPERS USING BROADCASTS ---

def move_to_center():
    """Drives forward 2 units to the center game pile using FWD broadcasts."""
    brain.screen.clear_screen()
    display_line(1, "DRIVING TO")
    display_line(2, "CENTER PILE...")
    FWD.broadcast_and_wait()
    FWD.broadcast_and_wait()

def return_to_player():
    """Turns 180, drives 2 units back to player, and re-orients using RT and FWD broadcasts."""
    brain.screen.clear_screen()
    display_line(1, "RETURNING TO")
    display_line(2, "PLAYER...")
    # Turn 180 degrees (2 right turns)
    RT.broadcast_and_wait()
    RT.broadcast_and_wait()
    # Drive back to player position
    FWD.broadcast_and_wait()
    FWD.broadcast_and_wait()
    # Turn 180 degrees back to face center
    RT.broadcast_and_wait()
    RT.broadcast_and_wait()

def victory_dance():
    """Victory dance routine: spins 360 degrees when winning."""
    brain.screen.clear_screen()
    display_line(1, "VICTORY DANCE!")
    display_line(3, "*** WINNER ***")
    # Spin around using RT turns
    for _ in range(4):
        RT.broadcast_and_wait()
        brain.play_sound(SoundType.TADA)

# --- DECK & HAND SETUP ---

def create_uno_deck():
    colors = ['Red', 'Yellow', 'Green', 'Blue']
    values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Skip', 'Reverse', 'Draw 2']
    deck = []

    for color in colors:
        for val in values:
            card_name = color + " " + val
            if val == '0':
                deck.append(card_name)
            else:
                deck.append(card_name)
                deck.append(card_name)

    for _ in range(4):
        deck.append("Wild")
        deck.append("Wild Draw 4")

    return deck

def custom_shuffle(deck):
    n = len(deck)
    for i in range(n - 1, 0, -1):
        j = random.randint(0, i)
        deck[i], deck[j] = deck[j], deck[i]

def deal_hand(deck, num_cards=7):
    hand = []
    for _ in range(num_cards):
        if len(deck) > 0:
            hand.append(deck.pop(0))
    return hand

# --- SCREEN & DISPLAY HELPERS ---

def display_line(row, text):
    """Prints text safely within the 16-character hardware screen limit."""
    brain.screen.set_cursor(row, 1)
    if len(text) > SCREEN_COLS:
        text = text[:SCREEN_COLS]
    brain.screen.print(text)

def display_hand_on_screen(hand):
    """Lists all stored cards on the screen between turns."""
    brain.screen.clear_screen()
    brain.screen.set_fill_color(Color.BLACK)
    brain.screen.set_pen_color(Color.WHITE)
    
    display_line(1, "STORED HAND (" + str(len(hand)) + "):")
    
    # Display up to 3 cards fit on lines 2, 3, and 4
    for idx in range(min(3, len(hand))):
        card_text = str(idx + 1) + ":" + hand[idx]
        display_line(idx + 2, card_text)
        
    display_line(5, "[Check] Continue")
    while wait_for_button_press() != "CHECK":
        pass

# --- FULL SCREEN CARD GRAPHICS FROM GOOGLE DOC ---

def draw_card_full_screen(card_str, color_code):
    """Renders pixel-level card graphics based on Google Doc template."""
    brain.screen.clear_screen()

    if color_code == 'R':
        brain.screen.set_fill_color(Color.RED)
    elif color_code == 'G':
        brain.screen.set_fill_color(Color.GREEN)
    elif color_code == 'B':
        brain.screen.set_fill_color(Color.BLUE)
    elif color_code == 'Y':
        brain.screen.set_fill_color(Color.YELLOW)
    else:
        brain.screen.set_fill_color(Color.BLACK)

    brain.screen.set_pen_color(Color.WHITE)

    for i in range(5):
        brain.screen.draw_rectangle(0+i, 0+i, 159-(i*2), 107-(i*2))

    card = card_str[1:] if len(card_str) > 1 else card_str

    if card == "0":
        for i in range(15):
            brain.screen.draw_rectangle(20+i, 20+i, 119-(i*2), 67-(i*2))
    elif card == "8":
        for i in range(15):
            brain.screen.draw_rectangle(20+i, 20+i, 119-(i*2), 67-(i*2))
        for i in range(15):
            brain.screen.draw_line(72+i, 20, 72+i, 85)
    elif card == "1":
        for i in range(15):
            brain.screen.draw_line(20, 47+i, 139, 47+i)
    elif card == "3":
        for i in range(15):
            brain.screen.draw_line(20, 20+i, 139, 20+i)
            brain.screen.draw_line(20+i, 20, 20+i, 87)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(125+i, 20, 125+i, 87)
    elif card == "2":
        for i in range(15):
            brain.screen.draw_line(20+i, 20, 20+i, 87)
            brain.screen.draw_line(20, 20+i, 72, 20+i)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(72, 73+i, 139, 73+i)
            brain.screen.draw_line(125+i, 20, 125+i, 87)
        for i in range(3):
            brain.screen.draw_line(145+i, 20, 145+i, 87)
    elif card == "5":
        for i in range(15):
            brain.screen.draw_line(20+i, 20, 20+i, 87)
            brain.screen.draw_line(20, 73+i, 72, 73+i)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(72, 20+i, 139, 20+i)
            brain.screen.draw_line(125+i, 20, 125+i, 87)
        for i in range(3):
            brain.screen.draw_line(145+i, 20, 145+i, 87)
    elif card == "6":
        for i in range(15):
            brain.screen.draw_line(20+i, 20, 20+i, 87)
            brain.screen.draw_line(20, 73+i, 72, 73+i)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(72, 20+i, 139, 20+i)
            brain.screen.draw_line(125+i, 20, 125+i, 87)
            brain.screen.draw_line(72, 73+i, 139, 73+i)
        for i in range(3):
            brain.screen.draw_line(145+i, 20, 145+i, 87)
    elif card == "9":
        for i in range(15):
            brain.screen.draw_line(20+i, 20, 20+i, 87)
            brain.screen.draw_line(20, 20+i, 72, 20+i)
            brain.screen.draw_line(20, 73+i, 72, 73+i)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(72, 20+i, 139, 20+i)
            brain.screen.draw_line(125+i, 20, 125+i, 87)
        for i in range(3):
            brain.screen.draw_line(145+i, 20, 145+i, 87)
    elif card == "4" and "D" not in card_str:
        for i in range(15):
            brain.screen.draw_line(20, 20+i, 72, 20+i)
            brain.screen.draw_line(20, 73+i, 72, 73+i)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(72, 20+i, 139, 20+i)
    elif card == "7":
        for i in range(15):
            brain.screen.draw_line(20, 20+i, 139, 20+i)
            brain.screen.draw_line(20+i, 20, 20+i, 87)
    elif card == "Rv":
        for i in range(15):
            brain.screen.draw_line(62+i, 30, 62+i, 87)
            brain.screen.draw_line(69, 20, 52+i, 40)
            brain.screen.draw_line(69, 20, 82-i, 40)
            brain.screen.draw_line(82+i, 20, 82+i, 77)
            brain.screen.draw_line(89, 87, 74+i, 67)
            brain.screen.draw_line(89, 87, 104-i, 67)
    elif card == "S":
        for i in range(15):
            brain.screen.draw_rectangle(40+i, 20+i, 82-(i*2), 67-(i*2))
        for i in range(15):
            brain.screen.draw_line(52+i, 20, 92+i, 80)
    elif card == "D2":
        brain.screen.set_fill_color(Color.WHITE)
        for i in range(40):
            brain.screen.draw_circle(60+i, 42+int(i/2), 30)
        if color_code == 'R': brain.screen.set_fill_color(Color.RED)
        elif color_code == 'G': brain.screen.set_fill_color(Color.GREEN)
        elif color_code == 'B': brain.screen.set_fill_color(Color.BLUE)
        elif color_code == 'Y': brain.screen.set_fill_color(Color.YELLOW)
        brain.screen.draw_rectangle(47, 32, 40, 25)
        brain.screen.draw_rectangle(73, 52, 40, 25)
        for i in range(5):
            brain.screen.draw_line(18+i, 85, 18+i, 95)
            brain.screen.draw_line(14, 88+i, 26, 88+i)
            brain.screen.draw_line(10+i, 66, 10+i, 79)
            brain.screen.draw_line(10, 66+i, 20, 66+i)
            brain.screen.draw_line(18+i, 66, 18+i, 79)
            brain.screen.draw_line(20, 75+i, 30, 75+i)
            brain.screen.draw_line(26+i, 66, 26+i, 79)
            brain.screen.draw_line(159-18-i, 107-85, 159-18-i, 107-95)
            brain.screen.draw_line(159-14, 107-88-i, 159-26, 107-88-i)
            brain.screen.draw_line(159-10-i, 107-66, 159-10-i, 107-79)
            brain.screen.draw_line(159-10, 107-66-i, 159-20, 107-66-i)
            brain.screen.draw_line(159-18-i, 107-66, 159-18-i, 107-79)
            brain.screen.draw_line(159-20, 107-75-i, 159-30, 107-75-i)
            brain.screen.draw_line(159-26-i, 107-66, 159-26-i, 107-79)
    elif card_str == "W":
        brain.screen.set_fill_color(Color.BLUE)
        brain.screen.draw_rectangle(50, 20, 30, 32)
        brain.screen.set_fill_color(Color.RED)
        brain.screen.draw_rectangle(50, 52, 30, 32)
        brain.screen.set_fill_color(Color.GREEN)
        brain.screen.draw_rectangle(80, 20, 30, 32)
        brain.screen.set_fill_color(Color.YELLOW)
        brain.screen.draw_rectangle(80, 52, 30, 32)
        brain.screen.set_fill_color(Color.TRANSPARENT)
        brain.screen.set_pen_width(3)
        for i in range(15):
            brain.screen.draw_circle(80, 52, int(30-(i/5)))
        brain.screen.set_pen_color(Color.BLACK)
        for i in range(65):
            brain.screen.draw_circle(80, 52, int(31+(i/5)))
        brain.screen.set_pen_width(1)
    elif card_str == "D4":
        brain.screen.set_fill_color(Color.YELLOW)
        brain.screen.draw_rectangle(78, 42, 40, 25)
        brain.screen.set_fill_color(Color.GREEN)
        brain.screen.draw_rectangle(60, 28, 40, 25)
        brain.screen.set_fill_color(Color.BLUE)
        brain.screen.draw_rectangle(42, 42, 40, 25)
        brain.screen.set_fill_color(Color.RED)
        brain.screen.draw_rectangle(60, 56, 40, 25)
        for i in range(5):
            brain.screen.draw_line(18+i, 85, 18+i, 95)
            brain.screen.draw_line(14, 88+i, 26, 88+i)
            brain.screen.draw_line(10, 75+i, 20, 75+i)
            brain.screen.draw_line(16+i, 75, 16+i, 66)
            brain.screen.draw_line(10, 66+i, 30, 66+i)
            brain.screen.draw_line(159-18-i, 107-85, 159-18-i, 107-95)
            brain.screen.draw_line(159-14, 107-88-i, 159-26, 107-88-i)
            brain.screen.draw_line(159-10, 107-75-i, 159-20, 107-75-i)
            brain.screen.draw_line(159-16-i, 107-75, 159-16-i, 107-66)
            brain.screen.draw_line(159-10, 107-66-i, 159-30, 107-66-i)
    else:
        # Default / Back of Card Graphic (Red oval with UNO logo)
        brain.screen.set_fill_color(Color.RED)
        brain.screen.set_pen_color(Color.RED)
        for i in range(40):
            brain.screen.draw_circle(60+i, 42+int(i/2), 30)
        brain.screen.set_pen_color(Color.YELLOW)
        for i in range(5):
            brain.screen.draw_line(75, 50+i-5, 85, 50+i-5)
            brain.screen.draw_line(75, 50+i+5, 85, 50+i+5)
            brain.screen.draw_line(75, 50+i+5, 85, 50+i-5)
            brain.screen.draw_line(75, 50+i-15, 85, 50+i-15)
            brain.screen.draw_line(75+int(i/2), 50-15, 75+int(i/2), 50-25)
            brain.screen.draw_line(83+int(i/2), 50-15, 83+int(i/2), 50-25)
            brain.screen.draw_line(75, 50+i-25, 85, 50+i-25)
            brain.screen.draw_line(75, 50+i+15, 85, 50+i+15)
            brain.screen.draw_line(83+int(i/2), 50+15, 83+int(i/2), 50+25)
            brain.screen.draw_line(75, 50+i+25, 85, 50+i+25)
        brain.screen.set_fill_color(Color.TRANSPARENT)

def convert_and_render_card(card_name):
    """Converts game card names to card frame parameters and resets text colors."""
    if card_name == "BACK":
        draw_card_full_screen("BACK", "R")
    elif "Wild Draw 4" in card_name:
        draw_card_full_screen("D4", "W")
    elif "Wild" in card_name:
        draw_card_full_screen("W", "W")
    elif " " in card_name:
        color, val = card_name.split(" ", 1)
        color_code = color[0].upper()
        if val == "Draw 2":
            card_str = color_code + "D2"
        elif val == "Skip":
            card_str = color_code + "S"
        elif val == "Reverse":
            card_str = color_code + "Rv"
        else:
            card_str = color_code + val
        draw_card_full_screen(card_str, color_code)
    else:
        draw_card_full_screen("BACK", "R")

    # Reset screen colors back to standard white text on black background
    brain.screen.set_fill_color(Color.BLACK)
    brain.screen.set_pen_color(Color.WHITE)

def process_card_discard(played_card, remaining_hand_count):
    """Handles discarding: renders card graphic first, drives, and triggers sound alerts."""
    # Step 1: Render the card graphic FIRST
    convert_and_render_card(played_card)
    
    # Trigger audio ON DISCARD:
    if remaining_hand_count == 1:
        # Down to 1 card (UNO Alert sound)
        try:
            brain.play_sound(SoundType.SIREN)
        except:
            try:
                brain.play_sound("siren")
            except:
                pass
    elif remaining_hand_count == 0:
        # Discarding final winning card (Victory sound)
        try:
            brain.play_sound("tada")
        except:
            try:
                brain.play_sound("fanfare")
            except:
                try:
                    brain.play_sound("siren")
                except:
                    pass

    # Step 2: Drive to center pile and return
    FWD.broadcast_and_wait()
    FWD.broadcast_and_wait()
    return_to_player()

    # Step 3: Announce UNO after returning if 1 card remains
    if remaining_hand_count == 1:
        brain.screen.clear_screen()
        display_line(1, "*** UNO! ***")
        display_line(3, "1 CARD LEFT!")
        wait(1, SECONDS)

def wait_for_button_press():
    """Waits for Left, Right, or Check button input."""
    while True:
        if brain.buttonLeft.pressing():
            while brain.buttonLeft.pressing():
                wait(20, MSEC)
            return "LEFT"
        elif brain.buttonRight.pressing():
            while brain.buttonRight.pressing():
                wait(20, MSEC)
            return "RIGHT"
        elif brain.buttonCheck.pressing():
            while brain.buttonCheck.pressing():
                wait(20, MSEC)
            return "CHECK"
        wait(20, MSEC)

def print_hand_to_terminal(hand):
    """Outputs current stored hand to terminal console."""
    print("\n--- ROBOT STORED HAND (" + str(len(hand)) + " Cards) ---")
    for idx, card in enumerate(hand, start=1):
        print(str(idx) + ": " + card)
    print("---------------------------------------")

# --- ATTACK CHECK & MULTIPLAYER MENUS ---

def check_attack_phase(hand, deck):
    """Asks if real player attacked. Plays Draw 2 counter or forces robot to draw 2."""
    brain.screen.clear_screen()
    display_line(1, "ATTACK PHASE")
    display_line(2, "Did opponent")
    display_line(3, "play Draw 2?")
    display_line(4, "<L/R> NO")
    display_line(5, "[Check] YES")

    btn = wait_for_button_press()
    if btn == "CHECK":
        draw2_indices = [i for i, c in enumerate(hand) if "Draw 2" in c]
        
        if len(draw2_indices) > 0:
            played_card = hand.pop(draw2_indices[0])
            print("\nAttack countered! Robot driving to discard: " + played_card)
            
            process_card_discard(played_card, len(hand))
            
            # If counter attack emptied the hand, jump straight to victory dance
            if len(hand) == 0:
                victory_dance()
                return played_card

            brain.screen.clear_screen()
            display_line(1, "COUNTER ATTACK!")
            display_line(2, "Robot played:")
            display_line(3, played_card)
            display_line(5, "[Check] Continue")
            while wait_for_button_press() != "CHECK":
                pass
            return played_card
        else:
            print("\nRobot has no Draw 2! Driving to center to draw 2 penalty cards...")
            
            convert_and_render_card("BACK")
            FWD.broadcast_and_wait()
            FWD.broadcast_and_wait()
            
            drawn_cards = []
            for _ in range(2):
                if len(deck) > 0:
                    c = deck.pop(0)
                    hand.append(c)
                    drawn_cards.append(c)
            
            return_to_player()

            brain.screen.clear_screen()
            display_line(1, "NO DRAW 2 CARD!")
            display_line(2, "Took 2 cards!")
            display_line(5, "[Check] Continue")
            while wait_for_button_press() != "CHECK":
                pass
            return None
    return None

def set_discard_pile_menu():
    """Prompt the player to select the card played by the real-life opponent."""
    colors = ['Red', 'Yellow', 'Green', 'Blue', 'Wild']
    color_idx = 0
    
    while True:
        brain.screen.clear_screen()
        display_line(1, "OPPONENT PLAYED:")
        display_line(2, "Color: " + colors[color_idx])
        display_line(4, "<L/R> Change")
        display_line(5, "[Check] Next")

        btn = wait_for_button_press()
        if btn == "LEFT":
            color_idx = (color_idx - 1) % len(colors)
        elif btn == "RIGHT":
            color_idx = (color_idx + 1) % len(colors)
        elif btn == "CHECK":
            selected_color = colors[color_idx]
            break

    if selected_color == "Wild":
        print("Opponent played: Wild")
        return "Wild"

    values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Skip', 'Reverse', 'Draw 2']
    val_idx = 0

    while True:
        brain.screen.clear_screen()
        display_line(1, "OPPONENT PLAYED:")
        display_line(2, selected_color)
        display_line(3, "Val: " + values[val_idx])
        display_line(5, "<L/R>  [Check]")

        btn = wait_for_button_press()
        if btn == "LEFT":
            val_idx = (val_idx - 1) % len(values)
        elif btn == "RIGHT":
            val_idx = (val_idx + 1) % len(values)
        elif btn == "CHECK":
            selected_val = values[val_idx]
            break

    top_card = selected_color + " " + selected_val
    print("Opponent played: " + top_card)
    return top_card

def is_valid_play(card, top_card):
    """Accurately checks if a stored card matches the opponent's card or is Wild."""
    if "Wild" in card:
        return True

    if top_card == "Wild" or top_card == "Wild Draw 4":
        return True

    if " " in card and " " in top_card:
        card_color, card_val = card.split(" ", 1)
        top_color, top_val = top_card.split(" ", 1)

        if card_color == top_color or card_val == top_val:
            return True

    return False

def player_turn_menu(hand, deck, top_discard):
    """Allows cycling through stored cards to see what is AVAILABLE vs INVALID."""
    playable_indices = [i for i, c in enumerate(hand) if is_valid_play(c, top_discard)]
    
    # Forced Draw if no cards match
    if len(playable_indices) == 0:
        brain.screen.clear_screen()
        display_line(1, "NO VALID CARDS!")
        display_line(2, "Vs: " + top_discard)
        display_line(4, "Must draw 1 card")
        display_line(5, "[Check] Draw Card")
        
        print("\nNo playable cards against " + top_discard + ". Robot driving to draw...")
        while wait_for_button_press() != "CHECK":
            pass
            
        convert_and_render_card("BACK")
        FWD.broadcast_and_wait()
        FWD.broadcast_and_wait()
        
        if len(deck) > 0:
            drawn_card = deck.pop(0)
            hand.append(drawn_card)
            print("Robot added drawn card: " + drawn_card)
            
        return_to_player()
            
        brain.screen.clear_screen()
        display_line(1, "CARD DRAWN!")
        display_line(2, "Added to Hand")
        display_line(5, "[Check] End Turn")
        while wait_for_button_press() != "CHECK":
            pass
        return top_discard

    # Interactive Navigation of Hand
    cursor_idx = 0
    while True:
        selected_card = hand[cursor_idx]
        can_play = is_valid_play(selected_card, top_discard)
        
        brain.screen.clear_screen()
        display_line(1, "Vs: " + top_discard)
        display_line(2, "Card " + str(cursor_idx + 1) + "/" + str(len(hand)))
        display_line(3, selected_card)
        display_line(4, "Status: " + ("AVAILABLE" if can_play else "INVALID"))
        display_line(5, "<L/R>  [Check]")

        btn = wait_for_button_press()
        if btn == "LEFT":
            cursor_idx = (cursor_idx - 1) % len(hand)
        elif btn == "RIGHT":
            cursor_idx = (cursor_idx + 1) % len(hand)
        elif btn == "CHECK":
            if can_play:
                played_card = hand.pop(cursor_idx)
                print("Robot playing card: " + played_card)
                
                # Discard sequence: graphic first -> drive & return
                process_card_discard(played_card, len(hand))
                
                # If playing the final card, execute victory dance immediately
                if len(hand) == 0:
                    victory_dance()
                    return played_card
                
                brain.screen.clear_screen()
                display_line(1, "PLAYED CARD:")
                display_line(2, played_card)
                display_line(5, "[Check] Confirm")
                while wait_for_button_press() != "CHECK":
                    pass
                return played_card
            else:
                brain.screen.clear_screen()
                display_line(1, "CANNOT PLAY!")
                display_line(2, "Card is INVALID")
                display_line(3, "Must match color")
                display_line(4, "or value.")
                display_line(5, "[Check] Back")
                while wait_for_button_press() != "CHECK":
                    pass

# --- MAIN GAME LOOP ---

def run_multiplayer_game():
    uno_deck = create_uno_deck()
    custom_shuffle(uno_deck)
    player_hand = deal_hand(uno_deck, 7)

    game_over = False
    turn_count = 1
    top_discard = "Red 0"

    while not game_over:
        print("\n====================")
        print("ROUND " + str(turn_count))
        print_hand_to_terminal(player_hand)

        # Display all stored cards on screen at start of round
        display_hand_on_screen(player_hand)

        # 1. Ask "Do you have an attack?"
        counter_card = check_attack_phase(player_hand, uno_deck)

        if counter_card is not None:
            top_discard = counter_card
        else:
            # 2. Select card played by real-life opponent
            top_discard = set_discard_pile_menu()
            # 3. Choose available card from hand & perform broadcast driving sequence
            top_discard = player_turn_menu(player_hand, uno_deck, top_discard)

        if len(player_hand) == 0:
            print("\n*** GAME OVER: Robot player has cleared all stored cards! ***")
            game_over = True
        else:
            # Display all stored cards on screen between turns
            display_hand_on_screen(player_hand)
            turn_count += 1

# Run game assistant
run_multiplayer_game()
