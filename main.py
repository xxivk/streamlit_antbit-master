import streamlit as st
import streamlit_authenticator as stauth # pip install streamlit-authenticator==0.1.5 
from app import streamlit_antbit 
import pandas as pd



def login():
    df = pd.read_csv('infocard.csv')
    df = pd.DataFrame(df)
    names = df['investorName'].iloc[0]
    #st.write(df.investorName.iloc[0])

    usernames = ['saad']
    passwords = ['456']
    #==============================================
    hashed_passwords = stauth.Hasher(passwords).generate()
    authenticator = stauth.Authenticate(names,usernames,hashed_passwords,'some_cookie_name','some_signature_key',cookie_expiry_days=30)
    name, authentication_status, username = authenticator.login('Login', 'main')
    #==============================================
    if st.session_state["authentication_status"]:
        test=authenticator.logout('Logout', 'main')
        st.header(f'Welcome {name}')
        #call our app
        streamlit_antbit()
    elif st.session_state["authentication_status"] == False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] == None:
        st.info('Please enter your username and password')

def main():
    login()

if __name__ == "__main__":
    main()
    

