import streamlit as st
# Title of the app
st.title('Welcome to Streamlit!')

# To check weather person is eligible for vote or not
age = st.number_input('Enter your age')

st.write("You have entered Age: ", age)

if age < 18:
    st.write("You are not eligible for vote")
else:
    st.write("You are eligible for vote")