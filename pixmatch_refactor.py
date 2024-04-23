import streamlit as st
import os
import time as tm
import random
import base64
import json
from PIL import Image
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="PixMatch", page_icon="🕹️", layout="wide", initial_sidebar_state="expanded")

#vDrive = os.path.splitdrive(os.getcwd())[0]
# if vDrive == "C:": actual_directory = "C:/Users/Shawn/dev/utils/pixmatch/"   # local developer's disc
# else: actual_directory = "./"
actual_directory = "./"

template_span = """<span style='font-size: 140px;
                      border-radius: 7px;
                      text-align: center;
                      display:inline;
                      padding-top: 3px;
                      padding-bottom: 3px;
                      padding-left: 0.4em;
                      padding-right: 0.4em;
                      '>
                      |fill_variable|
                      </span>"""

pressed_emoji = """<span style='font-size: 24px;
                                border-radius: 7px;
                                text-align: center;
                                display:inline;
                                padding-top: 3px;
                                padding-bottom: 3px;
                                padding-left: 0.2em;
                                padding-right: 0.2em;
                                '>
                                |fill_variable|
                                </span>"""

horizontal_bar = "<hr style='margin-top: 0; margin-bottom: 0; height: 1px; border: 1px solid #635985;'><br>"  # thin divider line

purple_button_colour = """
                        <style>
                            div.stButton > button:first-child {background-color: #4b0082; color:#ffffff;}
                            div.stButton > button:hover {background-color: RGB(0,112,192); color:#ffffff;}
                            div.stButton > button:focus {background-color: RGB(47,117,181); color:#ffffff;}
                        </stle>
                    """

mystate = st.session_state

if "expired_cells" not in mystate: mystate.expired_cells = []
if "my_score" not in mystate: mystate.my_score = 0
if "player_buttons" not in mystate: mystate.player_buttons = {}
if "sidebar_emoji" not in mystate: mystate.sidebar_emoji = ''
if "emoji_bank" not in mystate: mystate.emoji_bank = []
if "GameDetails" not in mystate: mystate.GameDetails = ['Medium', 6, 7,
                                                        '']  # difficulty level, sec interval for autogen, total_cells_per_row_or_col, player name


# common functions
def reduce_gap_from_page_top(which_section='main page'):
    """
    reduce_gap_from_page_top function reduces the gap from the top of the specified section in the page.

    Parameters:
        - wich section (str): Specifies the section of the page where the gap reduction should be applied.
                         It can take one of the following values:
                            - 'main page': Reduces the gap from the top of the main area.
                            - 'sidebar': Reduces the gap from the top of the sidebar.
                            - 'all': Reduces the gap from the top of both the main area and the sidebar.
    """

    if which_section == 'main page':
        st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", True)  # main area
    elif which_section == 'sidebar':
        st.markdown(" <style> div[class^='st-emotion-cache-10oheav'] { padding-top: 0rem; } </style> ", True)  # sidebar
    elif which_section == 'all':
        st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", True)  # main area
        st.markdown(" <style> div[class^='st-emotion-cache-10oheav'] { padding-top: 0rem; } </style> ", True)  # sidebar


