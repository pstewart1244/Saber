from os.path import dirname, join

import random
import math

from textx import metamodel_from_file
from textx.export import metamodel_export, model_export

#def player_creation_processor(p):
    # Create Player object
class Player:
    def __init__(self, name, BA, OBP, SLG):
        self.name = name
        self.BA = BA
        self.OBP = OBP
        self.SLG = SLG
        self.OPS = OBP+SLG

    def update(self,newBA,newOBP,newSLG):
        self.BA = newBA
        self.OBP = newOBP
        self.SLG = newSLG
        self.OPS = newOBP+newSLG

    #Player's string representation
    def __str__(self):
        return f"{self.name}"
    #separate print method that includes stats
    def print_with_stats(self):
        return f"{self.name} (BA: {self.BA:.3f}  OBP: {self.OBP:.3f}  SLG: {self.SLG:.3f})"
    #additional print method for one stat
    def print_stat(self, stat):
        match stat:
            case 'BA':
                return f"{self.name} Batting Average: {self.BA:.3f}"
            case 'OBP':
                return f"{self.name} On-Base Pct: {self.OBP:.3f}"
            case 'SLG':
                return f"{self.name} Slugging Pct:{self.SLG:.3f}"
            case 'OPS':
                return f"{self.name} OPS: {self.OPS:.3f}"
        raise Exception("Can't print stat {stat}")
            




class Team:
    def __init__(self, name, roster):
        self.name = name
        self.roster = roster
        #creates a printable version of the team roster
        self.rosterNames = "["
        for n in roster:
            self.rosterNames += n.__str__()+", "
        self.rosterNames += "endMarker"
        self.rosterNames = self.rosterNames.replace(", endMarker", "]")
        
        #team stats (inaccessible)
        self.BA = 0
        self.OBP = 0
        self.SLG = 0
        self.OPS = 0

        self.calculate_stats()

    #averages every player's stats into the team's figures
    def calculate_stats(self):
        playercount = 0
        for player in self.roster:
            playercount += 1
            self.BA += player.BA
            self.OBP += player.OBP
            self.SLG += player.SLG
        self.BA = self.BA/playercount
        self.OBP = self.OBP/playercount
        self.SLG = self.SLG/playercount
        self.OPS = self.OBP+self.SLG

    #team's string representation
    def __str__(self):
        return f"{self.name}"
    #separate print method that includes team's stats
    def print_with_stats(self):
        return f"{self.name}\nPlayers: {self.rosterNames}\nTeam BA: {self.BA:.3f}  Team OBP: {self.OBP:.3f}  Team SLG: {self.SLG:.3f}"
    #additional print method for one stat
    def print_stat(self, stat):
        match stat:
            case 'BA':
                return f"{self.name} Batting Average: {self.BA:.3f}"
            case 'OBP':
                return f"{self.name} On-Base Pct: {self.OBP:.3f}"
            case 'SLG':
                return f"{self.name} Slugging Pct: {self.SLG:.3f}"
            case 'OPS':
                return f"{self.name} OPS: {self.OPS:.3f}"
            case 'roster':
                return f"{self.name} Roster: {self.rosterNames}"
        raise Exception("Can't print stat {stat}")
    


#Uses normal distributions centered at player/team values to project season
class Simulation:
    #weights and deviations that fine tune the projection formula
    BA_WEIGHT = 28.99956433
    OBP_WEIGHT = 78.61409856
    SLG_WEIGHT = 38.91778004
    OPS_WEIGHT = 54.83096786

    BA_STD_DEV = 0.01082923
    OBP_STD_DEV = 0.012311738
    SLG_STD_DEV = 0.024246076
    #scrapped value
    #OPS_STD_DEV = 0.035361373

    def __init__(self, name, var):
        self.name = name
        self.var = var
        #season projection algorithm for players
        if isinstance(var, Player):
            self.AB = random.randint(500,600)
            self.hits = round(random.gauss(var.BA, self.BA_STD_DEV)*self.AB)
            self.BA = self.hits/self.AB
            self.OBP = random.gauss(var.OBP, self.OBP_STD_DEV)
            self.SLG = random.gauss(var.SLG, self.SLG_STD_DEV)
            self.OPS = self.OBP+self.SLG
            
        #season projection algorithm for teams
        else:  
            self.BA = random.gauss(var.BA, self.BA_STD_DEV)
            self.OBP = random.gauss(var.OBP, self.OBP_STD_DEV)
            self.SLG = random.gauss(var.SLG, self.SLG_STD_DEV)
            self.OPS = self.OBP+self.SLG
            #more complex logarithmic formula calculates wins
            self.wins = round(self.BA_WEIGHT*math.log(self.BA)+self.OBP_WEIGHT*math.log(self.OBP)+self.SLG_WEIGHT*math.log(self.SLG)+self.OPS_WEIGHT*math.log(self.OPS))+264
            #Accounts for the algorithm being thrown off by unrealistic stats
            if self.wins > 162:
                self.wins = 162
            if self.wins < 0:
                self.wins = 0

    #simulation's string representation
    def __str__(self):
        return f"{self.name}"
    #separate string method that includes simulation's info
    def print_with_stats(self):
        prnt = f"{self.name}"
        if isinstance(self.var, Player):
            prnt += f"\nBA: {self.BA:.3f}  OBP: {self.OBP:.3f}  SLG: {self.SLG:.3f}  OPS: {self.OPS:.3f}"
            prnt += f"\nAt-Bats: {self.AB}  Hits: {self.hits}"
        else:
            prnt += f"\nTeam BA: {self.BA:.3f}  Team OBP: {self.OBP:.3f}  Team SLG: {self.SLG:.3f} Team OPS: {self.OPS:.3f}"
            prnt += f"\nWins: {self.wins}"
        return prnt
    #additional print method for one stat
    def print_stat(self, stat):
        match stat:
            case 'BA':
                return f"{self.name} Batting Average: {self.BA:.3f}"
            case 'OBP':
                return f"{self.name} On-Base Pct: {self.OBP:.3f}"
            case 'SLG':
                return f"{self.name} Slugging Pct: {self.SLG:.3f}"
            case 'OPS':
                return f"{self.name} OPS: {self.OPS:.3f}"
            case 'hits':
                if isinstance(self.var, Player):
                    return f"{self.name} hits: {self.hits}"
                else:
                    raise Exception("Hits not applicable for teams.")
            case 'at_bats':
                if isinstance(self.var, Player):
                    return f"{self.name} At-Bats: {self.hits}"
                else:
                    raise Exception("At-bats not applicable for teams.")
            case 'wins':
                if isinstance(self.var, Team):
                    return f"{self.name} wins: {self.wins}"
                else:
                    raise Exception("Wins not applicable for players.")
        raise Exception("Can't print stat {stat}")



