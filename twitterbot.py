import tweepy
import os
import schedule
import time
import datetime
from os import path


#Access Tokens and Keys To Twitter Account
consumer_key = "xxx"
consumer_secret = "xxx"
access_token = "xxx"
access_token_secret = "xxx"

#auth v1 stuff
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
#auth v2 stuff
#client = tweepy.Client('xxx', "xxx", access_token, access_token_secret)


#global variables
option = 0
imagecount = 0


def test():

    try:
        api.verify_credentials()
        print("[+] Connected To The Server")
    except:
        print("[-] Can't Connect To The Server")
    input()
    start_menu()

def change_profile_image():
    while True:
        try:
            print('\n*** Type "menu" to return to the main menu or continue with your action below ***\n\n')
            filename = input("Enter the Image Directory: ")
            if filename == "menu":
                start_menu()
            api.update_profile_image(filename)
            break
        except:
            print("+-+-+- Invalid Directory or No Connection, Try Again +-+-+- ")
    print("[+] Changed Profile Picture")
    print("Press Any Key To Return: ")
    input()
    start_menu()

def post_tweet():
    while True:
        try:
            print('\n*** Type "menu" to return to the main menu or continue with your action below ***\n\n')
            text = input("Enter Your Tweet: ")
            if text == "menu":
                start_menu()
            api.update_status(str(text))
            break
        except:
            print("+-+-+- No Connection, Try Again Later... +-+-+- ")
    print("[+] Tweet Posted")
    print("Press Any Key To Return: ")
    input()
    start_menu()

def upload_media_manual():
    while True:
        try:
            print('\n*** Type "menu" to return to the main menu or continue with your action below ***\n\n')
            text = input("Enter Your Tweet(Leave Empty If You Don't Want To Use Any Text): ")
            if text == "menu":
                start_menu()
            imagefile = input("Enter the Image Directory: ")
            if imagefile == "menu":
                start_menu()
            media = api.media_upload(imagefile)
            api.update_status(str(text), media_ids = [media.media_id_string])
            break
        except:
            print("\n+-+-+- Error, Check Your File Directory And Internet Connection, Then Try Again +-+-+- \n")
    print("[+] Tweet Posted")
    print("Press Any Key To Return: ")
    input()
    start_menu()



def periodic_upload(text, imagefile, fileextension):
    try:
        global imagecount
        imagefile += '\\' + str(imagecount) + str(fileextension)
        if (path.exists(str(imagefile))):
            print("[+]  Directory Check Completed, the path is valid and will continue with uploading")
        else:
            print("[-] The File You Are Trying To Upload Does Not Exist, Press Enter to Return to Main Menu...")
            input()
            start_menu()
        print("Upload process has started... Uploading image number: ", imagecount)
        media = api.media_upload(imagefile)
        api.update_status(str(text), media_ids=[media.media_id_string])
        print("[+] Tweet Posted @ " + datetime.now().strftime("%H:%M:%S"))
        os.remove(imagefile)
        imagecount += 1

    except:
        print("Process Interrupted. Program will close. Exit Manually...")
        input()


def upload_media_automatically():
    global imagecount
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)
    print("!*! WARNING !*! You must name your media in a consecutive order of upload and\nyou MUST have a copy of your files somewhere else because the program will delete the files after uploading\n(eg: 1.png, 2.png . . . After Uploading 1.png the program will delete the 1.png)\n")
    print("[1] Daily\n[2] Hourly\n[3] CustomSeconds")
    try:
        selection = int(input("Select Your Upload Period: "))
        if (selection == 1):
            try:
                period = str(input("Enter a time of the day that you want your post to be published at as HH:MM (eg: 13:48 will upload an image every day at 13:48): "))
                print("You Set Your Upload period as daily at: " + period)
            except:
                print("Wrong Format, Enter to Try Again")
                input()
                upload_media_automatically()
        elif (selection == 2):
            try:
                period = input("Enter a period of minutes that you want your post to be published at (eg: A Value of 28 will upload an image every 28 minutes): ")
                print("You Set Your Upload period as " + period + " minutes")
            except:
                print("Wrong Format, Enter to Try Again")
                input()
                upload_media_automatically()
        elif (selection == 3):
            try:
                period = input("Enter a period of seconds that you want your post to be published at (eg: A Value of 560 will upload an image every 560 seconds): ")
                print("You Set Your Upload period as " + period + " seconds")
            except:
                print("Wrong Format, Enter to Try Again")
                input()
                upload_media_automatically()
    except:
        print("Incorrect Input, Please Only Make a Selection From the List Above\nPress Enter To Retry...")
        input()
        upload_media_automatically()
    try:
        text = ""
        imagefile = input("Enter the Folder Directory Of Images: ")
        fileextension = input("Enter the File Extension Of Images (eg: .png .jpg): ")
        imagecount = input("Enter the number of first image: ")
        imagecount = int(imagecount)
        if (selection == 1):
            schedule.every().day.at(period).do(periodic_upload, text, imagefile, fileextension)
            while 1:
                schedule.run_pending()
                time.sleep(1)
        elif (selection == 2):
            schedule.every(int(period)).minutes.do(periodic_upload, text, imagefile, fileextension)
            while 1:
                schedule.run_pending()
                time.sleep(1)
        elif (selection == 3):
            schedule.every(int(period)).seconds.do(periodic_upload, text, imagefile, fileextension)
            while 1:
                schedule.run_pending()
                time.sleep(1)

    except:
        print("Incorrect Input\nPress Enter To Retry...")
        input()
        upload_media_automatically()








def menu():
    print("[1] Change Profile Image")
    print("[2] Test")
    print("[3] Post Tweet")
    print("[4] Post Media Manually")
    print("[5] Post Media Automatically")
    print("[0] Exit\n")

def option_input():
    global option
    try:
        option = int(input("Please Select an Action From the Menu: "))
    except:
        start_menu()

def option_selector():
    global option
    while option != 0:
        if option == 1:
            change_profile_image()
            break
        elif option == 2:
            test()
            break
        elif option == 3:
            post_tweet()
            break
        elif option == 4:
            upload_media_manual()
            break
        elif option == 5:
            upload_media_automatically()
            break

        else:
            print("Invalid Action, Please try Again")
        print()
        option_input()
        option_selector()

def start_menu():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)
    print("Hello, This is My Twitter Bot v1.0\n\n")
    menu()
    option_input()
    option_selector()

start_menu()
















