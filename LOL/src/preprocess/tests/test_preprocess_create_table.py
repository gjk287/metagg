import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocess_create_table import preprocess_and_save


def main():
	preprocess_and_save('league')
	preprocess_and_save('betting_site')
	preprocess_and_save('bet_type', 'bet_type_special')
	preprocess_and_save('bet_type', 'bet_type_ou')
	preprocess_and_save('bet_type', 'bet_type_handicap')
	preprocess_and_save('bet_type', 'bet_type_both')




if __name__ == "__main__":
	main()