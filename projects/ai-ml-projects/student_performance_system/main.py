import os 

print("Hello, Welcome to this system\nFollow the instruction ahead to run this system")
print('''Use 1 for run Analysis
2 for Prediction System''')

choice = input("Enter your choice: ")


if choice == "1":
    os.system("python analysis.py")

elif choice == "2":
    os.system("python model.py")

else:
    print("\nInvalid Choice \nExiting the system.....")