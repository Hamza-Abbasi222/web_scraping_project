# T15_send_whatsapp_messages_to_ind_or_grp.py

import pywhatkit as kit
import datetime
import time

def send_message_to_contact(phone_number, message):
    now = datetime.datetime.now()
    send_time = now + datetime.timedelta(minutes=2)  # Schedule to send after 2 minutes
    kit.sendwhatmsg(phone_number, message, send_time.hour, send_time.minute + 1)

def send_message_to_group(group_id, message):
    now = datetime.datetime.now()
    send_time = now + datetime.timedelta(minutes=2)  # Schedule to send after 2 minutes
    kit.sendwhatmsg_to_group(group_id, message, send_time.hour, send_time.minute + 1)

def main():
    choice = input("Do you want to send a message to a contact or a group? (contact/group): ").strip().lower()
    
    if choice == 'contact':
        phone_number = input("Enter the phone number to send WhatsApp message (e.g., '+1234567890'): ")
        message = input("Enter the message to send: ")
        send_message_to_contact(phone_number, message)
    elif choice == 'group':
        group_id = input("Enter the WhatsApp group ID: ")
        message = input("Enter the message to send: ")
        send_message_to_group(group_id, message)
    else:
        print("Invalid choice. Please choose either 'contact' or 'group'.")

if __name__ == "__main__":
    main()
