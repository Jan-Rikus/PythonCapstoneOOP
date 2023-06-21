# COMPULSORY TASK: CAPSTONE PROJECT III

# Importing relevant modules
from tabulate import tabulate
import pyinputplus as pyip


# _________________________________________________
# NOTE:
# All shoe prices/costs are converted to integers
# as presented in original text document
# for uniformity
# _________________________________________________

# ========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        return f"{self.country}, {self.code}, {self.product}, {self.cost}, {self.quantity}"


# =============Shoe list===========
shoe_list = []


# ==========Functions outside the class==============
def table_display(list_name, table_list):
    """This function will display the catalogue
       in table format"""

    headers = [
        '\x1B[1mIndex\x1B[0m',
        '\x1B[1mCountry\x1B[0m',
        '\x1B[1mCode\x1B[0m',
        '\x1B[1mProduct\x1B[0m',
        '\x1B[1mCost (ZAR)\x1B[0m',
        '\x1B[1mQuantity\x1B[0m'
    ]

    print("\n\x1B[1mStock Catalogue\x1B[0m")
    print(tabulate(table_list, headers=headers, tablefmt='psql'))

    return None


def read_shoes_data(list_name):
    """This function will read in the shoe data from the 'inventory.txt' file,
       create a shoe object/instance and append to the 'shoe' list."""

    with open('inventory.txt', 'r') as file:

        try:
            next(file)  # Skip the first line ('How to skip the 1st line' - CodingDeeply.com)

            for line in file:
                # Strip \n character and splitting line on the delimiter (,)
                data = line.strip().split(',')

                # Extract data from list and assign to variables
                country = data[0]
                code = data[1]
                product = data[2]
                cost = float(data[3])
                quantity = int(data[4])

                # Creating new Shoe object/instance
                shoe = Shoe(country, code, product, cost, quantity)

                # Appending to shoe_list
                list_name.append(shoe)

        except FileNotFoundError as error:
            print("The file you are looking for does not exist!")
            print(error)

        return None


def capture_shoes(list_name):
    """This function will capture new shoe data, create
       a shoe object/instance and append to 'shoe' list"""

    country = input('Country: ')
    code = input('Shoe Code: ')
    product = input('Product name: ')
    cost = float(input('Price in ZAR (R): '))
    quantity = int(input('Stock Quantity: '))

    # Creating new Shoe object/instance
    shoe = Shoe(country, code, product, cost, quantity)

    # Appending to shoe_list
    list_name.append(shoe)

    # Adding new added shoe data to 'inventory.txt' file
    with open('inventory.txt', 'a') as file:
        file.write(f"\n{country},{code},{product},{int(cost)},{quantity}")

    print(f"{product} with code {code} successfully added to the catalogue!")

    return None


def view_all(list_name):
    """This function will display shoe data in table format"""

    data = []  # Data list for tabulate module for displaying catalogue in table format

    for count, item in enumerate(list_name, start=1):
        data.append([count, item.country, item.code, item.product, item.cost, item.quantity])

    table_display(list_name, data)

    return None


def write_inventory(list_name):
    """This function will override the 'inventory' text file
       after adjustments have been made to stock data"""

    # Writing updated 'inventory' file
    output = "Country,Code,Product,Cost,Quantity\n"
    for item in list_name:
        output += f"{item.country},{item.code},{item.product},{int(item.cost)},{item.quantity}\n"

    with open('inventory.txt', 'w') as file:
        file.write(output)


