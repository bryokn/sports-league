from sqlalchemy.orm import sessionmaker
from models import Team, Coach, Player, Match, Venue, engine

Session = sessionmaker(bind=engine)
session = Session()

def add_team():
    team_name = input("Enter team name: ")
    coach_name = input("Enter coach name: ")
    coach_contact = input("Enter coach contact information: ")
    coach = Coach(name=coach_name, contact_info=coach_contact)
    team = Team(name=team_name, coach=coach)
    session.add(team)
    session.commit()
    print("Team added successfully!")

def add_player():
    player_name = input("Enter player name: ")
    player_age = int(input("Enter player age: "))
    player_position = input("Enter player position(s) separated by commas: ")
    player_contact = input("Enter player contact information: ")
    team_id = int(input("Enter team ID: "))
    team = session.query(Team).get(team_id)
    player = Player(name=player_name, age=player_age, position=player_position, contact_info=player_contact, team=team)
    session.add(player)
    session.commit()
    print("Player added successfully!")

#function to add coaches, matches, venues, etc.

def main():
    while True:
        print("\nGrassroots Hockey League Management System")
        print("1. Add Team")
        print("2. Add Player")
        print("3. Add Coach")
        print("4. Add Match")
        print("5. Add Venue")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_team()
        elif choice == "2":
            add_player()
        # Add more options for other functionalities
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
