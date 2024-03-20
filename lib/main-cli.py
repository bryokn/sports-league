# importing necessary modules
from sqlalchemy.orm import sessionmaker, joinedload
from models.models import Team, Coach, Player, Match, Venue, TeamCaptain
from models.models import engine
from datetime import datetime
                 
Session = sessionmaker(bind=engine) #session class
session = Session() #session instance

#add new team function
def add_team():
    team_name = input("Enter team name: ")
    coach_name = input("Enter coach name: ")
    coach_contact = input("Enter coach contact information: ")
    coach = Coach(name=coach_name, contact_info=coach_contact)
    team = Team(name=team_name, coach=coach)
    session.add(team)
    session.commit()
    print("Team added successfully!")

#add player to team function
def add_player():
    player_name = input("Enter player name: ")
    player_age = int(input("Enter player age: "))
    player_position = input("Enter player position(s) separated by commas: ")
    player_contact = input("Enter player contact information: ")
    team_id = int(input("Enter team ID: "))
    team = session.get(Team, team_id)
    player = Player(name=player_name, age=player_age, position=player_position, contact_info=player_contact, team=team)
    session.add(player)
    session.commit()
    print("Player added successfully!")

#add a new coach function
def add_coach():
    coach_name = input("Enter coach name: ")
    coach_contact = input(" Enter coach contact information: ")
    coach = Coach(name=coach_name, contact_info=coach_contact)
    session.add(coach)
    session.commit()
    print("Coach added successfully!")
    
#add match function
def add_match():
    #manually input match details
    date_time_str = input("Enter match date and time (YYYY-MM-DD HH:MM):")
    date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M") # Converting the input string to a datetime object
    venue_id = int(input("Enter venue ID: "))
    home_team_id = int(input("Enter home team ID: "))
    away_team_id = int(input("Enter away team ID: "))
    home_team_score = int(input("Enter home team score: "))
    away_team_score = int(input("Enter away team score: "))
    match = Match(date_time=date_time, venue_id=venue_id, home_team_id=home_team_id, away_team_id=away_team_id,
                  home_team_score=home_team_score, away_team_score=away_team_score)
    session.add(match)
    session.commit()
    print("Match added successfully!")

#add new venue function
def add_venue():
    venue_name = input("Enter venue name: ")
    location = input("Enter venue location: ")
    availability_schedule = input("Enter venue availability schedule: ")
    venue = Venue(name=venue_name, location=location, availability_schedule=availability_schedule)
    session.add(venue)
    session.commit()
    print("Venue added successfully!")
#assigning captain to teams   
def assign_team_captain():
    team_id = int(input("Enter team ID: "))
    player_id = int(input("Enter player ID: "))
    team = session.get(Team, team_id)
    player = session.get(Player, player_id)
    if team and player and player in team.players:
        captain = TeamCaptain(player=player, team_id = team_id)
        session.add(captain)
        session.commit()
        print(f"{player.name} has been assigned as the Captain of {team.name}.")
    else:
        print("Invalid Team or Player ID, or the player is not part of this team.")

#Show team captains function
def show_team_captains():
    captains = session.query(TeamCaptain).join(Player).join(Team).all()
    if captains:
        print("Team Captains:")
        for captain in captains:
            print(f"Team: {captain.player.team.name}, Captain: {captain.player.name} \nContact: {captain.player.contact_info}\n")
    else:
        print("No team captains found.")
# View all players function        
def view_all_players():
    teams = session.query(Team).options(joinedload(Team.players)).all()
    if teams:
        print("Players: \n")
        for team in teams:
            print(f"Team: {team.name}")
            if team.players:
                for player in team.players:
                    print(f" Player ID: {player.id} \nName: {player.name}, {player.age}, Position: {player.position}\n")
            else:
                print("No players registered for this team.")
            print()
    else:
        print("No teams found!!")

