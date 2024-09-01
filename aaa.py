import streamlit as st
st.title('Loan calculation app')
st.write('kindly enter yours details')
a=st.radio('Are you a govt emp',options=['yes','no'])
if a=='yes':
    st.write('you will this benefit')
else:
    st.write('ok')
b=st.checkbox('Are you looking loan')
if b==1:
    st.write('abcde')

x=st.number_input('enter your salary')

st.sidebar.write('policies')
z=st.sidebar.button('abc')