def leaderboard_manager(what_to_do):
    """
    The leaderboard function manages the leaderboard based on the specified action.

    Args:
        - what_to_do (str): Specifies the action to perform on the leaderboard.
                        It can take one of the following values:
                            - 'create': Creates a new leaderboard file if it doesn't exist.
                            - 'write': writes the leaderboard
                            - 'read': reads the leaderboard
    """
    if what_to_do == 'create':   # Check if the action is to create a leaderboard
        if mystate.GameDetails[3] != '':
            if os.path.isfile(actual_directory + 'leaderboard.json') == False:  # Check if the game details are available and if the leaderboard file doesn't exist
                leaderboard_data = {}   # Create an empty dictionary
                json.dump(leaderboard_data, open(actual_directory + 'leaderboard.json', 'w'))   # Write the empty dictionary to a JSON file to create the leaderboard

    elif what_to_do == 'write': # Check if the action is to write in the leaderboard
        if mystate.GameDetails[3] != '':  # record in leaderboard only if player name is provided
            if os.path.isfile(actual_directory + 'leaderboard.json'):
                leaderboard = json.load(open(actual_directory + 'leaderboard.json'))  # Load the existing leaderboard data from the file
                leaderboard_dict_length = len(leaderboard)  # Get the length of the leaderboard dictionary

                leaderboard[str(leaderboard_dict_length + 1)] = {'NameCountry': mystate.GameDetails[3], 'HighestScore': mystate.my_score}  # Add the current player's information to the leaderboard
                leaderboard = dict(
                    sorted(leaderboard.items(), key=lambda item: item[1]['HighestScore'], reverse=True))  # Sort the leaderboard in descending order based on the highest score

                if len(leaderboard) > 3:  # Keep only the top 3 entries in the leaderboard. WE NEED TO CHANGE TO 4 ENTRIES IN THE TOP
                    for i in range(len(leaderboard) - 3): leaderboard.popitem()  # Remove the last key-value pair

                json.dump(leaderboard, open(actual_directory + 'leaderboard.json', 'w'))  # Write the updated leaderboard data back to the file

    elif what_to_do == 'read':
        if mystate.GameDetails[3] != '':  # record in leaderboard only if player name is provided
            if os.path.isfile(actual_directory + 'leaderboard.json'):
                leaderboard = json.load(open(actual_directory + 'leaderboard.json'))  # read file

                leaderboard = dict(
                    sorted(leaderboard.items(), key=lambda item: item[1]['HighestScore'], reverse=True))  # sort desc

                # Display the leaderboard:
                column_winner, column_winner_up1, column_winner_up2, column_winner_up3 = st.columns((2, 3, 3, 3))
                rank_count = 0
                for vkey in leaderboard.keys():
                    if leaderboard[vkey]['NameCountry'] != '':
                        rank_count += 1
                        if rank_count == 1:
                            column_winner.write('🏆 Past Winners:')
                            column_winner_up1.write(
                                f"🥇 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")
                        elif rank_count == 2:
                            column_winner_up2.write(
                                f"🥈 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")
                        elif rank_count == 3:
                            column_winner_up3.write(
                                f"🥈 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")


def initial_page():
    with st.sidebar:
        # Displaying Pix Match subheader and horizontal bar
        st.subheader("🖼️ Pix Match:")
        st.markdown(horizontal_bar, True)

        # Loading and displaying sidebar logo
        sidebarlogo = Image.open('sidebarlogo.jpg').resize((300, 390))
        st.image(sidebarlogo, use_column_width='auto')

    # ViewHelp
    # Help details HTML string
    help_details = f"""<span style="font-size: 26px;">
    <ol>
    <li style="font-size:15px";>Game play opens with (a) a sidebar picture and (b) a N x N grid of picture buttons, where N=6:Easy, N=7:Medium, N=8:Hard.</li>
    <li style="font-size:15px";>You need to match the sidebar picture with a grid picture button, by pressing the (matching) button (as quickly as possible).</li>
    <li style="font-size:15px";>Each correct picture match will earn you <strong>+N</strong> points (where N=5:Easy, N=3:Medium, N=1:Hard); each incorrect picture match will earn you <strong>-1</strong> point.</li>
    <li style="font-size:15px";>The sidebar picture and the grid pictures will dynamically regenerate after a fixed seconds interval (Easy=8, Medium=6, Hard=5). Each regeneration will have a penalty of <strong>-1</strong> point</li>
    <li style="font-size:15px";>Each of the grid buttons can only be pressed once during the entire game.</li>
    <li style="font-size:15px";>The game completes when all the grid buttons are pressed.</li>
    <li style="font-size:15px";>At the end of the game, if you have a positive score, you will have <strong>won</strong>; otherwise, you will have <strong>lost</strong>.</li>
    </ol></span>"""

    # Setting up layout for displaying game rules and instructions
    rule_column, image_column = st.columns(2)
    random.seed()
    game_help_img = actual_directory + random.choice(["MainImg1.jpg", "MainImg2.jpg", "MainImg3.jpg", "MainImg4.jpg"])
    game_help_img = Image.open(game_help_img).resize((550, 550))
    image_column.image(game_help_img, use_column_width='auto')

    # Displaying rules and instructions for playing the game
    rule_column.subheader('Rules | Playing Instructions:')
    rule_column.markdown(horizontal_bar, True)
    rule_column.markdown(help_details, unsafe_allow_html=True)
    st.markdown(horizontal_bar, True)

    # Displaying author details
    author_details = "<strong>Happy Playing: 😎 Shawn Pereira: shawnpereira1969@gmail.com</strong>"
    st.markdown(author_details, unsafe_allow_html=True)


