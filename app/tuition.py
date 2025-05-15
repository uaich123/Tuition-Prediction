import streamlit as st
import pandas as pd
import joblib

st.markdown("Enter your program details to estimate the tuition fee.")
st.write("If there is a huge disrepency between the predicted tuition and the actual tuition, then make sure that "
"you have entered all the data correctly. For example, Harvard University is in the U.S., not U.K. " \
"and the correct city spelling is 'Cambridge' not 'Cambrige'. ")
st.write("Also, make sure to type in the full name of the program; for example, " \
"Computer Science, not Comp Sci. or CS.")
st.write("Write down the university exactly as it appears in the list below. For example," \
"write Georgia Tech instead of Georgia Tech University or Georgia Institute of Technology.")

st.write("""Please note that this tool covers a total of 622 universities, so your university might not " \
"be listed here." \

\

You might have to try different abbreviations of the university to find it. For example, \
MIT is listed as **MIT**, not Massachusetts Institute of Technology.""")
df = pd.read_csv("Data/International_Education_Costs.csv")
text_search = st.text_input("Search for a university:")
if text_search:
    mask = df['University'].str.contains(text_search, case=False)
    matches = df[mask]
    if not matches.empty:
        matches.drop_duplicates(inplace=True)
        keep_cols = ['University', 'City', 'Country']
        goodbye_cols = [col for col in df.columns if col not in keep_cols]
        matches.drop(columns = goodbye_cols, inplace=True)
        matches = pd.DataFrame({"University":matches["University"], "City": matches["City"], "Country": matches["Country"]})
        st.dataframe(matches.drop_duplicates(), hide_index=True)
    else:
        st.warning("No university found.")


country = st.sidebar.selectbox("Country", ["USA", "UK", "Germany", "Canada", "Australia"])
city = st.sidebar.text_input("City", "Cambridge")
university = st.sidebar.text_input("University", "Harvard University")
program = st.sidebar.text_input("Program", "Computer Science")
level = st.sidebar.selectbox("Degree Level", ["Undergraduate", "Master", "PhD"])
duration = st.sidebar.number_input("Program Duration (Years)", min_value=0.5, max_value=10.0, value=2.0, step=0.5)
rent = st.sidebar.number_input("Monthly Rent (USD)", min_value=100, max_value=5000, value=1200)
insurance = st.sidebar.number_input("Annual Insurance (USD)", min_value=100, max_value=5000, value=1000)
visa_fee = st.sidebar.number_input("Visa Fee (USD)", min_value=0, max_value=1000, value=200)
living_index = st.sidebar.number_input("Living Cost Index", min_value=0.0, max_value=100.0, value=75.0, step=0.1)
exchange_rate = st.sidebar.number_input("Exchange Rate", min_value=0.1, max_value=5.0, value=1.0, step = 0.10)

input_data = pd.DataFrame([{
    'Country': country,
    'City': city,
    'University': university,
    'Program': program,
    'Level': level,
    'Duration_Years': duration,
    'Rent_USD': rent,
    'Insurance_USD': insurance,
    'Visa_Fee_USD': visa_fee,
    'Living_Cost_Index': living_index,
    'Exchange_Rate': exchange_rate
}])

model = joblib.load("./model/model.joblib")
categorical_cols = ['Country', 'City', 'University', 'Program', 'Level']
input_data[categorical_cols] = input_data[categorical_cols].astype(str)
if st.sidebar.button("Predict Tuition Cost"):
    prediction = model.predict(input_data)[0]
    st.subheader("Estimated Tuition Cost")
    st.success(f"${prediction:,.2f} USD")