# Let's correct the code and try running it again.
import random


def assign_people_to_game(df_people, people_per_game, number_of_games, remainder_processing):
    # Initialize games
    games = [[] for _ in range(number_of_games)]

    # Sort people based on previous_status_ok
    sorted_people = sorted(df_people, key=lambda x: x['previous_status_ok'])

    # Calculate total game slots and compare with total people
    total_slots = people_per_game * number_of_games
    total_people = len(sorted_people)
    remainder = total_people - total_slots

    # Assign people with priority (previous_status_ok=False) to games
    for person in sorted_people:
        if total_slots <= 0:
            break  # Stop if all slots are filled

        # Find the least filled game to add the person to
        min_filled_game = min(games, key=len)
        min_filled_game.append(person['person_id'])
        total_slots -= 1

    # Handle remainder
    if remainder > 0:
        # More people than game slots; do nothing as excess people are already excluded
        pass
    else:
        remainder = abs(remainder)  # Convert to positive for easier handling
        if remainder_processing == 'extend2':
            # Add extra people to the last game
            min_filled_game = min(games, key=len)
            min_filled_game.extend([person['person_id'] for person in sorted_people[:remainder]])
        elif remainder == 3 or remainder_processing == 'split':
            # Create a new game with 2 or 3 people
            games.append([person['person_id'] for person in sorted_people[:remainder]])
        else:
            # Add the remaining person to an existing game
            min_filled_game = min(games, key=len)
            min_filled_game.append(sorted_people[0]['person_id'])

    return games


# Test the function
test_people = [
    {'person_id': 1, 'previous_status_ok': True},
    {'person_id': 2, 'previous_status_ok': True},
    {'person_id': 3, 'previous_status_ok': False},
    {'person_id': 4, 'previous_status_ok': True},
    {'person_id': 5, 'previous_status_ok': False},
    {'person_id': 6, 'previous_status_ok': True},
]

result = assign_people_to_game(test_people, 2, 3, 'extend2')
print(result)