def re_stock(list_name):
    """This function will look up the shoe entries with the
       lowest stock quantity and allow the user to restock"""

    # Dictionary {shoe code: stock quantity}
    code_quantity = {}

    data = []  # Data list for tabulate module for displaying catalogue in table format

    for item in list_name:
        code_quantity[item.code] = item.quantity

    # Finding the lowest quantity (stock quantity)
    low_stock = min(code_quantity.values())

    # Returns the shoe code of the lowest stock quantity
    require_restock = [key for key, value in code_quantity.items() if value == low_stock]

    index = 1
    for item in require_restock:
        for line in list_name:
            if item == line.code:  # Only append lowest stock to data list for display
                data.append([index, line.country, line.code, line.product, line.cost, line.quantity])
                index += 1

    print("\n\x1B[1mThe following stock are running low and require restocking:\x1B[0m")
    table_display(list_name, data)

    while True:

        # Restocking steps
        restock_index = pyip.inputInt("Enter the index of the product you would like to restock: ")

        if restock_index < 1:
            print("Invalid input, please try again...")

        elif restock_index > len(data):
            print("Invalid input, please try again...")

        else:
            for i in range(len(list_name)):
                if data[restock_index - 1][2] == list_name[i].code:
                    list_name[i].quantity = pyip.inputInt("Confirm new stock quantity: ")
                    print("Stock quantity successfully updated!")
            break

    # Writing updated 'inventory' file
    write_inventory(shoe_list)

    return None


def search_shoe(list_name):
    """This function will look up the shoe code entered
       by the user and then display the shoe object"""

    print("\n\x1B[1;4mSHOE CATALOGUE:\x1B[0m")

    codes = []  # Shoe codes only, to test whether search is a registered shoe in the catalogue
    data = []  # Data list for tabulate module for displaying catalogue in table format

    # Looking up all shoe codes and appending to a 'code list'
    for line in list_name:
        codes.append(line.code)

    while True:

        search = input("\nSearch shoe by code: ")

        if search == "":
            print("you haven't entered anything, please try again...")

        elif search not in codes:  # Option to add shoe is not registered in catalogue
            add_new_shoe = pyip.inputYesNo("No results found, would you like to add this shoe to the catalogue?"
                                           " (yes/no): ")

            if add_new_shoe == "yes":
                capture_shoes(list_name)  # Adding the shoe to catalogue
                break

            elif add_new_shoe == "no":
                mm = pyip.inputYesNo("Return to main menu? (yes/no): ")

                if mm == "no":
                    continue

                else:
                    print("Returning to main menu...")
                    break

        else:
            for count, line in enumerate(list_name, start=1):
                if line.code == search:
                    data.append([count, line.country, line.code, line.product, line.cost, line.quantity])
                    table_display(list_name, data)
            break

    return search


def value_per_item(list_name):
    """This function will calculate the total value for shoe in the catalogue"""

    print("\n\x1B[1;4mSHOE STOCK VALUES\x1B[0m")

    # Table display headers
    headers = [
        '\x1B[1mProduct\x1B[0m',
        '\x1B[1mCost (ZAR)\x1B[0m',
        '\x1B[1mQuantity\x1B[0m',
        '\x1B[1mStock Value\x1B[0m',
    ]

    while True:

        option = pyip.inputInt("""
1 - search shoe by code
2 - total stock value

Select an option from the menu above: """)

        if option == 1:

            shoe = search_shoe(list_name)  # Display individual shoe searched

            data = []  # Data list for tabulate module for displaying catalogue in table format

            for line in list_name:
                if line.code == shoe:
                    shoe_cost = float(line.cost)
                    shoe_stock = int(line.quantity)
                    item_value = f"R {shoe_cost * shoe_stock:.0f}"
                    data.append([line.product, line.cost, line.quantity, item_value])

                    print("\n\x1B[1mStock Value Breakdown\x1B[0m")
                    print(tabulate(data, headers=headers, tablefmt='psql'))

                    break

        elif option == 2:  # Display whole catalogue stock values

            data = []  # Data list for tabulate module for displaying catalogue in table format

            for line in list_name:
                shoe_cost = float(line.cost)
                shoe_stock = int(line.quantity)
                item_value = f"R {shoe_cost * shoe_stock:.0f}"
                data.append([line.product, line.cost, line.quantity, item_value])

            print("\n\x1B[1mStock Value Breakdown (per shoe)\x1B[0m")
            print(tabulate(data, headers=headers, tablefmt='psql'))
            break

        else:
            print("Invalid option, please try again...")

        return None