def read_picture_file(wich_file):
    """
    Reads the content of the specified image file and returns its base64 encoded string.

    Args:
    - file_path (str): The path to the image file.

    Returns:
    - str: The base64 encoded string representing the image content.
    """

    try:
        full_file_path = f"{actual_directory}{wich_file}"  # Constructing the full file path
        return base64.b64encode(open(full_file_path, 'rb').read()).decode()    # Opening and reading the image file in binary mode, then encoding it to base64
        
    except:
        return "" # Returning an empty string if an error occurs during file reading


def pressed_check(vcell):
    """
    Checks if a button in the grid has been pressed, updates its state accordingly,
    and adjusts the player's score based on the button's correctness.

    Args:
    - cell (str): The cell identifier of the pressed button.
    """
    if mystate.player_buttons[vcell]['isPressed'] == False:
        mystate.player_buttons[vcell]['isPressed'] = True  # Mark the button as pressed
        mystate.expired_cells.append(vcell)  # Add the cell to the list of expired cells

        if mystate.player_buttons[vcell]['eMoji'] == mystate.sidebar_emoji:    # Check if the pressed button matches the sidebar emoji
            # Update the button state to correct and increase the player's score:
            mystate.player_buttons[vcell]['isTrueFalse'] = True
            mystate.my_score += 5

            # Adjust the score based on the game difficulty
            if mystate.GameDetails[0] == 'Easy':
                mystate.my_score += 5
            elif mystate.GameDetails[0] == 'Medium':
                mystate.my_score += 3
            elif mystate.GameDetails[0] == 'Hard':
                mystate.my_score += 1

        else:
            # Update the button state to incorrect and decrease the player's score
            mystate.player_buttons[vcell]['isTrueFalse'] = False
            mystate.my_score -= 1


def reset_board():
    """
       Resets the game board by assigning emojis to player buttons and the sidebar, ensuring each button cell
       has a unique emoji. If the sidebar emoji is not present in any button cell, it adds it randomly.

       """
    total_cells_per_row_or_col = mystate.GameDetails[2]   # Get the total number of cells per row or column

    # Randomly select a sidebar emoji from the emoji bank
    sidebar_emoji_no = random.randint(1, len(mystate.emoji_bank)) - 1
    mystate.sidebar_emoji = mystate.emoji_bank[sidebar_emoji_no]

    sidebar_emoji_in_list = False

    # Loop through each button cell to assign emojis
    for vcell in range(1, ((total_cells_per_row_or_col ** 2) + 1)):
        random_emoji_index = random.randint(1, len(mystate.emoji_bank)) - 1
        if mystate.player_buttons[vcell]['isPressed'] == False:
            vemoji = mystate.emoji_bank[ random_emoji_index]
            mystate.player_buttons[vcell]['eMoji'] = vemoji
            if vemoji == mystate.sidebar_emoji: sidebar_emoji_in_list = True
        
    # Check if the sidebar emoji is not in any button cell; if not, add it randomly
    if sidebar_emoji_in_list == False:  # sidebar pix is not on any button; add pix randomly
        total_cells = [x for x in range(1, ((total_cells_per_row_or_col ** 2) + 1))]
        available_cells = [x for x in total_cells if x not in mystate.expired_cells]
        if len(available_cells) > 0:
            random_index = random.randint(0, (len(available_cells) - 1))
            random_cell  = available_cells[random_index]
            mystate.player_buttons[random_cell ]['eMoji'] = mystate.sidebar_emoji


