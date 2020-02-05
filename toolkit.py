
#
# Various useful functions
#

# from IPython.display import HTML, display
from Board import *
from Player import *
from time import time
import numpy as np
import matplotlib.pyplot as plt



## (Doesn't work) Show the board

# def print_board(board):
#     display(HTML("""
#     <style>
#     .rendered_html table, .rendered_html th, .rendered_html tr, .rendered_html td {
#       border: 1px  black solid !important;
#       color: black !important;
#     }
#     </style>
#     """+board.html_str()))



## Play a whole game

def play_game(board: Board, player1: Player, player2: Player):
    """
    Plays a whole game
    :return: The result of this game
    """
    # CROSS is the first to play
    player1.new_game(CROSS)
    player2.new_game(NAUGHT)
    board.reset()

    finished = False
    while not finished:
        # In 2 steps : the CROSS player moves...
        result, finished = player1.move(board)

        if finished:
            if result == GameResult.DRAW:
                final_result = GameResult.DRAW
            else:
                final_result =  GameResult.CROSS_WIN
        else:
            # ... then the NAUGHT player moves
            result, finished = player2.move(board)
            if finished:
                if result == GameResult.DRAW:
                    final_result =  GameResult.DRAW
                else:
                    final_result =  GameResult.NAUGHT_WIN

    # If the players want to learn something from this game
    player1.final_result(final_result)
    player2.final_result(final_result)

    return final_result



## Let's define a `battle` function

def battle(p1: Player, p2: Player, num_games=10000, show=True):
    """
    Fully plays `num_games` (new) games between agent `p1` and agent `p2`
    NOTE : if you directly put `battle(NewPlayer1(), NewPlayer2())`,
    those players can no longer be accessed later,
    so what they have learned will be lost after the battle !
    """
    # Initializing the board
    board = Board()

    # Let's count the number of wins/draws
    draw_count = 0
    cross_count = 0
    naught_count = 0

    # For the duration of computation
    t0 = time()

    for _ in range(num_games):
        result = play_game(board, p1, p2)
        if result == GameResult.CROSS_WIN:
            cross_count += 1
        elif result == GameResult.NAUGHT_WIN:
            naught_count += 1
        else:
            draw_count += 1

    if show:
        print()

        print("Computation time : {}s\n".format(time()-t0))

        print("First player : {}".format(p1.name()))

        print("Second player : {}".format(p2.name()))

        print("After {} game we have : \ncross wins: {}, naught wins: {}, draws: {}".format(num_games, cross_count, naught_count, draw_count))

        print("Which gives percentages of : \ncross wins: {:.2%}, naught wins: {:.2%}, draws : {:.2%}".format(cross_count / num_games, naught_count / num_games, draw_count / num_games))

    else:
        return (cross_count / num_games, naught_count / num_games, draw_count / num_games)



## Generic printing function ...?



## Once we have enough players we will need a `rumble` function

def rumble(player_list, num_games=10000, name_list=None, show=True):
    """
    Tournament amongst the players of `players_list`
    Particular names can be given to the players with `names_list` in the format (player_index_in_`player_names`, new_name)
    Most of the code is for printing purposes
    """
    # Computation time
    t0 = time()

    # For every battle we need the proportion of draws and wins
    results = []
    for player1 in player_list:
        for player2 in player_list:
            p1 = player1.copy()
            p2 = player2.copy()
            p1_wins, p2_wins, draws = battle(p1, p2, num_games=num_games, show=False)
            # `results` puts draws at the end
            results.append([p1_wins, p2_wins, draws])

    # If we want to print the results
    if show:
        print()

        # Computation time
        print("Computation time : {}s\n".format(time()-t0))

        # We need to know the maximum length of player names to determine the length of the header
        player_names = []
        max_length = 0
        for player in player_list:
            name = player.name()
            player_names.append(name)
            # Update max_length if necessary
            if len(name) > max_length:
                max_length = len(name)
        if name_list != None:
            for index, name in name_list:
                player_names[index] = name
                # Update max_length if necessary
                if len(name) > max_length:
                    max_length = len(name)

        # The headers
        c1_header = "P1 vs P2"
        c2_header = "P1 Wins"
        c3_header = "P2 Wins"
        c4_header = "Draws"
        # So the length needed is, taking the middle ` - ` into account...
        c1_length = max(len(c1_header), 2*max_length + 3)
        # For the other columns : `.2%` makes a length <=7 string
        cx_length = max(len(max([c2_header, c3_header, c4_header], key=len)), 7)

        # Printing the headers
        print("|",
        format(c1_header, "<{}".format(c1_length)), "|",
        format(c2_header, "^{}".format(cx_length)), "|",
        format(c3_header, "^{}".format(cx_length)), "|",
        format(c4_header, "^{}".format(cx_length)), "|"
        )

        # Separator
        print((2+c1_length+3*(3+cx_length)+2)*"=")

        # Printing the results
        n = len(player_names)
        for i in range(n):
            for j in range(n):
                # The players
                versus = format(player_names[i], "<{}".format(max_length)) + " - " + format(player_names[j], "<{}".format(max_length))
                p1_wins, p2_wins, draws = results[i*n+j]
                # Changing into percentages
                # Duck-typing... :P
                p1_wins = format(p1_wins, ".2%")
                p2_wins = format(p2_wins, ".2%")
                draws = format(draws, ".2%")

                # Printing the row
                print("|",
                format(versus, "<{}".format(c1_length)), "|",
                format(p1_wins, ">{}".format(cx_length)), "|",
                format(p2_wins, ">{}".format(cx_length)), "|",
                format(draws, ">{}".format(cx_length)), "|"
                )

    else:
        return results



