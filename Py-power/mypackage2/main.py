from datetime import datetime, timedelta
import pickle
from pathlib import Path
from test import FileSorter 

class Contact:
    def __init__(self, name, address, phone, email, birthday):
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.birthday = birthday
    def __str__(self):
        return f"Name: {self.name} | Adress: {self.address} | Phone number: {self.phone} | Email: {self.email} | Date of birth: {self.birthday}"

class Note:
    def __init__(self, text):
        self.text = text
        self.tags = []

class BotAssist:
    def __init__(self):
        self.contacts = []
        self.notes = {}
        self.tags = {}

    def validate_phone(self, phone):
        return phone.isdigit() and len(phone) == 10

    def validate_email(self, email):
        return '@' in email and '.' in email.split('@')[-1]

    def add_contact(self, name, address, phone, email, birthday):
        while True:
          if not name:
            name = input("Name is obligatory, enter the name for new contact: ")
            continue
          
          if not self.validate_phone(phone):
            phone = input("Invalid phone number format. Please enter a 10-digit number: ")
            continue

          if not self.validate_email(email):
            email = input("Invalid email format. Please enter email again: ")
            continue
          break
        for contact in self.contacts:
          if contact.name.lower() == name.lower() and contact.birthday.lower() == birthday.lower():
             print(f"Contact with name '{name}' and birthday '{birthday}' already exists. Can not duplicate contact.")
             return

        contact = Contact(name, address, phone, email, birthday)
        self.contacts.append(contact)
        print("Contact added successfully.")
        
    def search_contacts_birthday(self, days):
        upcoming_birthday_contacts = []
        today = datetime.now()

        for contact in self.contacts:
            birthday_month, birthday_day = map(int, contact.birthday.split('-')[1:])
            birthday_date = datetime(today.year, birthday_month, birthday_day)

        # Check if the birthday has already passed this year
            if birthday_date < today:
            # If yes, consider the birthday for the next year
                birthday_date = datetime(today.year + 1, birthday_month, birthday_day)

            days_until_birthday = (birthday_date - today).days

            if -1 <= days_until_birthday <= days:
                upcoming_birthday_contacts.append(contact)

        if upcoming_birthday_contacts:
            print("Contacts with upcoming birthdays:")
            for contact in upcoming_birthday_contacts:
                print(contact.name, "|", contact.address, "|", contact.phone, "|", contact.email, "|", contact.birthday, "|")
        else:
            print("No contacts with upcoming birthdays.")

    


    def search_contacts(self, query):
        results = []
        for contact in self.contacts:
            if query.lower() in contact.name.lower():
                results.append(contact)
        return results

        

    def edit_contact(self, old_contact_name, new_name, new_address, new_phone, new_email, new_birthday):
      contact_found = False
      while True:
          if not new_name:
            new_name= input("Name is obligatory, enter the name for new contact: ")
            continue
          
          if not self.validate_phone(new_phone):
            new_phone = input("Invalid phone number format. Please enter a 10-digit number: ")
            continue

          if not self.validate_email(new_email):
            new_email = input("Invalid email format. Please enter email again: ")
            continue
          break
      for contact in self.contacts:
        if contact.name.lower() == old_contact_name.lower():
            contact_found = True
            contact.name = new_name
            if not new_address==None:
                contact.address = new_address
            contact.phone = new_phone
            contact.email = new_email
            if not new_birthday==None:
                contact.birthday = new_birthday
            break

      if not contact_found:
         return f'Contact not found'

      return f'Contact {old_contact_name} successfully edited.'


    def delete_contact(self, contact_name):

        for contact in self.contacts:
            if contact_name.lower() in contact.name.lower():
                self.contacts.remove(contact)
                print(f'{contact_name} removed')
            elif not contact_name.lower() in contact.name.lower():
                print("Contact not found")
                
                
    
      

    def add_note(self, note_name, note_text):
        if note_name in self.notes:  # Перевірка, чи назва нотатки вже існує
            choice = input(f"Note '{note_name}' already exists. Do you want to edit it? enter yes or no: ").lower()
            if choice == 'yes':
                self.edit_note(note_name, note_text)  # Виклик методу для редагування нотатки
            else:
                print("Note creation aborted.")
        else:
            self.notes[note_name] = Note(note_text)  # Створення нової нотатки в словнику notes
            print(f"Note '{note_name}' created successfully.")

    def search_notes(self, note_name):
        if not self.notes:  # Перевірка, чи словник notes пустий
            print("Notes not found. Please create a note using command '6'.")
        elif note_name in self.notes:  # Пошук нотатки за вказаною назвою
            print(f"Note '{note_name}': {self.notes[note_name].text}")
        else:
            print(f"Note '{note_name}' does not exist.")

    def edit_note(self, note_name, new_text):
        if note_name in self.notes:  # Перевірка, чи існує нотатка з вказаною назвою
            self.notes[note_name].text = new_text  # Зміна тексту нотатки
            print(f"Edited note '{note_name}' successfully.")
        else:
            print(f"Note '{note_name}' does not exist. Cannot edit.")

    def delete_note(self, note_name):
        if not self.notes:  # Перевірка, чи словник notes пустий
            print("No notes found. Please create a note using command '6'.")
        elif note_name in self.notes:  # Перевірка, чи існує нотатка з вказаною назвою
            print(f"Note '{note_name}': {self.notes[note_name].text}")
            choice = input(f"Are you sure you want to delete note '{note_name}'? (1 - Yes, 2 - No): ")
            if choice == '1':
                del self.notes[note_name]  # Видалення нотатки за вказаною назвою
                print(f"Note '{note_name}' deleted successfully.")
            else:
                print("Deletion aborted.")
        else:
            print(f"Note '{note_name}' does not exist.")
            
            
    def add_tags_to_note(self, title, new_tags):
        if title in self.notes:
            self.notes[title].tags.extend(new_tags)
            for tag in new_tags:
                if tag in self.tags:
                    self.tags[tag].append(title)
                else:
                    self.tags[tag] = [title]
            print("Tags added successfully.")
        else:
            print("Note not found.")
            
    def search_notes_by_tags(self, tags):
        results = []
        for note_name, note in self.notes.items():
            if all(tag in note.tags for tag in tags):
                results.append(note)
        sorted_results = sorted(results, key=lambda x: x.text)
        return sorted_results


    def save_data(self, filename="save.pickle"):
        with open(filename, "wb") as file:
            data = {"contacts": self.contacts, "notes": self.notes, "tags": self.tags}
            pickle.dump(data, file)
        print("Data saved successfully.")

    def load_data(self, filename="save.pickle"):
        try:
            with open(filename, 'rb') as file:
                data = pickle.load(file)
                self.contacts = data.get('contacts', [])
                self.notes = data.get('notes', {})
                self.tags = data.get('tags', {})
            print("Data loaded successfully.")
        except FileNotFoundError:
            print("File not found. No data loaded.")

    def sort_files(self, folder_path):
        file_sorter = FileSorter(folder_path)
        file_sorter.core()

    def show_all_contacts(self):
        if self.contacts:
            return "\n".join(map(str, self.contacts))
        else:
            return "Contact list is empty."
    def show_all_notes(self):
        if self.notes:
            return "\n".join(map(str, self.notes))
        else:
            return "Note list is empty."