def pre_new_game():
    """
     Initializes a new game by resetting necessary game state variables and setting up the game board.

     """

    total_cells_per_row_or_col = mystate.GameDetails[2]
    mystate.expired_cells = []
    mystate.my_score = 0

    # Create lists with Emoji categories
    foxes = ['😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾']
    emojis = ['😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😊', '😇', '🙂', '🙃', '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚', '😋', '😛',
              '😝', '😜', '🤪', '🤨', '🧐', '🤓', '😎', '🤩', '🥳', '😏', '😒', '😞', '😔', '😟', '😕', '🙁', '☹️', '😣', '😖', '😫', '😩',
              '🥺', '😢', '😠', '😳', '😥', '😓', '🤗', '🤔', '🤭', '🤫', '🤥', '😶', '😐', '😑', '😬', '🙄', '😯', '😧', '😮', '😲', '🥱',
              '😴', '🤤', '😪', '😵', '🤐', '🥴', '🤒']
    humans = ['👶', '👧', '🧒', '👦', '👩', '🧑', '👨', '👩‍🦱', '👨‍🦱', '👩‍🦰', '‍👨', '👱', '👩', '👱', '👩‍', '👨‍🦳', '👩‍🦲', '👵', '🧓',
              '👴', '👲', '👳']
    foods = ['🍏', '🍎', '🍐', '🍊', '🍋', '🍌', '🍉', '🍇', '🍓', '🍈', '🍒', '🍑', '🥭', '🍍', '🥥', '🥝', '🍅', '🍆', '🥑', '🥦', '🥬',
             '🥒', '🌽', '🥕', '🧄', '🧅', '🥔', '🍠', '🥐', '🥯', '🍞', '🥖', '🥨', '🧀', '🥚', '🍳', '🧈', '🥞', '🧇', '🥓', '🥩', '🍗',
             '🍖', '🦴', '🌭', '🍔', '🍟', '🍕']
    clocks = ['🕓', '🕒', '🕑', '🕘', '🕛', '🕚', '🕖', '🕙', '🕔', '🕤', '🕠', '🕕', '🕣', '🕞', '🕟', '🕜', '🕢', '🕦']
    hands = ['🤚', '🖐', '✋', '🖖', '👌', '🤏', '✌️', '🤞', '🤟', '🤘', '🤙', '👈', '👉', '👆', '🖕', '👇', '☝️', '👍', '👎', '✊', '👊',
             '🤛', '🤜', '👏', '🙌', '🤲', '🤝', '🤚🏻', '🖐🏻', '✋🏻', '🖖🏻', '👌🏻', '🤏🏻', '✌🏻', '🤞🏻', '🤟🏻', '🤘🏻', '🤙🏻', '👈🏻',
             '👉🏻', '👆🏻', '🖕🏻', '👇🏻', '☝🏻', '👍🏻', '👎🏻', '✊🏻', '👊🏻', '🤛🏻', '🤜🏻', '👏🏻', '🙌🏻', '🤚🏽', '🖐🏽', '✋🏽', '🖖🏽',
             '👌🏽', '🤏🏽', '✌🏽', '🤞🏽', '🤟🏽', '🤘🏽', '🤙🏽', '👈🏽', '👉🏽', '👆🏽', '🖕🏽', '👇🏽', '☝🏽', '👍🏽', '👎🏽', '✊🏽', '👊🏽',
             '🤛🏽', '🤜🏽', '👏🏽', '🙌🏽']
    animals = ['🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐨', '🐯', '🦁', '🐮', '🐷', '🐽', '🐸', '🐵', '🙈', '🙉', '🙊', '🐒', '🐔',
               '🐧', '🐦', '🐤', '🐣', '🐥', '🦆', '🦅', '🦉', '🦇', '🐺', '🐗', '🐴', '🦄', '🐝', '🐛', '🦋', '🐌', '🐞', '🐜', '🦟', '🦗',
               '🦂', '🐢', '🐍', '🦎', '🦖', '🦕', '🐙', '🦑', '🦐', '🦞', '🦀', '🐡', '🐠', '🐟', '🐬', '🐳', '🐋', '🦈', '🐊', '🐅', '🐆',
               '🦓', '🦍', '🦧', '🐘', '🦛', '🦏', '🐪', '🐫', '🦒', '🦘', '🐃', '🐂', '🐄', '🐎', '🐖', '🐏', '🐑', '🦙', '🐐', '🦌', '🐕',
               '🐩', '🦮', '🐕‍🦺', '🐈', '🐓', '🦃', '🦚', '🦜', '🦢', '🦩', '🐇', '🦝', '🦨', '🦦', '🦥', '🐁', '🐀', '🦔']
    vehicles = ['🚗', '🚕', '🚙', '🚌', '🚎', '🚓', '🚑', '🚒', '🚐', '🚚', '🚛', '🚜', '🦯', '🦽', '🦼', '🛴', '🚲', '🛵', '🛺', '🚔', '🚍',
                '🚘', '🚖', '🚡', '🚠', '🚟', '🚃', '🚋', '🚞', '🚝', '🚄', '🚅', '🚈', '🚂', '🚆', '🚇', '🚊', '🚉', '✈️', '🛫', '🛬',
                '💺', '🚀', '🛸', '🚁', '🛶', '⛵️', '🚤', '🛳', '⛴', '🚢']
    houses = ['🏠', '🏡', '🏘', '🏚', '🏗', '🏭', '🏢', '🏬', '🏣', '🏤', '🏥', '🏦', '🏨', '🏪', '🏫', '🏩', '💒', '🏛', '⛪️', '🕌', '🕍',
              '🛕']
    purple_signs = ['☮️', '✝️', '☪️', '☸️', '✡️', '🔯', '🕎', '☯️', '☦️', '🛐', '⛎', '♈️', '♉️', '♊️', '♋️', '♌️', '♍️',
                    '♎️', '♏️', '♐️', '♑️', '♒️', '♓️', '🆔', '🈳']
    red_signs = ['🈶', '🈚️', '🈸', '🈺', '🈷️', '✴️', '🉐', '㊙️', '㊗️', '🈴', '🈵', '🈹', '🈲', '🅰️', '🅱️', '🆎', '🆑', '🅾️', '🆘',
                 '🚼', '🛑', '⛔️', '📛', '🚫', '🚷', '🚯', '🚳', '🚱', '🔞', '📵', '🚭']
    blue_signs = ['🚾', '♿️', '🅿️', '🈂️', '🛂', '🛃', '🛄', '🛅', '🚹', '🚺', '🚻', '🚮', '🎦', '📶', '🈁', '🔣', '🔤', '🔡', '🔠', '🆖',
                  '🆗', '🆙', '🆒', '🆕', '🆓', '0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟',
                  '🔢', '⏏️', '▶️', '⏸', '⏯', '⏹', '⏺', '⏭', '⏮', '⏩', '⏪', '⏫', '⏬', '◀️', '🔼', '🔽', '➡️', '⬅️', '⬆️',
                  '⬇️', '↗️', '↘️', '↙️', '↖️', '↪️', '↩️', '⤴️', '⤵️', '🔀', '🔁', '🔂', '🔄', '🔃', '➿', '🔚', '🔙', '🔛',
                  '🔝', '🔜']
    moon = ['🌕', '🌔', '🌓', '🌗', '🌒', '🌖', '🌑', '🌜', '🌛', '🌙']

    random.seed() # Seed the random number generator

    # Determine which emoji bank to use based on the game difficulty:
    if mystate.GameDetails[0] == 'Easy':
        wich_bank = random.choice(['foods', 'moon', 'animals'])
        mystate.emoji_bank = locals()[wich_bank]

    elif mystate.GameDetails[0] == 'Medium':
        wich_bank = random.choice(
            ['foxes', 'emojis', 'humans', 'vehicles', 'houses', 'hands', 'purple_signs', 'red_signs', 'blue_signs'])
        mystate.emoji_bank = locals()[wich_bank]

    elif mystate.GameDetails[0] == 'Hard':
        wich_bank = random.choice(
            ['foxes', 'emojis', 'humans', 'foods', 'clocks', 'hands', 'animals', 'vehicles', 'houses', 'purple_signs',
             'red_signs', 'blue_signs', 'moon'])
        mystate.emoji_bank = locals()[wich_bank]

    # Initialize player buttons
    mystate.player_buttons = {}
    for vcell in range(1, ((total_cells_per_row_or_col ** 2) + 1)): mystate.player_buttons[vcell] = {'isPressed': False, 'isTrueFalse': False, 'eMoji': ''}


