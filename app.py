import streamlit as st
import pandas as pd
import pickle as pkl

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Car Price Prediction",
    page_icon="🚗",
    layout="centered"
)

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>
.stButton>button{
    width:100%;
    background-color:#4CAF50;
    color:white;
    border-radius:10px;
    height:3em;
    font-size:18px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Title
# -----------------------------
st.title("🚗 Car Price Prediction")
st.write("Enter the details of your car and click Predict Price.")

# -----------------------------
# Load Data
# -----------------------------
car = pd.read_csv("cleaned_data.csv")
pipe = pkl.load(open("CPP.pkl","rb"))

# -----------------------------
# Dropdown Values
# -----------------------------
companies = sorted(car["company"].unique())
fuel_types = sorted(car["fuel_type"].unique())
years = sorted(car["year"].unique(), reverse=True)

# -----------------------------
# User Inputs
# -----------------------------
company = st.selectbox(
    "🏢 Select Company",
    companies
)

models = sorted(
    car[car["company"] == company]["name"].unique()
)

name = st.selectbox(
    "🚘 Select Car Model",
    models
)

fuel_type = st.selectbox(
    "⛽ Select Fuel Type",
    fuel_types
)

year = st.selectbox(
    "📅 Select Manufacturing Year",
    years
)

kms_driven = st.number_input(
    "🛣️ Kilometers Driven",
    min_value=0,
    value=50000,
    step=1000
)

predict = st.button("🚗 Predict Price")

# -----------------------------
# Prediction
# -----------------------------
if predict:

    input_df = pd.DataFrame(
        [[company, name, year, kms_driven, fuel_type]],
        columns=[
            "company",
            "name",
            "year",
            "kms_driven",
            "fuel_type"
        ]
    )

    try:

        prediction = pipe.predict(input_df)

        price = float(prediction[0][0]) if hasattr(prediction[0], "__len__") else float(prediction[0])

        st.success("Prediction Successful ✅")

        st.metric(
            "Estimated Price",
            f"₹ {price:,.0f}"
        )

        if price < 300000:
            st.info("🚗 Budget Car")

        elif price < 800000:
            st.warning("🚙 Mid Range Car")

        else:
            st.success("🚘 Premium Car")

        st.balloons()

    except Exception as e:
        st.error("Prediction Error")
        st.write(e)

st.markdown("---")
st.caption("Made with ❤️ by Chhaya Killedar")
