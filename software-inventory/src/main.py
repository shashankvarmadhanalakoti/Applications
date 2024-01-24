import pyfiglet,getKandjiUsers
pyfiglet.figlet_format("Compliance Tool")
def main():
    print(pyfiglet.figlet_format("Compliance Tool"))
    
    print("1 -> Kandji Users")
    option = int(input())
    if option ==  1:
        getKandjiUsers.getUsers()
    else:
        print("Wrong option chosen")
        exit
if __name__ == "__main__":
    main()