def score_emoji():
    """
    Determine the appropriate emoji based on the player's score
    """

    if mystate.my_score == 0:
        return '😐'
    elif -5 <= mystate.my_score <= -1:
        return '😏'
    elif -10 <= mystate.my_score <= -6:
        return '☹️'
    elif mystate.my_score <= -11:
        return '😖'
    elif 1 <= mystate.my_score <= 5:
        return '🙂'
    elif 6 <= mystate.my_score <= 10:
        return '😊'
    elif mystate.my_score > 10:
        return '😁'


def new_game():
    """
       Function to initialize a new game session. This function resets the game board, displays the game interface including
       the sidebar with game details and score, generates buttons for each cell on the board, handles button clicks and
       updates the score, and checks for game completion to display appropriate effects. It also manages the auto-refresh
       timer, reads and writes to the leaderboard, and returns to the main page after the game is completed.
    """


    reset_board()
    total_cells_per_row_or_col = mystate.GameDetails[2]

    # Reduce gap from page top for sidebar
    reduce_gap_from_page_top('sidebar')

    # Sidebar layout
    with st.sidebar:
        st.subheader(f"🖼️ Pix Match: {mystate.GameDetails[0]}")
        st.markdown(horizontal_bar, True)

        st.markdown(template_span.replace('|fill_variable|', mystate.sidebar_emoji), True)

        aftimer = st_autorefresh(interval=(mystate.GameDetails[1] * 1000), key="aftmr")
        if aftimer > 0: mystate.my_score -= 1

        st.info(
            f"{score_emoji()} Score: {mystate.my_score} | Pending: {(total_cells_per_row_or_col ** 2) - len(mystate.expired_cells)}")

        st.markdown(horizontal_bar, True)
        if st.button(f"🔙 Return to Main Page", use_container_width=True):
            mystate.runpage = main
            st.rerun()

    # Read leaderboard
    leaderboard_manager('read')

    # Picture Positions
    st.subheader("Picture Positions:")
    st.markdown(horizontal_bar, True)

    # Set board defaults
    st.markdown("<style> div[class^='css-1vbkxwb'] > p { font-size: 1.5rem; } </style> ",
                unsafe_allow_html=True)  # make button face big
    # Create columns for each row
    for i in range(1, (total_cells_per_row_or_col + 1)):
        total_cells = ([1] * total_cells_per_row_or_col) + [2]  # 2 = rt side padding
        globals()['cols' + str(i)] = st.columns(total_cells)
    # Display buttons for each cell
    for vcell in range(1, (total_cells_per_row_or_col ** 2) + 1):

        # Display buttons for each cell
        if 1 <= vcell <= (total_cells_per_row_or_col * 1):
            arr_ref = '1'
            mval = 0

        elif ((total_cells_per_row_or_col * 1) + 1) <= vcell <= (total_cells_per_row_or_col * 2):
            arr_ref = '2'
            mval = (total_cells_per_row_or_col * 1)

        elif ((total_cells_per_row_or_col * 2) + 1) <= vcell <= (total_cells_per_row_or_col * 3):
            arr_ref = '3'
            mval = (total_cells_per_row_or_col * 2)

        elif ((total_cells_per_row_or_col * 3) + 1) <= vcell <= (total_cells_per_row_or_col * 4):
            arr_ref = '4'
            mval = (total_cells_per_row_or_col * 3)

        elif ((total_cells_per_row_or_col * 4) + 1) <= vcell <= (total_cells_per_row_or_col * 5):
            arr_ref = '5'
            mval = (total_cells_per_row_or_col * 4)

        elif ((total_cells_per_row_or_col * 5) + 1) <= vcell <= (total_cells_per_row_or_col * 6):
            arr_ref = '6'
            mval = (total_cells_per_row_or_col * 5)

        elif ((total_cells_per_row_or_col * 6) + 1) <= vcell <= (total_cells_per_row_or_col * 7):
            arr_ref = '7'
            mval = (total_cells_per_row_or_col * 6)

        elif ((total_cells_per_row_or_col * 7) + 1) <= vcell <= (total_cells_per_row_or_col * 8):
            arr_ref = '8'
            mval = (total_cells_per_row_or_col * 7)

        elif ((total_cells_per_row_or_col * 8) + 1) <= vcell <= (total_cells_per_row_or_col * 9):
            arr_ref = '9'
            mval = (total_cells_per_row_or_col * 8)

        elif ((total_cells_per_row_or_col * 9) + 1) <= vcell <= (total_cells_per_row_or_col * 10):
            arr_ref = '10'
            mval = (total_cells_per_row_or_col * 9)

        # Clear button content if pressed, else display emoji
        globals()['cols' + arr_ref][vcell - mval] = globals()['cols' + arr_ref][vcell - mval].empty()
        if mystate.player_buttons[vcell]['isPressed'] == True:
            if mystate.player_buttons[vcell]['isTrueFalse'] == True:
                globals()['cols' + arr_ref][vcell - mval].markdown(pressed_emoji.replace('|fill_variable|', '✅️'), True)

            elif mystate.player_buttons[vcell]['isTrueFalse'] == False:
                globals()['cols' + arr_ref][vcell - mval].markdown(pressed_emoji.replace('|fill_variable|', '❌'), True)

        else:
            vemoji = mystate.player_buttons[vcell]['eMoji']
            globals()['cols' + arr_ref][vcell - mval].button(vemoji, on_click=pressed_check, args=(vcell,),
                                                             key=f"B{vcell}")

    st.caption('')  # vertical filler
    st.markdown(horizontal_bar, True)

    # Check if all cells are pressed
    if len(mystate.expired_cells) == (total_cells_per_row_or_col ** 2):
        leaderboard_manager('write')

        # Display balloons for positive score, snow for negative score
        if mystate.my_score > 0:
            st.balloons()
        elif mystate.my_score <= 0:
            st.snow()

        # Wait for 5 seconds before returning to main page
        tm.sleep(5)
        mystate.runpage = main
        st.rerun()


