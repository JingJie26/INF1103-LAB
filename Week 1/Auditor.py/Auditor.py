inventory = 0
quit = 0
total_inventory = 0
total_error = 0
while True:
    inventory = input ("Enter a stock quantity:")

    if inventory == "quit":
        print("Total unit processed:",total_inventory)
        print("Number of failed entries:", total_error)
        break
    if inventory.isdigit():
        total_inventory += int(inventory)
        print(total_inventory)
    else:
        print("Error")
        total_error +=1
        print("Enter a positive number")

    if int(total_inventory) > 500:
        print ("Total inventory exceeds 500")
        print("Total unit processed:",total_inventory)
        print("Number of failed entries:", total_error)
        break