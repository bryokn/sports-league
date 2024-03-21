# Grassroots Hockey League
This is a CLI application built with Python and SQLAlchemy to manage the Kipchebor Grassroots Hockey League. It allows administrators to add teams, players, coaches, matches, and venues, as well as assign team captains. Users can view teams, the league table, previous match results, and available venues.

## Features
 **Admin Interface**
- Add teams, players, coaches,matches and venues
- Assign team captains
- View all registered players
- Edit coaches, players and venues

**User Interface**
- View teams and their players
- View the league table
- View previous match results
- Check available venues and their schedules

## Getting started
1. Clone the repository
```
git clone https://github.com/bryokn/sports-league.git
```
2. Navigate to the project directory:
```
cd sports-league
```
3. Create a virtual environment and activate it (optional but recommended)
```
pipenv shell
```
4. Install the required dependencies:
```
pip install sqlalchemy
```
5. Run the application:
```
python3 main-cli.py
```
6. Follow the on-screen intructions to navigate through the various fetures of the application.

## Database
The application uses SQLite as the database engine, and the database file (`hockey.db`) will be created automatically in the project directory when you run the application for the first time.
## Models
The application uses the following models:

- `Team`: Represents a hockey team with attributes such as name, coach, and players.
- `Coach`: Represents a coach with attributes such as name and contact information.
- `Player`: Represents a player with attributes such as name, age, position, and contact information.
- `TeamCaptain`: Represents the captain of a team, linking a player to a team.
- `Match`: Represents a hockey match with attributes such as date, time, venue, home team, away team, and scores.
- `Venue`: Represents a venue with attributes such as name, location, and availability schedule.
## Contributions
Contributions are welcome! If you find any issues or want to add new features, please open an issue or submit a pull request.
## LICENSE
This project is licensed under the MIT License.
## Author
This application is built and maintained by (c) 2024 Brian Kipkirui. bryokn@gmail.com