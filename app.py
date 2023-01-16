import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
from streamlit_option_menu import option_menu # pip install streamlit-option-menu




st.set_page_config(
    page_title="ANTBIT",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded")

def streamlit_antbit():

    #-----------------------------------------------#
    #                         Nav Bar                   #
    #-----------------------------------------------#
    Page = option_menu(None, ["Home", "Strategy", "Reports", 'Settings','Contact us'], 
        icons=['house', 'boxes', "card-text", 'gear' ,'envelope'], 
        menu_icon="cast", default_index=0, orientation="horizontal")
    Page
    st.markdown("##")
    #==============================================================================================#
    #                                                                                                Home page                                                                                            #
    #==============================================================================================#
    if Page == 'Home':
        st.markdown("""---""")
        df = pd.read_csv('infocard.csv')
        df = pd.DataFrame(df)
        starting_balance = (df.startingBalance)
        #current_balance = (df.CurrentBalance)
        
        st.markdown("##")
        # TOP KPI's
        
        starting_balance = df.startingBalance.iloc[0]
        current_balance = 1000
        pnl_dollar = round(current_balance-starting_balance, 2)
        pnl_pct = round((current_balance-starting_balance)/starting_balance *100,1)
        def fees():
            if current_balance > starting_balance:
                fees_dollar = pnl_dollar / 100 *fees_pct
            elif current_balance < starting_balance:
                fees_dollar = 0
            return fees_dollar
        fees_pct = 35
        fees_dollar = fees()
        in_water = 7000
        off_water = 3000
        #-----------------------------------------------#
        #Row A            Balances                   #
        #-----------------------------------------------#
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        st.header('Account overview')
        colA1, colA2, colA3 = st.columns(3)
        colA1.metric("Starting Balance", f"{starting_balance} $")
        colA2.metric("Current Balance", f"{current_balance} $")
        colA3.metric("PNL", f"{pnl_dollar} $" , f'{pnl_pct}%')
        if pnl_dollar >1:
            colA3.write(' ذلك فضل الله يؤتيه من يشاء ')
            #col3.write(' ﴾ إن الله لذو فضل على الناس ولكن أكثر الناس لا يشكرون ﴿')
        #-----------------------------------------------#
        #Row B        Fees & inWater            #
        #-----------------------------------------------#
        colB1, colB2, colB3 = st.columns(3)
        colB1.metric("Fees (35%)", f"{fees_dollar} $")
        colB2.metric("Balance in water", f"{in_water} $")
        colB3.metric("Balance out water", f"{off_water} $")
        #===========================
        st.markdown("##")
        st.markdown("""---""")
        #-----------------------------------------------#
        #Row C            Asset table                #
        #-----------------------------------------------#
        st.header('Assets')
        df = pd.DataFrame({'Asset' : ['TESLA', 'Google', 'Microsoft', 'Apple'],
                                            'Price' : [87, 91, 97, 95],
                                            'Quantity' : [83, 99, 84, 76],
                                            'Position size %' : [87, 91, 97, 95],
                                            'Market value' : [87, 91, 97, 95],
                                            'PNL %' : [87, 91, 97, 95]})
        st.table(df)
        #===========================
        st.markdown("##")
        st.markdown("""---""")
        #-----------------------------------------------#
        #Row D                Chart                     #
        #-----------------------------------------------#
        st.header("Chart")
        df = pd.DataFrame({
                                            'date': [0, 1, 2, 3, 4],
                                            'Balance': [10000, 9000, 14000, 12000, 19000],
                                            })
        @st.cache
        def tp():
            return df['Balance'] + (df['Balance'] * 0.05)
        def sl():
            return df['Balance'] - (df['Balance'] * 0.05)
        df['Take profit'] = tp()
        df['Stop lose'] = sl()
        fig = px.line(df, x="date", y=["Balance" , 'Stop lose' , 'Take profit']) # x and y ------ both are columns.
        st.plotly_chart(fig , use_container_width=True)
    #==============================================================================================#
    #                                                                                              Strategy page                                                                                        #
    #==============================================================================================#
    if Page == 'Strategy':
        st.markdown("""---""")
        #-----------------------------------------------#
        #Row A          Select Strategy           #
        #-----------------------------------------------#
        st.header('Strategy')
        strategy = st.selectbox(
            'Select your account strategy:',
            ('A', 'B', 'C'))
        #===========================
        st.markdown("""---""")
        #-----------------------------------------------#
        #Row B                  Risk                      #
        #-----------------------------------------------#
        st.header('Risk')
        risk = st.slider('Select your account risk:', min_value = 0.0, max_value=3.0,step=0.25)
        #-----------------------------------------------#
        #Row C              Risk button             #
        #-----------------------------------------------#
        st.markdown("##")
        st.markdown("""---""")
        st.info(f'Once you change strategy & risk, please click CONFIRM')
        if st.button('CONFIRM '):
            st.success('Account strategy & risk have been successfully updated.')
    #==============================================================================================#
    #                                                                                               Report page                                                                                          #
    #==============================================================================================#
    if Page == 'Reports':
        st.markdown("""---""")
        #-----------------------------------------------#
        #Row A             Select week             #
        #-----------------------------------------------#
        st.header('Weekly report')
        weekly_report = st.selectbox(
            'Please select period:',
            ('Last week', 'Last 2 weeks', 'Last 3 weeks', 'Last month'))
        st.write('You selected:', weekly_report)
        #-----------------------------------------------#
        #Row B           Asset table                #
        #-----------------------------------------------#
        #Data
        df2 = px.data.gapminder()
        if weekly_report == 'Last week':
            reported_data = df2.tail(7) # if you want to show each week separetly use reported_data = df.loc['21':'29', :],,, The index should be 30.
        elif weekly_report == 'Last 2 weeks':
            reported_data = df2.tail(14) # reported_data = df.loc['14':'20', :]
        elif weekly_report == 'Last 3 weeks':
            reported_data = df2.tail(21) # reported_data = df.loc['7':'13', :]
        elif weekly_report == 'Last month':
            reported_data = df2.tail(30) # reported_data = df.loc['0':'6', :]
        #Show button
        if not reported_data.empty:
            if st.button('Show'):
                st.table(reported_data)
        else:
            st.error('Not enough data, your account is new.')
        #-----------------------------------------------#
        #Row C         Download CSV            #
        #-----------------------------------------------#
        #Weekly
        @st.cache
        def convert_df(reported_data):
            return reported_data.to_csv().encode('utf-8')
        csv = convert_df(reported_data)
        st.download_button(
            label=f"Download ({weekly_report}) data as CSV",
            data=csv,
            file_name='weekly_report.csv',
            mime='text/csv',
        )
        #Trade journal
        @st.cache
        def convert_df2(df2):
            return df2.to_csv().encode('utf-8')
        csv2 = convert_df(df2)
        st.download_button(
            label=f"Download (Trade journal) data as CSV",
            data=csv2,
            file_name='Trade_journal.csv',
            mime='text/csv',
        )
        #===========================
        st.markdown("##")
        st.markdown("""---""")
    #==============================================================================================#
    #                                                                                               Settings page                                                                                        #
    #==============================================================================================#
    if Page == 'Settings':
        st.markdown("""---""")
        st.header('Account API')
        with st.expander('Change API'):
            st.text_input('Public key')
            st.text_input('Secret key')
            if st.button('Update'):
                st.success('Your API has been successfully updated!')
        #===========================
        st.markdown("##")
        st.markdown("""---""")
        #===========================
        st.header('Freeze account')
        with st.expander('Are you sure ?'):
            st.warning('Warning! Your account will be freezeed for 24 hours.')
            if st.button('Confirm'):
                st.success('Your account has been successfully freezed!')
        #===========================
        st.markdown("##")
        st.markdown("""---""")
    #==============================================================================================#
    #                                                                                                  Contact us                                                                                          #
    #==============================================================================================#
    if Page == 'Contact us':
        st.markdown("""---""")
        #-----------------------------------------------#
        #Row A             Contact us               #
        #-----------------------------------------------#
        st.header('Whenever you need us, you find us .')
        st.write('Got question ? Our team is happy to help and answer any question you might have. Please contact our support team on the next link:')
        st.markdown("""
                                </li>
                                <li class="nav-item">
                                <a class="nav-link py-2 px-0 px-lg-2" href="https://t.me/ANTBIT_AR" target="_blank" rel="noopener">
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-telegram" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.287 5.906c-.778.324-2.334.994-4.666 2.01-.378.15-.577.298-.595.442-.03.243.275.339.69.47l.175.055c.408.133.958.288 1.243.294.26.006.549-.1.868-.32 2.179-1.471 3.304-2.214 3.374-2.23.05-.012.12-.026.166.016.047.041.042.12.037.141-.03.129-1.227 1.241-1.846 1.817-.193.18-.33.307-.358.336a8.154 8.154 0 0 1-.188.186c-.38.366-.664.64.015 1.088.327.216.589.393.85.571.284.194.568.387.936.629.093.06.183.125.27.187.331.236.63.448.997.414.214-.02.435-.22.547-.82.265-1.417.786-4.486.906-5.751a1.426 1.426 0 0 0-.013-.315.337.337 0 0 0-.114-.217.526.526 0 0 0-.31-.093c-.3.005-.763.166-2.984 1.09z"/></svg>
                                <small class="d-lg-none ms-2">Telegram</small>
                                </li>
                                """, unsafe_allow_html=True)
        #===========================
        st.markdown("##")
        st.markdown("""---""")
        #===========================
        with st.expander("About"):
            st.image('https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,h_170,w_170,f_auto,b_white,q_auto:eco,dpr_1/bh875jdsjqbdcn627bhz')
            st.markdown("""
                                    ANTBIT specializes in building & operating a Non-Custodial Quantitative trading systems and a custodial investment app owned by the ANTBIT DAO.

                                    Headquartered in San Francisco with operation in Manhattan, New York, Close to the regulators,  ANTBIT, LLC is now registered in California, Wyoming & NewYork and to be a federally registered investment adviser and privately held investment firm in USA, Europe MiFID, SaudiArabia CMA Sandbox, and DIFC Sandbox.


                                    """)
            #st.markdown('<a href="https://t.me/ANTBIT_AR" target="_self">GITHUB</a>', unsafe_allow_html=True)


            st.write('Find us here:')
            st.markdown("""
                                    </li>
                                    <li class="nav-item">
                                    <a class="nav-link py-2 px-0 px-lg-2" href="https://t.me/ANTBIT_AR" target="_blank" rel="noopener">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-telegram" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.287 5.906c-.778.324-2.334.994-4.666 2.01-.378.15-.577.298-.595.442-.03.243.275.339.69.47l.175.055c.408.133.958.288 1.243.294.26.006.549-.1.868-.32 2.179-1.471 3.304-2.214 3.374-2.23.05-.012.12-.026.166.016.047.041.042.12.037.141-.03.129-1.227 1.241-1.846 1.817-.193.18-.33.307-.358.336a8.154 8.154 0 0 1-.188.186c-.38.366-.664.64.015 1.088.327.216.589.393.85.571.284.194.568.387.936.629.093.06.183.125.27.187.331.236.63.448.997.414.214-.02.435-.22.547-.82.265-1.417.786-4.486.906-5.751a1.426 1.426 0 0 0-.013-.315.337.337 0 0 0-.114-.217.526.526 0 0 0-.31-.093c-.3.005-.763.166-2.984 1.09z"/></svg>
                                    <small class="d-lg-none ms-2">Telegram</small>
                                    </li>
                                    <li class="nav-item">
                                    <a class="nav-link py-2 px-0 px-lg-2" href="https://www.youtube.com/@AhmadShadid1/featured" target="_blank" rel="noopener">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-youtube" viewBox="0 0 16 16">
                                    <path d="M8.051 1.999h.089c.822.003 4.987.033 6.11.335a2.01 2.01 0 0 1 1.415 1.42c.101.38.172.883.22 1.402l.01.104.022.26.008.104c.065.914.073 1.77.074 1.957v.075c-.001.194-.01 1.108-.082 2.06l-.008.105-.009.104c-.05.572-.124 1.14-.235 1.558a2.007 2.007 0 0 1-1.415 1.42c-1.16.312-5.569.334-6.18.335h-.142c-.309 0-1.587-.006-2.927-.052l-.17-.006-.087-.004-.171-.007-.171-.007c-1.11-.049-2.167-.128-2.654-.26a2.007 2.007 0 0 1-1.415-1.419c-.111-.417-.185-.986-.235-1.558L.09 9.82l-.008-.104A31.4 31.4 0 0 1 0 7.68v-.123c.002-.215.01-.958.064-1.778l.007-.103.003-.052.008-.104.022-.26.01-.104c.048-.519.119-1.023.22-1.402a2.007 2.007 0 0 1 1.415-1.42c.487-.13 1.544-.21 2.654-.26l.17-.007.172-.006.086-.003.171-.007A99.788 99.788 0 0 1 7.858 2h.193zM6.4 5.209v4.818l4.157-2.408L6.4 5.209z"/></svg>
                                    <small class="d-lg-none ms-2">Youtube</small>
                                    </li>
                                    <li class="nav-item">
                                    <a class="nav-link py-2 px-0 px-lg-2" href="https://www.linkedin.com/company/antbitio/" target="_blank" rel="noopener">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-linkedin" viewBox="0 0 16 16">
                                    <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248-.822 0-1.359.54-1.359 1.248 0 .694.521 1.248 1.327 1.248h.016zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016a5.54 5.54 0 0 1 .016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225h2.4z"/></svg>
                                    <small class="d-lg-none ms-2">LinkedIn</small>
                                    </li>
                                    <li class="nav-item">
                                    <a class="nav-link py-2 px-0 px-lg-2" href="https://mobile.twitter.com/flywithahmad" target="_blank" rel="noopener">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-twitter" viewBox="0 0 16 16">
                                    <path d="M5.026 15c6.038 0 9.341-5.003 9.341-9.334 0-.14 0-.282-.006-.422A6.685 6.685 0 0 0 16 3.542a6.658 6.658 0 0 1-1.889.518 3.301 3.301 0 0 0 1.447-1.817 6.533 6.533 0 0 1-2.087.793A3.286 3.286 0 0 0 7.875 6.03a9.325 9.325 0 0 1-6.767-3.429 3.289 3.289 0 0 0 1.018 4.382A3.323 3.323 0 0 1 .64 6.575v.045a3.288 3.288 0 0 0 2.632 3.218 3.203 3.203 0 0 1-.865.115 3.23 3.23 0 0 1-.614-.057 3.283 3.283 0 0 0 3.067 2.277A6.588 6.588 0 0 1 .78 13.58a6.32 6.32 0 0 1-.78-.045A9.344 9.344 0 0 0 5.026 15z"/></svg>
                                    <small class="d-lg-none ms-2">Twitter</small>
                                    </li>
                                    """, unsafe_allow_html=True)


streamlit_antbit()






