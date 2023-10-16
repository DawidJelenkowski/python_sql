#
#
# Scope of work:
# - create an interface that offers the user a menu of 5 choices:
# -- 1. Add a box type
# -- 2. Show box types
# -- 3. Load box to container
# -- 4. Show containers
# -- 5. Summary Report
# -- X. Close

# - for now, each choice should print a simple statement indicating
# the choice, eg "Choice 2 selected"

# - the menu should be offered continuously until the user chooses X,
# in which case, the interface greets the user and the
# program terminates

# import helper functions
from database import create_database_and_tables, add_box, get_all_boxes, get_box, get_container, add_box_to_container, seed_data, get_all_containers, get_all_freight, get_config


from tabulate import tabulate


def retrive_numeric_input(called):
  input_ok = False
  
  while not input_ok:
    n = input(f"\nPlease enter {called}: ")
    
    # Validates whether the input is numeric
    try:
      n = float(n)
      input_ok = True
    except ValueError:
      print("Please provide a numeric input")
  
  return n


# database helper that returns all the box types in the database
def display_box_types():
  boxes = get_all_boxes(connection)
  
  print("\n" + tabulate(boxes,
    headers=["boxes_id", "box_name", "height", "width", "length"],
    tablefmt="psql") + "\n")


# database helper that adds boxes to the database  
def add_box_menu():
  box_name = input("\nPlease enter a name for the box: ")
  
  box_height = retrive_numeric_input(called="the box's height in meters")
  box_width = retrive_numeric_input(called="the box's width in meters")
  box_length = retrive_numeric_input(called="the box's length in meters")
  
  add_box(connection, (box_name, box_height, box_width, box_length))
    


def load_box_menu():
  # ask for the box name
  n = input("Enter the name of the box: ")
  
  # validate whether the box exists
  box = get_box(connection, by_name=n)
  
  if not box:
    print("\nA box by that name could not be found. \n")
  else:
    box_dims = box.height * box.width * box.length
    container_id = input("Enter the id of the container to load the box to: ")
  
    container = get_container(connection, container_id)
    
    if container is None or (container.occupied_volume + box_dims <= float(config.get('MAX_CONTAINER_STORAGE'))):
      add_box_to_container(connection, box.id, container_id)
    else:
      print(f"Container {container_id} does not have enough space for box {box.id}.")
      
      
def display_containers():
    containers = get_all_containers(connection)
    print("\n" + tabulate(containers, headers=["container_id", "occupied_volume"], tablefmt="fancy_grid") + "\n")


def display_summary():
  freight = get_all_freight(connection)
  # get all containers or return a tuple, without it it would return None
  containers = get_all_containers(connection) or ()
  
  nr_containers = len(containers)
  
  if not nr_containers:
    print("\n There is no contracted freight currently.\n")
    return
  
  contracted_volume = sum([c.occupied_volume for c in containers])
  revenue = round(contracted_volume * float(config.get('CUBIC_METRE_CHARGEOUT')), 2)
  
  cost = nr_containers * float(config.get('COST_PER_CONTAINER'))
  
  print(f"\nContracted {len(freight)} box(es) in {len(containers)} container(s).")
  print(f"\nThe total contracted volume is {contracted_volume} m3.")
  print(f"\nEstimated cost of carrying this freight is ${cost}")
  print(f"\nEstimated Profit/Lost: ${round(revenue - cost, 2)}\n.")
  
  
def main_menu():
  print("Welcome to Freight Manager!\n")

  n = "no_op"

  while n.upper() != 'X':
    # display menu
    print("1. Add a box type\n2. Show box types\n3. Load box to container"
          "\n4. Show container\n5. Summary Report\nX. Close\n")
    
    n = input("Your choice: ")
    
    if n == "1":
      add_box_menu()
    elif n == "2":
      display_box_types()
    elif n == "3":
      load_box_menu()
    elif n == "4":
      display_containers()
    elif n == "5":
      display_summary()

  print("\nGoodbye!")


if __name__ == "__main__":
  connection = create_database_and_tables(filename="freight_prod.db")
  seed_data(connection)
  config = get_config(connection)
  main_menu()