from degree import Degree
import sys

def main():
    if len(sys.argv) > 2 or len(sys.argv) < 2:
        sys.exit("Usage: Python3 main.py [directory]")
    directory = sys.argv[1]
    # Load data from files to memory
    degree = Degree(directory)
    
    source = degree.person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person Not Found.")
    target = degree.person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person Not Found.")
    
    path = degree.shortest_path(source=source, target=target)
    
    if path is None:
        print("No Connection.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of seperation")
        path = [(None, source)] + path
        degree.people_path(degrees=degrees, path=path)
    
    


if __name__ == "__main__":
    main()