class Saber:

    def __init__(self):
        self.player_list = {}
        self.team_list = {}
        self.simulation_list = {}

    def __str__(self):
        return f"Players: {self.player_list}\n\nTeams: {self.team_list}\n\nSimulations: {self.simulation_list}\n"
    
    def interpret(self, model):
        print("")
        for c in model.statements:
            #parses PlayerCreation statements and creates player variable
            if c.__class__.__name__ == "PlayerCreation":
                name = c.name
                if name in self.player_list or name in self.team_list or name in self.simulation_list:
                    raise Exception(f"variable '{name}' already exists.")
                player = Player(name, c.ba, c.obp, c.slg)
                self.player_list[name] = player
                #outputs player
                print(f"Created player: {player.print_with_stats()}")

            #parses TeamCreation statements and creates team variable
            elif c.__class__.__name__ == "TeamCreation":
                name = c.name
                if name in self.player_list or name in self.team_list or name in self.simulation_list:
                    raise Exception(f"variable '{name}' already exists.")          
                #'players' is a list to be filled with the players passed in the
                #teamCreation statement, then passed to Team() to be instantiated
                players = []
                #uses parsed player names to pull from global Player list
                for playerName in c.roster:
                    if playerName in self.player_list:
                        players.append(self.player_list[playerName])
                    else:
                        raise Exception(f"player '{playerName}' not found.")
                #creates team variable
                team = Team(name, players)
                self.team_list[name] = team
                #outputs team
                print(f"Created team: {team.print_with_stats()}\n")

            #parses SimulationCreation statement and creates simulation variable
            elif c.__class__.__name__ == "SimulationCreation":
                name = c.name
                if name in self.player_list or name in self.team_list or name in self.simulation_list:
                    raise Exception(f"variable '{name}' already exists.")
                #passes 'var' keyword into the simulation method as the correct data type
                if c.var in self.player_list:
                    simulation = Simulation(name, self.player_list[c.var])
                elif c.var in self.team_list:
                    simulation = Simulation(name, self.team_list[c.var])
                else:
                    raise Exception(f"Can only simulate seasons for players or teams.")
                self.simulation_list[name] = simulation
                #outputs simulated season
                print(f"Projected season for {c.var}:\nSeason name: {simulation.print_with_stats()}\n")
            
            #parses update method
            elif c.__class__.__name__ == "Update":
                if c.name in self.player_list:
                    player = self.player_list[c.name]
                    player.update(c.ba,c.obp,c.slg)
                    print(f"Updated {player.print_with_stats()}")
                else:
                    raise Exception(f"Player {c.name} not recognized.")
                
            #Change saber.tx Print statement's stat to an =ID, then parse it manually here 
            elif c.__class__.__name__ == "Print":
                if c.name in self.player_list:
                    player = self.player_list[c.name]
                    print(f"{player.print_stat(c.stat)}")
                elif c.name in self.team_list:
                    team = self.team_list
                    print(f"{team.print_stat(c.stat)}")
                elif c.name in self.simulation_list:
                    simulation = self.simulation_list
                    print(f"{simulation.print_stat(c.stat)}")
                

                




def main(debug=False):

    this_folder = dirname(__file__)

    saber_mm = metamodel_from_file(join(this_folder, 'saber.tx'), classes=[Player,Team,Simulation], debug=False)
    metamodel_export(saber_mm, join(this_folder, 'saber_meta.dot'))

    # Register object processor for PlayerCreation
    #saber_mm.register_obj_processors({'PlayerCreation': player_creation_processor})

    saber_model = saber_mm.model_from_file(join(this_folder, 'program.sbr'))
    model_export(saber_model, join(this_folder, 'program.dot'))

    saber = Saber()
    saber.interpret(saber_model)


if __name__ == "__main__":
    main()