## Once we start examining reinforcement learning methods we will need to evaluate their performance:

def evaluate_players(p1: Player, p2: Player, games_per_battle=10, num_battles=100, show_step=True):
    """
    Gives the progression of the players after `num_battles` of `games_per_battle` games each
    Can serve as a traning function
    """
    p1_wins = []
    p2_wins = []
    draws = []

    # For printing
    previous = 0

    for i in range(num_battles):
        p1win, p2win, draw = battle(p1, p2, num_games=games_per_battle, show=False)
        p1_wins.append(p1win)
        p2_wins.append(p2win)
        draws.append(draw)
        # Shows every additional 10% completion
        if show_step:
            percent = int(100*(i+1)/num_battles)
            if percent % 10 == 0 and previous % 10 != 0:
                print("{}% of battles done".format(percent))
            previous = percent

    print("All battles over")

    # `battle` gives proportions
    return p1_wins, p2_wins, draws

def evolution_players(p1: Player, p2: Player, games_per_battle=10, num_battles=100, loc='best', show_step=True):
    """
    Plotting function
    """
    # X-axis : game number
    count = np.arange(0, games_per_battle*(num_battles+1), games_per_battle)

    # Y-axis : percentages
    p1_wins, p2_wins, draws = evaluate_players(p1, p2, games_per_battle=games_per_battle, num_battles=num_battles, show_step=True)

    p1_wins.insert(0, 0)
    p2_wins.insert(0, 0)
    draws.insert(0, 0)
    # Duck-typing... :P
    p1_wins = 100*np.array(p1_wins)
    p2_wins = 100*np.array(p2_wins)
    draws = 100*np.array(draws)

    plt.ylabel('Game outcomes in %')
    plt.xlabel('Game number')

    plt.step(count, p1_wins, 'g-', label=p1.name()+' as P1 wins')
    plt.step(count, p2_wins, 'r-', label=p2.name()+' as P2 wins')
    plt.step(count, draws, 'b-', label='Draw')
    # + `shadow=True` ...?
    plt.legend(loc=loc, fancybox=True, framealpha =0.7)

    plt.show()












## bokeh

# import numpy as np
# from bokeh.layouts import row
# from bokeh.models import ColumnDataSource, Slider, CustomJS
# from bokeh.plotting import Figure, show
#
# # Define data
# x = [x*0.05 for x in range(0, 500)]
# trigonometric_functions = {
#     '0': np.sin(x),
#     '1': np.cos(x),
#     '2': np.tan(x),
#     '3': np.arctan(x)}
# initial_function = '0'
#
# # Wrap the data in two ColumnDataSources
# source_visible = ColumnDataSource(data=dict(
#     x=x, y=trigonometric_functions[initial_function]))
# source_available = ColumnDataSource(data=trigonometric_functions)
#
# # Define plot elements
# plot = Figure(plot_width=400, plot_height=400)
# plot.line('x', 'y', source=source_visible, line_width=3, line_alpha=0.6)
# slider = Slider(title='Trigonometric function',
#                 value=int(initial_function),
#                 start=np.min([int(i) for i in trigonometric_functions.keys()]),
#                 end=np.max([int(i) for i in trigonometric_functions.keys()]),
#                 step=1)
#
# # Define CustomJS callback, which updates the plot based on selected function
# # by updating the source_visible ColumnDataSource.
# slider.callback = CustomJS(
#     args=dict(source_visible=source_visible,
#               source_available=source_available), code="""
#         var selected_function = cb_obj.value;
#         // Get the data from the data sources
#         var data_visible = source_visible.data;
#         var data_available = source_available.data;
#         // Change y-axis data according to the selected value
#         data_visible.y = data_available[selected_function];
#         // Update the plot
#         source_visible.change.emit();
#     """)
#
# layout = row(plot, slider)
# show(layout)