def main():
   assistant =  BotAssist()
   assistant.load_data()

   while True:
       command = input("\nEnter your command for start(for menu-press 'menu'): ").lower()
    
       if command == '1':
          name = input('Enter your name:')
          address = input('Enter your adress:')
          phone = input('Enter your phone (10-digits) : ')
          email = input('Enter your email:')
          birthday = input('Enter your birthday in YYYY-MM-DD:')
          assistant.add_contact(name, address, phone, email, birthday)

       elif command == '2':
          search_query = input("Enter first name or last name: ")

          results = assistant.search_contacts(search_query)
          if results:
             print("Search Results:")
             for result in results:
                 print("Name:", result.name, "|", "Address:", result.address, "|", "Phone number:", result.phone, "|", "Email:", result.email, "|", "Date of birth:", result.birthday, "|")
          else:
           print("No contacts found.")

       elif command == '3':
          contact_name = input('Enter the contact name you want to delete:')
          if contact_name =='':
              print ("No contacts found.")
          else:
              assistant.delete_contact(contact_name)

       elif command == '4':
          old_contact_name = input('Enter the contact old name you want to edit: ')
          contact_exists = any(contact.name.lower() == old_contact_name.lower() for contact in assistant.contacts)

          if not contact_exists:
            print(f'Contact "{old_contact_name}" does not exist. Please, try again.')
            continue

          new_name = input('Enter the new name: ')
          new_address = input('Enter the new address: ')
          new_phone = input('Enter the new phone: ')
          new_email = input('Enter the new email: ')
          new_birthday = input('Enter the new birthday in YYYY-MM-DD: ')

          print(assistant.edit_contact(old_contact_name, new_name, new_address, new_phone, new_email, new_birthday))

       elif command == '5':
            day_to_birthday = int(input("Enter the number of days until the birthday: "))
            assistant.search_contacts_birthday(day_to_birthday)
        
       elif command == '6':
            note_name = input("Enter note name: ")
            note_text = input("Enter note text: ")
            assistant.add_note(note_name, note_text)  # Виклик методу для створення нотатки

       elif command == '7':
            note_name = input("Enter note name to search: ")
            assistant.search_notes(note_name)  # Виклик методу для пошуку нотатки

       elif command == '8':
            edit_or_delete = input("Enter 'edit' to edit a note or 'delete' to delete a note: ").lower()

            if edit_or_delete == 'edit':
                note_name = input("Enter note name to edit: ")
                new_text = input("Enter new text for the note: ")
                assistant.edit_note(note_name, new_text)  # Виклик методу для редагування нотатки
            elif edit_or_delete == 'delete':
                note_name = input("Enter note name to delete: ")
                assistant.delete_note(note_name)  # Виклик методу для видалення нотатки
            else:
                print("Invalid command. Please enter 'edit' or 'delete'.")
    
                
       elif command == '9': # Виклик методу для додавання тегів до нотатків
            title = input("Enter note name:")
            new_tags = input("Enter tags:").split(",")
            assistant.add_tags_to_note(title, new_tags)
       elif command == "10": # пошук нотатків за тегами
            tags = input("Enter tags for search (comma separated):").split(",")
            results = assistant.search_notes_by_tags(tags)
            if results:
                for result in results:
                    print(result.tags, "|", result.text)
            else:
                print("Not found.")
       elif command == 'show all':
            print(assistant.show_all_contacts())
       elif command == 'show all notes':
            print(assistant.show_all_notes())        
       elif command == "save":
           filename = input("Enter the filename to save data: ")
           assistant.save_data(filename)

       elif command == 'load':
            filename = input("Enter the filename to load data: ")
            assistant.load_data(filename) 
       elif command == 'sort':
           folder_path = Path(input("Enter the folder path to sort (absolute path):"))
           assistant.sort_files(folder_path)
           print("Folder is sorted successfully!")

           
       elif command == 'menu':
            print("\n---------------------------\nHello, I'm your ' Personal Assistant '.\nI save all information automatically. I can make next comand:\n---------------------------\n 1-add contact\n 2-search contact\n 3-delete contact\n 4-edit contact\n 5-find birthday\n 6-add note \n 7-search note \n 8-edit or delete note\n 9-add tag \n 10-search note by tag\n--------------------------- \n show all-Show all contacts \n show all notes-Show all notes \n sort-if you want sort folder\n save-if you want save information handler\n load-if you want to continue with the previously saved information\n show all notes- Show all notes\n exit, close, end-if you want exit\n---------------------------")
          

       elif command in ['end', 'close', 'exit']:
          break
       else:
          print("Invalid, Try Again:")

   return assistant       
           
if __name__ == "__main__":
    try:
        assistant = main()  
        if assistant:
            assistant.save_data()  
    except Exception as error:
        print(f"An error occurred: {error}")