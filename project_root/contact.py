from flask import Flask, request, render_template, redirect, url_for
import json

app = Flask(__name__)

class ContactManager:
    def __init__(self, file_path='contact.json'):
        self.file_path = file_path
        self.contacts = self.load_contacts()

    def load_contacts(self):
        try:
            with open(self.file_path, 'r') as file:
                contacts = json.load(file)
            return contacts
        except FileNotFoundError:
            return []

    def save_contacts(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.contacts, file, indent=2)

    def add_contact(self, name, address, phone, email):
        contact = {
            "name": name,
            "address": address,
            "phone": phone,
            "email": email
        }
        self.contacts.append(contact)
        self.save_contacts()

    def search_contact(self, search_name):
        return [contact for contact in self.contacts if search_name.lower() in contact['name'].lower()]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_contact', methods=['POST'])
def add_contact():
    name = request.form['name']
    address = request.form['address']
    phone = request.form['phone']
    email = request.form['email']
    
    contact_manager.add_contact(name, address, phone, email)
    return redirect(url_for('index'))

@app.route('/search_contact', methods=['POST'])
def search_contact():
    search_name = request.form['search_name']
    results = contact_manager.search_contact(search_name)
    return render_template('index.html', results=results)

if __name__ == "__main__":
    contact_manager = ContactManager()
    app.run(debug=True)