def main():

    """
    Function to display the main page of the game. It sets up the layout, including the sidebar for game settings
    and options. It allows the user to select the difficulty level and input their name and country for the leaderboard.
    The function also handles the creation of a new game session when the user clicks the 'New Game' button, based on the
    selected difficulty level. It then redirects to the 'new_game' function to start the game.
    """


    st.markdown('<style>[data-testid="stSidebar"] > div:first-child {width: 310px;}</style>',
                unsafe_allow_html=True, )  # reduce sidebar width
    st.markdown(purple_button_colour, unsafe_allow_html=True)

    initial_page()
    with st.sidebar:
        mystate.GameDetails[0] = st.radio('Difficulty Level:', options=('Easy', 'Medium', 'Hard'), index=1,
                                          horizontal=True, )
        mystate.GameDetails[3] = st.text_input("Player Name, Country", placeholder='Shawn Pereira, India',
                                               help='Optional input only for leaderboard_manager')

        if st.button(f"🕹️ New Game", use_container_width=True):

            if mystate.GameDetails[0] == 'Easy':
                mystate.GameDetails[1] = 8  # secs interval
                mystate.GameDetails[2] = 6  # total_cells_per_row_or_col

            elif mystate.GameDetails[0] == 'Medium':
                mystate.GameDetails[1] = 6  # secs interval
                mystate.GameDetails[2] = 7  # total_cells_per_row_or_col

            elif mystate.GameDetails[0] == 'Hard':
                mystate.GameDetails[1] = 5  # secs interval
                mystate.GameDetails[2] = 8  # total_cells_per_row_or_col

            leaderboard_manager('create')

            pre_new_game()
            mystate.runpage = new_game
            st.rerun()

        st.markdown(horizontal_bar, True)


if 'runpage' not in mystate: mystate.runpage = main
mystate.runpage()