from libs.utils import PasswordGenerator, AccountsManagement
import pandas as pd
import streamlit as st
from datetime import datetime

st.title("🔑 Password Generator")

# Initialize session state more concisely
if "generated_password" not in st.session_state:
    st.session_state.generated_password = None
    st.session_state.my_account = AccountsManagement()
    st.session_state.website = ""
    st.session_state.user_name = ""
    st.session_state.message = {"text": "", "type": "", "expiry": None}

# Handle temporary messages
if st.session_state.message["expiry"] and datetime.now() > st.session_state.message["expiry"]:
    st.session_state.message = {"text": "", "type": "", "expiry": None}

# Display temporary message if exists
if st.session_state.message["text"]:
    if st.session_state.message["type"] == "success":
        st.success(st.session_state.message["text"])
    elif st.session_state.message["type"] == "error":
        st.error(st.session_state.message["text"])
    
page = st.sidebar.selectbox("Menu", ["Add Account", "Manage Accounts"])

if page == "Add Account":
    password_generator = PasswordGenerator() 

    st.session_state.website = st.text_input("Website", value=st.session_state.website)
    st.session_state.user_name = st.text_input("Username/email", value=st.session_state.user_name)

    col1, col2 = st.columns(2)
    with col1:
        length = st.number_input("Password length", value=16, step=1, min_value=8)
        nums = st.number_input("Numbers in password", value=1, step=1, min_value=0)
    with col2:
        special_chars = st.number_input("Special chars in password", value=1, step=1, min_value=0)
        uppercase = st.number_input("Uppercase chars in password", value=1, step=1, min_value=0)

    generate_button = st.button("Generate password")

    if generate_button:
        # Validate inputs
        if not st.session_state.website or not st.session_state.user_name:
            missing = []
            if not st.session_state.website:
                missing.append("Website")
            if not st.session_state.user_name:
                missing.append("Username/Email")
            st.error(f"Error: {' and '.join(missing)} cannot be empty")
        else:
            st.session_state.generated_password = password_generator.generate_password(
                length, nums, special_chars, uppercase
            )

    if st.session_state.generated_password:
        st.write(f"**Your account for {st.session_state.website}:**")
        st.write(f"**Username/email:**  \n{st.session_state.user_name}")
        
        # Show password with a "show/hide" option for better security
        password_placeholder = st.empty()
        show_password = st.checkbox("Show password", value=False)
        
        if show_password:
            password_placeholder.write(f"**Password:**  \n{st.session_state.generated_password}")
        else:
            password_placeholder.write("**Password:**  \n \*\*\*\*\*\*\*")
                
        save_button = st.button("Save password")

        if save_button:
            selected_account = st.session_state.my_account.get_account(
                st.session_state.website, st.session_state.user_name
            )

            if selected_account:
                st.error("Error: That website already has a saved account")
            else:
                try:
                    st.session_state.my_account.add_account(
                        website=st.session_state.website, 
                        user_name=st.session_state.user_name, 
                        password=st.session_state.generated_password
                    )
                    # Set success message with expiry time
                    from datetime import datetime, timedelta
                    st.session_state.message = {
                        "text": "Account saved successfully!", 
                        "type": "success", 
                        "expiry": datetime.now() + timedelta(seconds=3)
                    }
                    st.session_state.generated_password = None
                    st.session_state.website = ""
                    st.session_state.user_name = ""
                    st.rerun()
                except Exception as err:
                    st.error(f"Error saving account: {err}")

elif page == "Manage Accounts":
    st.write("### Accounts & Passwords")
    
    saved_accounts = st.session_state.my_account.accounts

    if not saved_accounts:
        st.info("No saved accounts")
    else:
        # Consider masking passwords for security
        df = pd.DataFrame(saved_accounts, columns=["Website", "Username/Email", "Password"])
        df["Password"] = df["Password"].apply(lambda x: "********")  # Mask passwords
        
        st.dataframe(df, hide_index=True)
        
        # Add option to view full details of specific account with extra confirmation
        website_to_view = st.selectbox("Select account to view details", 
                                       [""] + list(set(df["Website"])))
        
        if website_to_view:
            accounts_for_site = df[df["Website"] == website_to_view]
            account_emails = list(accounts_for_site["Username/Email"])
            email_to_view = st.selectbox("Select username/email", [""] + account_emails)
            
            if email_to_view and st.button("View Password"):
                account = st.session_state.my_account.get_account(website_to_view, email_to_view)
                if account:
                    website, user_name, password = account[0]
                    st.code(f"Website: {website}\nUsername: {user_name}\nPassword: {password}")