import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src\\preprocess\\tests'))
from test_preprocess_gamepedia import preprocess_and_save as pas_gamepedia


def main():
	# preprocess gamepedia data
	pas_gamepedia('game_schedule')
	pas_gamepedia('match_history_url')




if __name__ == "__main__":
	main()