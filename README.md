# Password Generator App

## Description
This is a simple password generator and account management application built with Streamlit in Python. The app allows users to generate strong passwords and manage their saved account credentials securely.

This project is developed as part of the DevScale Bootcamp to complete an assigned task.

## Features
- Generate strong passwords based on user-defined criteria
- Save generated passwords along with the associated website and username/email
- Manage saved accounts by viewing stored credentials in a tabular format

## Requirements
Before running the application, ensure you have the following installed:

- Python 3.9 above
- Required Python libraries (install via `requirements.txt` if available)

## Installation
1. Clone or download this repository.
2. Navigate to the project directory.
3. Install dependencies by running:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the application:
   ```sh
   streamlit run main.py
   ```

## Usage
1. Open the application in your web browser.
2. Select a menu option from the sidebar:
   - **Add Account**: Generate a password for a new account.
     - Enter the website name and username/email.
     - Set password length and other criteria (numbers, special characters, uppercase letters).
     - Click **Generate password**.
     - Click **Save password** to store the generated credentials.
   - **Manage Accounts**: View saved credentials in a table format.
3. Exit the application when done.

## Notes
- The application stores account credentials temporarily in Streamlit's session state, meaning the data is lost when the app is restarted.
- For persistent storage, consider integrating a database or file-based storage system.

## License
This project is open-source and can be modified as needed.

## Author
mfathulqoribmfathulqorib, with mentoring from DevScale ❤️

