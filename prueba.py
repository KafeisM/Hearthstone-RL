from hearthstone.enums import CardClass
from fireplace.game import Game
from fireplace.player import Player
from fireplace.utils import random_draft
from fireplace.exceptions import GameOver
import random


def get_valid_decks():
    """Create valid decks for both players."""
    card_classes = [
        CardClass.MAGE,
        CardClass.HUNTER,
        CardClass.PALADIN,
        CardClass.WARRIOR,
        CardClass.DRUID,
        CardClass.WARLOCK,
        CardClass.SHAMAN,
        CardClass.PRIEST,
        CardClass.ROGUE
    ]

    # Pick random classes for each player
    player1_class = random.choice(card_classes)
    player2_class = random.choice(card_classes)

    # Try to create decks with manually specified card collections if needed
    try:
        deck1 = random_draft(player1_class)
    except IndexError:
        # Fallback to predefined deck if random_draft fails
        deck1 = ["CS2_032", "CS2_033", "CS2_034", "CS2_172", "CS2_168",
                 "CS2_120", "CS3_001", "CS2_092", "CS2_022", "CS2_023",
                 "CS2_024", "CS2_025", "CS2_026", "CS2_027", "CS2_028",
                 "CS2_029", "CS2_030", "CS2_031", "CS1_042", "CS1_113",
                 "CS2_118", "CS2_119", "CS2_213", "CS2_188", "CS2_004",
                 "CS2_005", "CS2_007", "CS2_179", "CS2_117", "CS2_151"]

    try:
        deck2 = random_draft(player2_class)
    except IndexError:
        # Fallback to predefined deck if random_draft fails
        deck2 = ["CS2_032", "CS2_033", "CS2_034", "CS2_172", "CS2_168",
                 "CS2_120", "CS3_001", "CS2_092", "CS2_022", "CS2_023",
                 "CS2_024", "CS2_025", "CS2_026", "CS2_027", "CS2_028",
                 "CS2_029", "CS2_030", "CS2_031", "CS1_042", "CS1_113",
                 "CS2_118", "CS2_119", "CS2_213", "CS2_188", "CS2_004",
                 "CS2_005", "CS2_007", "CS2_179", "CS2_117", "CS2_151"]

    # Get hero cards for each class
    player1_hero = player1_class.default_hero
    player2_hero = player2_class.default_hero

    return deck1, deck2, player1_hero, player2_hero


def setup_game():
    """Initialize a game with valid decks and heroes."""
    deck1, deck2, hero1, hero2 = get_valid_decks()

    player1 = Player("Player1", deck1, hero1)
    player2 = Player("Player2", deck2, hero2)

    game = Game(players=(player1, player2))
    game.start()

    # Skip mulligan for now
    for player in game.players:
        player.choice = None

    return game


def play_turn(game):
    """Play a single turn."""
    player = game.current_player

    # Get playable cards
    playable_cards = [card for card in player.hand if card.is_playable()]

    if playable_cards:
        # Choose a random card to play
        card = random.choice(playable_cards)
        print(f"{player} plays {card}")

        # Choose a target if required
        if card.requires_target():
            targets = card.targets
            if targets:
                target = random.choice(targets)
                card.play(target=target)
            else:
                # Can't play this card without a target
                card.play()
        else:
            card.play()
    else:
        # If no cards can be played, attack with what we have
        for character in player.characters:
            if character.can_attack():
                targets = character.targets
                if targets:
                    target = random.choice(targets)
                    print(f"{player} attacks {target} with {character}")
                    character.attack(target)


def simulate_game():
    """Play a complete game and return the result."""
    game = setup_game()

    try:
        for _ in range(100):  # Limit to 100 turns to prevent infinite games
            play_turn(game)
            game.end_turn()
    except GameOver:
        # Game has ended
        winner = game.player1 if game.player1.playstate == 4 else game.player2
        print(f"Game ended. {winner} wins!")
        return winner.name

    print("Game ended due to turn limit.")
    return "Draw"


# Run the simulation
if __name__ == "__main__":
    game_result = simulate_game()
    print(f"Final result: {game_result}")