import csv
from util import Node, QueueFrontier

class Degree:
    
    def __init__(self, directory):
        # Maps names to a set of corresponding persons_id
        self.names = {}
        # Maps persons_id to a dictionary of: name, birth, movies (a set of movie_ids)
        self.people = {}
        # Maps movies_ids to a dictionary of: title, year, stars (a set of person_ids)
        self.movies = {}

        """
        Load data from csv file into memory
        """   
        print("Loading Data...")     
        # Load people
        with open(f"{directory}/people.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.people[row["id"]] = {
                    "name": row["name"],
                    "birth": row["birth"],
                    "movies": set()
                }
                if row["name"].lower() not in self.names:
                    self.names[row["name"].lower()] = {row["id"]}
                else:
                    self.names[row["name"].lower()].add({row["id"]})
        # Load Movies
        with open(f"{directory}/movies.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.movies[row["id"]] = {
                    "title": row["title"],
                    "year": row["year"],
                    "stars": set()
                }
        # Load Stars
        with open(f"{directory}/stars.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    self.people[row["person_id"]]["movies"].add(row["movie_id"])
                    self.movies[row["movie_id"]]["stars"].add(row["person_id"])
                except KeyError:
                    pass
        print("Data Loaded...")
                
    def person_id_for_name(self, name):
        person_ids = list(self.names.get(name.lower(), set()))
        if len(person_ids) == 0:
            return None
        elif len(person_ids) > 1:
            print(f"Which '{name}'?")
            for person_id in person_ids:
                person = self.people[person_id]
                name = person["name"]
                birth = person["birth"]
                print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
            try:
                person_id = input("Intended Person ID: ")
                if person_id in person_ids:
                    return person_id
            except ValueError:
                pass
        else:
            return person_ids[0]

    def neighbors_for_person(self,person_id):
        movie_ids = self.people[person_id]["movies"]
        neighbors = set()
        for movie_id in movie_ids:
            for person_id in self.movies[movie_id]["stars"]:
                neighbors.add((movie_id, person_id))
        return neighbors
    
    def shortest_path(self, source, target):
        start = Node(state=source, parent=None, action=None)
        frontier = QueueFrontier()
        frontier.add(start)
        
        explored_set = set()
        
        while True:
            
            if frontier.empty():
                return None
            else:
                removed_node = frontier.remove()
                
                if removed_node.state == target:
                    solution = []
                    while removed_node.parent is not None:
                        solution.append((removed_node.action, removed_node.state))
                        removed_node = removed_node.parent
                    solution.reverse()
                    return solution
            for action, state in self.neighbors_for_person(removed_node.state):
                if not frontier.contain_state(state) and state not in explored_set:
                    child = Node(state=state, parent=removed_node, action=action)
                    frontier.add(child)
                
    def people_path(self, degrees, path):
        for i in range(degrees):
            person1 = self.people[path[i][1]]["name"]
            person2 = self.people[path[i+1][1]]["name"]
            movie = self.movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")