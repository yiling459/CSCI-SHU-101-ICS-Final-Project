from game_player_class import *

def main():
    import argparse
    parser = argparse.ArgumentParser(description='chat client argument')
    parser.add_argument('-d', type=str, default=None, help='server IP addr')
    args = parser.parse_args()

    player = Player(args)
    player.run_chat()

if __name__ == "__main__":
    main()