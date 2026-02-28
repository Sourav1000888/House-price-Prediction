import streamlit as st
import pandas as pd
import joblib
import numpy as np
from datetime import datetime

# House price prediction

columns = joblib.load('x.pkl')
model = joblib.load('pipeline.pkl')


#prediction function
def predict_house_price(location, total_sqft, bath, balcony, bhk):
    # predict input data
    prediction = model.predict(pd.DataFrame([[location, total_sqft, bath, balcony, bhk]], 
                        columns=['location', 'total_sqft', 'bath', 'balcony', 'bhk']))[0]
    
    # divide by 100, for lakhs convert into crores
    return prediction

# Initialize session state for history
if "history" not in st.session_state:
    st.session_state.history = []

# Header
st.title("House Price Prediction System")
st.markdown("Predict house prices based on location, size, and features.")

# Sidebar
st.sidebar.header("Quick Actions")
if st.sidebar.button("New Prediction"):
    st.rerun()

st.sidebar.header("Filters")
currency = st.sidebar.selectbox("Currency", ["INR (Lakhs)", "USD"])  # Optional



# Main Content with Tabs
tab1, tab2 = st.tabs(["Predict", "History"])

#Predict tab
with tab1:
    st.header("Enter House Details")
    
    # Input fields
    location = st.selectbox("Location", sorted(set(columns['location'])))
    total_square_feet = pd.Series(np.expm1(columns['total_sqft'])).astype(int)
    total_sqft = st.selectbox('Choose Square Feets :', options=sorted(set(total_square_feet)))
    bath = st.selectbox('Bathrooms', set(columns['bath'].astype(int)))
    balcony = st.selectbox('Balconies', set(columns['balcony'].astype(int)))
    bhk = st.selectbox('BHK', set(columns['bhk']))

    #Predict button
    if st.button("Predict Price", use_container_width=True, type='primary'):
        predicted_price = predict_house_price(location, total_sqft, bath, balcony, bhk)
        predicted_price = round(predicted_price, 2)
        if currency == 'INR (Lakhs)':
            st.success(f"Predicted Price: {predicted_price} Lakhs INR")
        elif currency == 'USD':
            st.success(f"Predicted Price: {round(predicted_price*0.010894, 2)} USD")

        
        # Display details
        st.subheader("Prediction Details")
        st.write(f"**Location:** {location}")
        st.write(f"**Total Sqft:** {total_sqft}")
        st.write(f"**Bathrooms:** {bath}")
        st.write(f"**Balconies:** {balcony}")
        st.write(f"**BHK:** {bhk}")
        
        # Add to history
        st.session_state.history.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "location": location,
            "total_sqft": total_sqft,
            "bath": bath,
            "balcony": balcony,
            "bhk": bhk,
            "predicted_price": f'{predicted_price} lakhs INR' if currency == 'INR (Lakhs)' else f'{round(predicted_price*0.010894, 2)} USD'
        })

#History tab
with tab2:
    st.header("Prediction History")
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df)
        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()
    else:
        st.write("No history yet.")

