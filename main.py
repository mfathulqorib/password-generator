from libs.utils import PassworgGenerator, AccountsManagement
import pandas as pd
import streamlit as st

st.title("Password Generator")

# Initialize session state for password storage
if "generated_password" not in st.session_state:
    st.session_state.generated_password = None

# Initialize session state for account management
if "my_account" not in st.session_state:
    st.session_state.my_account = AccountsManagement()
    
page = st.sidebar.selectbox("Menu",["Add Account", "Manage Accounts"])

if page == "Add Account":
    password_generator = PassworgGenerator()

    website = st.text_input("Website")
    user_name = st.text_input("Username/email")

    length = st.number_input("Password length", value=16, step=1)
    nums = st.number_input("Number char in password", value=1, step=1)
    special_chars = st.number_input("Special char in password", value=1, step=1)
    uppercase = st.number_input("Uppercase char in password", value=1, step=1)

    generate_button = st.button("Generate password")

    if generate_button:
        try:
            st.session_state.generated_password = password_generator.generate_password(length, nums, special_chars, uppercase)
        
        except ValueError as err:
            st.write(f"Error: {err}")

    if st.session_state.generated_password:
        st.write(f"**Your account for {website}:**")
        st.write(f"""Username/email:  
                    **{user_name}**  
                """)
        st.write(f""" 
                Password:  
                **{st.session_state.generated_password}**""")
                
        save_button = st.button("Save password")

        if save_button:
            st.write("Account saved")
            st.session_state.my_account.add_account(website=website, user_name=user_name, password=st.session_state.generated_password)
            st.session_state.generated_password = None

elif page == "Manage Accounts":
    st.write("### Accounts & Password")
    
    saved_accounts = st.session_state.my_account.accounts

    if not saved_accounts:
        st.write("No saved accounts")
    
    else:
        df = pd.DataFrame(saved_accounts, columns=["Website", "Username/Email", "Password"])
        st.dataframe(df, hide_index=True)