def highest_qty(list_name):
    """This function will look up the shoe entries with the
       highest stock quantity and allow the user to mark on sale"""

    # Dictionary {shoe code: stock quantity}
    code_quantity = {}

    data = []  # Data list for tabulate module for displaying catalogue in table format

    for item in list_name:
        code_quantity[item.code] = item.quantity

    # Finding the lowest quantity (stock quantity)
    high_stock = max(code_quantity.values())

    # Returns the shoe code of the lowest stock quantity
    discount_required = [key for key, value in code_quantity.items() if value == high_stock]

    index = 1
    for item in discount_required:
        for line in list_name:
            if item == line.code:
                data.append([index, line.country, line.code, line.product, line.cost, line.quantity])
                index += 1

    print("\n\x1B[1mThe following stock is too high and require price drop:\x1B[0m")
    table_display(list_name, data)

    # Discount steps
    sale = pyip.inputYesNo("Mark on sale (yes/no): ")

    if sale == "yes":

        while True:

            discount_shoe = pyip.inputInt("Enter the index of the product you would like to mark on sale: ")

            if discount_shoe < 1:
                print("Invalid input, please try again...")

            elif discount_shoe > len(data):
                print("Invalid input, please try again...")

            else:
                for i in range(len(list_name)):
                    if data[discount_shoe - 1][2] == list_name[i].code:

                        while True:

                            disc_percentage = pyip.inputInt(""" 
1 - 10%
2 - 15%
3 - 20%

Select discount percentage option: """)

                            if disc_percentage == 1:
                                original_price = list_name[i].cost
                                list_name[i].cost -= (list_name[i].cost * 0.1)
                                print(f"Shoe code {list_name[i].code} has now been marked down 10% from"
                                      f" R{int(original_price)} to R{int(list_name[i].cost)}\n")

                                # Writing updated 'inventory' file
                                write_inventory(shoe_list)
                                break

                            elif disc_percentage == 2:
                                original_price = list_name[i].cost
                                list_name[i].cost -= (list_name[i].cost * 0.15)
                                print(f"Shoe code {list_name[i].code} has now been marked down 15% from"
                                      f" R{int(original_price)} to R{int(list_name[i].cost)}\n")

                                # Writing updated 'inventory' file
                                write_inventory(shoe_list)
                                break

                            elif disc_percentage == 3:
                                original_price = list_name[i].cost
                                list_name[i].cost -= (list_name[i].cost * 0.2)
                                print(f"Shoe code {list_name[i].code} has now been marked down 20% from"
                                      f" R{int(original_price)} to R{int(list_name[i].cost)}\n")

                                # Writing updated 'inventory' file
                                write_inventory(shoe_list)
                                break

                            else:
                                print("You have entered an invalid option, please try again: ")

                break

    else:
        print("Returning to main menu...")

        return None


# ==========Main Menu=============

# Reading 'inventory.txt' data
read_shoes_data(shoe_list)

e = "no"

while e != "yes":

    print(f"\n\033[1;4mMAIN MENU\033[0m")

    menu = pyip.inputInt("""
1 - Look up a shoe
2 - View all shoes
3 - Add a new shoe
4 - Restock
5 - Inventory value
6 - Mark-downs
7 - Log out

Select an option from the menu above: """)

    if menu == 1:
        search_shoe(shoe_list)    # Look up specific shoe

    elif menu == 2:
        view_all(shoe_list)    # View whole catalogue

    elif menu == 3:
        capture_shoes(shoe_list)    # Adding a new shoe

    elif menu == 4:
        re_stock(shoe_list)    # Restock the shoe in catalogue with the lowest quantity

    elif menu == 5:
        value_per_item(shoe_list)    # Display shoe stock value (stock quantity x stock price)

    elif menu == 6:
        highest_qty(shoe_list)    # Option to mark price down for shoe in catalogue with the highest quantity

    elif menu == 7:    # Exit the program
        e = "yes"
        print("Logging out...")
        print("Goodbye!")

    else:
        print("Invalid input, please try again...")

# End of program
