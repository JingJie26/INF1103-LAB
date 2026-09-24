def load_inventory():
    try:
        with open("inventory.txt", "r") as file:
            total_inventory = int(file.readline())
            history = file.readline().split(",")
            transaction_history = [int(x) for x in history if x]
            return total_inventory, transaction_history
    except FileNotFoundError:
        return 0, []

def save_inventory(total_inventory, transaction_history):
    with open("inventory.txt", "w") as file:
        file.write(str(total_inventory) + "\n")
        file.write(",".join(str(x) for x in transaction_history))
    
def get_valid_input():
    inventory = input("Enter a stock quantity: ")
    
    if inventory == "quit":
        return "quit"
    if inventory.isdigit():
        return int(inventory)
    else:
        print("Error")
        return None
    
def process_delivery(current_total,new_value):
    new_total = current_total + new_value
    return new_total

def calculate_tax(amount):
    tax = amount * 0.10
    return tax

def generate_report (total_units, failed_attempts):
    print("Total units:", total_units)
    print("Failed attempts:", failed_attempts)

total_inventory, transaction_history = load_inventory()
total_error = 0
deliveries_processed = 0

while True:
    inventory = get_valid_input()

    if inventory == "quit":
        save_inventory(total_inventory, transaction_history)
        generate_report(deliveries_processed, total_error)
        break

    if inventory is None:
        total_error += 1
        continue

    total_inventory = process_delivery(total_inventory, inventory)
    tax = calculate_tax(inventory)
    deliveries_processed += 1
    transaction_history.append(inventory)

    print("Transaction history:", transaction_history)
    print(total_inventory)
    print("Tax:", tax)

   