#view teams and their players function        
def view_teams():
    teams = session.query(Team).all()
    if teams:
        print("Teams:\n")
        for team in teams:
            print(f"Team ID: {team.id} \nTeam Name: {team.name} \nCoach: {team.coach.name}\n \n")
        team_choice = input("\nEnter the Team ID to view players (or 'Q' to go back):")
        if team_choice.lower() == 'q':
            return
        else:
            try:
                team_id = int(team_choice)
                team = session.get(Team, team_id)
                #view players in registered in which teams
                if team:
                    print(f"\nPlayers for {team.name}:")
                    captain = session.query(TeamCaptain).join(Player).filter(TeamCaptain.team_id == team_id).first()
                    for player in team.players:
                        if captain and player.id == captain.player_id: # checks if the player is the team captain
                            print(f"\nPlayer ID: {player.id}")
                            print(f"Name: {player.name} - TEAM CAPTAIN")
                            print(f"Age: {player.age}")
                            print(f"Position(s): {player.position}")
                        else:
                            print(f"\nPlayer ID: {player.id}")
                            print(f"Name: {player.name}")
                            print(f"Age: {player.age}")
                            print(f"Position(s): {player.position}")
                        #print(f"Team Captain: {captain.player.name}")
                else:
                    print("Invalid Team ID!!")
                    
            except ValueError:
                print("Invalid input. Please enter a valid Team ID or 'Q' to go back.")
    else:
        print("No teams found!")

#View league table function
def view_league_table():
    teams = session.query(Team).options(
        joinedload(Team.home_matches, Match.home_team),
        joinedload(Team.away_matches, Match.away_team)
    ).all() # load teams and their associated home and away matches

    if teams:
        table = []
        for team in teams:
            home_wins = sum(1 for match in team.home_matches if match.home_team_score > match.away_team_score) #calculate home wins
            home_draws = sum(1 for match in team.home_matches if match.home_team_score == match.away_team_score) #calculate home draws
            away_wins = sum(1 for match in team.away_matches if match.away_team_score > match.home_team_score) #calculate away wins
            away_draws = sum(1 for match in team.away_matches if match.away_team_score == match.home_team_score) #calculate away draws
            points = (home_wins + away_wins) * 3 + home_draws + away_draws # calculate total points
            goals_scored = sum(match.home_team_score for match in team.home_matches) + sum(match.away_team_score for match in team.away_matches) #calculaet goals scored
            goals_conceded = sum(match.away_team_score for match in team.home_matches) + sum(match.home_team_score for match in team.away_matches) #calculate goals conceded
            goal_difference = goals_scored - goals_conceded #goal difference
            table.append((team.name, points, goal_difference, goals_scored, goals_conceded)) #adds stats to table

        print("League Table 📋 \n")
        print("{:20} {:5} {:5} {:5} {:5}".format("Team", "Pts", "GD", "GF", "GA")) #table header
        table.sort(key=lambda x: (-x[1], -x[2], -x[3], x[0])) #sorts table on points, GD, GS and team name
        for team_name, points, goal_difference, goals_scored, goals_conceded in table:
            print("{:20} {:5} {:5} {:5} {:5}".format(team_name, points, goal_difference, goals_scored, goals_conceded)) #print table rows
    else:
        print("No teams found!!")
#view previous matches function
def view_previous_matches():
    matches = session.query(Match).options(
        joinedload(Match.home_team), joinedload(Match.away_team)).all()
    if not matches:
        print("No previous matches found!!")
    else:
        for match in matches:
            print(f"\nDate: {match.date_time}\nHome Team: {match.home_team.name} ({match.home_team_score}🏑) vs Away Team: {match.away_team.name} ({match.away_team_score}🏑) \nVenue: {match.venue.name}")

def view_venues():
    venues = session.query(Venue).all()
    if venues:
        print("\n🏟️  Available Venues:  🏟️\n")
        for venue in venues:
            print(f"🏟️ Venue ID: {venue.id}")
            print(f"Name: {venue.name}")
            print(f"Location: {venue.location}")
            print(f"Availability: {venue.availability_schedule}")
            print()
    else:
        print("No Venues Found!!")
#function to change/edit coaches info
def edit_coaches():
    coaches = session.query(Coach).all()
    if coaches:
        print("Coaches:")
        for coach in coaches:
            print(f"ID: {coach.id}, Name: {coach.name}, Contact {coach.contact_info}")
        coach_id = int(input("\nEnter the coach ID to edit:"))
        coach = session.get(Coach, coach_id)
        if coach:
            new_name = input(f"Enter the new name (current: {coach.name}): ")
            new_contact = input(f"Enter the new contact information (current: {coach.contact_info}):")
            if new_name:
                coach.name = new_name
            if new_contact:
                coach.contact_info = new_contact
            session.commit()
            print("\nCoach information updated successfully.")
        else:
            print("Invalid Coach ID!!")
    else:
        print("No coaches found!!")
      
