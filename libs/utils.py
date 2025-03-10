import secrets
import string

class AccountsManagement:
    def __init__(self):
        self.accounts = []
    
    def add_account(self, website, user_name, password):
        account = (website, user_name, password)
        self.accounts.append(account)
    
    def get_account(self, target_website, target_user_name):
        selected_account = [(website, user_name, password) for website, user_name, password in self.accounts if website == target_website and user_name == target_user_name]
        return selected_account


class PassworgGenerator:
    def __init__(self):
        self.password = ""

    def generate_password(self, length=16, nums=0, special_chars=0, uppercase=0):

        if nums + special_chars + uppercase > length:
            raise ValueError("The sum of constraints cannot exceed password length")

        # Define character sets
        letters_upper = string.ascii_uppercase
        letters_lower = string.ascii_lowercase
        digits = string.digits
        symbols = string.punctuation

        # Ensure required characters are present
        password_chars = (
            [secrets.choice(digits) for _ in range(nums)] +
            [secrets.choice(symbols) for _ in range(special_chars)] +
            [secrets.choice(letters_upper) for _ in range(uppercase)] +
            [secrets.choice(letters_lower)]
        )

        # Fill the remaining length with random characters
        all_characters = string.ascii_letters + string.digits + string.punctuation
        password_chars += [secrets.choice(all_characters) for _ in range(length - len(password_chars))]

        # Shuffle to randomize order
        secrets.SystemRandom().shuffle(password_chars)

        # Convert list to string
        generated_password = ''.join(password_chars)
        
        self.password = generated_password
        return self.password 

