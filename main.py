from libs.utils import PassworgGenerator, AccountsManagement
import pandas as pd
import streamlit as st
import time

st.title("Password Generator")

# Initialize session state 
if "generated_password" not in st.session_state:
    st.session_state.generated_password = None

if "my_account" not in st.session_state:
    st.session_state.my_account = AccountsManagement()

if "website" not in st.session_state:
    st.session_state.website = ""

if "user_name" not in st.session_state:
    st.session_state.user_name = ""
    
page = st.sidebar.selectbox("Menu",["Add Account", "Manage Accounts"])

if page == "Add Account":
    password_generator = PassworgGenerator()

    st.session_state.website = st.text_input("Website", value=st.session_state.website)
    st.session_state.user_name = st.text_input("Username/email", value=st.session_state.user_name)

    length = st.number_input("Password length", value=16, step=1)
    nums = st.number_input("Number char in password", value=1, step=1)
    special_chars = st.number_input("Special char in password", value=1, step=1)
    uppercase = st.number_input("Uppercase char in password", value=1, step=1)

    generate_button = st.button("Generate password")

    if generate_button:
        try:
            if not st.session_state.website and not st.session_state.user_name:
                raise ValueError("Website and Username/Email cannot be empty")
            elif not st.session_state.website:
                raise ValueError("Website cannot be empty")
            elif not st.session_state.user_name:
                raise ValueError("Username/Email cannot be empty")
            
            st.session_state.generated_password = password_generator.generate_password(length, nums, special_chars, uppercase)

        except ValueError as err:
            st.error(f"Error: {err}")

    if st.session_state.generated_password:
        st.write(f"**Your account for {st.session_state.website}:**")
        st.write(f"""
                **Username/email:**  
                {st.session_state.user_name}  
                """)
        st.write(f""" 
                **Password:**  
                {st.session_state.generated_password}
                """)
                
        save_button = st.button("Save password")

        if save_button:
            selected_account = st.session_state.my_account.get_account(st.session_state.website, st.session_state.user_name)

            try:
                if selected_account:
                    raise Exception("That website already have saved account")
                
                st.session_state.my_account.add_account(website=st.session_state.website, user_name=st.session_state.user_name, password=st.session_state.generated_password)
                st.success("Account saved, this massage will dissapear in 3 second")
                st.session_state.generated_password = None

                # Wait for 3 seconds before rerunning
                time.sleep(3)
                st.session_state.website = ""
                st.session_state.user_name = ""
                st.rerun(scope="app")

            except Exception as err:
                st.error(f"Error: {err}")
            except ValueError as err:
                st.error(f"Error: {err}")

elif page == "Manage Accounts":
    st.write("### Accounts & Password")
    
    saved_accounts = st.session_state.my_account.accounts

    if not saved_accounts:
        st.write("No saved accounts")
    
    else:
        df = pd.DataFrame(saved_accounts, columns=["Website", "Username/Email", "Password"])
        st.dataframe(df, hide_index=True)