#function to edit players and allows team switching
def edit_players():
    players = session.query(Player).all()
    if players: #print list of all registered players 
        print("Players:\n")
        for player in players:
            print(f"ID: {player.id}, Name: {player.name}, Age: {player.age}, Position(s): {player.position}, Team: {player.team.name}")
        player_id = int(input("Enter the player ID to edit: "))
        player = session.get(Player, player_id)
        if player: #update player data with new info
            new_name = input(f"Enter the new name (current: {player.name}): ")
            new_age = input(f"Enter the new age (current: {player.age}): ")
            new_position = input(f"Enter the new position(s) separated by commas (current: {player.position}): ")
            new_contact = input(f"Enter the new contact information (current: {player.contact_info}): ")
            switch_team = input(f"Is the player switching teams? (y/n) (current team: {player.team.name}): ") #ask if player is switching teams
            if new_name:
                player.name = new_name
            if new_age:
                player.age = int(new_age)
            if new_position:
                player.position = new_position
            if new_contact:
                player.contact_info = new_contact
            #if player is switching teams, prompt for new team ID
            if switch_team.lower() == 'y':
                team_id = int(input("Enter the new team ID: "))
                new_team = session.get(Team, team_id)
                if new_team:
                    player.team = new_team #update player info and print confirming message
                    print(f"\n{player.name} has been moved to {new_team.name}!!")
                else:
                    print("Invalid team ID.")
            session.commit() #commit changes to db and show success message
            print("Player information updated successfully.")
        else:
            print("Invalid player ID.")
    else:
        print("No players found.")


def edit_venues():
    pass

#admin interface to add players, teams, coaches, matches, venues and show team captains
def admin_interface():
    while True:
        print("🏑 Kipchebor Grassroots Hockey League 🏑\n")
        print("Admin Roles 🛡️")
        print("\n1. Add Team")
        print("2. Add Player")
        print("3. Add Coach")
        print("4. Add Match")
        print("5. Add Venue")
        print("6. Assign Team Captains")
        print("7. Show Team Captains")
        print("8. View all registered players")
        print("\n EDIT MODE")
        print("9. Edit coaches")
        print("10. Edit Players")
        print("11. Edit Venues\n")
        print("0. Go Back")
        admin_choice = input("\nEnter your choice: ")
        if admin_choice == "1":
            add_team()
        elif admin_choice == "2":
            add_player()
        elif admin_choice == "3":
            add_coach()
        elif admin_choice == "4":
            add_match()
        elif admin_choice == "5":
            add_venue()
        elif admin_choice == "6":
            assign_team_captain()
        elif admin_choice == "7":
            show_team_captains()
            input("\n Press any key to go back to the previous menu...\n")
        elif admin_choice == "8":
            view_all_players()
            input("\n Press any key to go back to the previous menu...\n")
        elif admin_choice == "9":
            edit_coaches()
        elif admin_choice == "10":
            edit_players()
        elif admin_choice == "11":
            edit_venues()
        elif admin_choice == "0":
            print("Exiting admin interface...")
            break
        else:
            print("Invalid choice. Please try again.")

#Main function to manage main menu
def main():
    while True:
        print("\n🏑 Kipchebor Grassroots Hockey League 🏑")
        print("\n1. Admin Roles 🛡️")
        print("2. View Teams")
        print("3. View League Table 📋")
        print("4. View Previous Match Results")
        print("5. Check Venues and Availability 🏟️")
        print("0. Exit")
        choice = input("\nEnter your choice: ")
        if choice == "1":
            admin_interface()
        elif choice == "2":
            view_teams()
            input("\n Press any key to go back to the previous menu...\n")
        elif choice == "3":
            view_league_table()
            input("\n Press any key to go back to the previous menu...\n")
        elif choice == "4":
            view_previous_matches()
            input("\n Press any key to go back to the previous menu...\n")
        elif choice == "5":
            view_venues()
            input("\n Press any key to go back to the previous menu...\n")
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again")
        
#Entry point of the system
if __name__ == "__main__":
    main()
