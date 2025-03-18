import streamlit as st
from openai import OpenAI

st.title("Personalize Recommendation")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Initialize chat history with a system message (custom prompt)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": 
         "You are a customer retention specialist. "
         "Based on customer details, you provide two actionable suggestions to reduce churn risk."}
    ]

# User input fields for customer data
col1, col2 = st.columns(2)
with col1:
    Acw = st.number_input(
        "Insert number of weeks customer has had active account", value=65, placeholder="Type a number..."
    )

    Dtu = st.number_input(
        "Insert gigabytes of monthly data usage", value=0.29, placeholder="Type a number..."
    )

    CusCall = st.number_input(
        "Insert number of calls into customer service", value=4, placeholder="Type a number..."
    )

    Dmin = st.number_input(
        "Insert average daytime minutes per month", value=129.1, placeholder="Type a number..."
    )
    Renew = st.selectbox(
        "Does the user recently renew the contract?",
        ("Yes","No"),
        index=0,
        placeholder="Select...",
    )

with col2:
    Dcall = st.number_input(
        "Insert average number of daytime calls", value=137, placeholder="Type a number..."
    )

    Bill = st.number_input(
        "Insert average monthly bill", value=44.9, placeholder="Type a number..."
    )

    Ofee = st.number_input(
        "Insert largest overage fee in last 12 months", value=11.43, placeholder="Type a number..."
    )

    Roam = st.number_input(
        "Insert largest average number of roaming minutes", value=12.7, placeholder="Type a number..."
    )
    Dplan = st.selectbox(
        "Does the user has data plan?",
        ("Yes","No"),
        index=1,
        placeholder="Select...",
    )

# Submit button
if st.button("Get Churn Prevention Suggestions"):
    # Constructing the prompt with user input
    user_prompt = f"""
    Based on the following customer details, provide **two specific recommendations** to prevent churn:
    - **Account Age (Weeks):** {Acw}
    - **Contract Renewal (Yes=1, No=0):** {1 if Renew == "Yes" else 0}
    - **Has Data Plan (Yes=1, No=0):** {1 if Dplan == "Yes" else 0}
    - **Data Usage (GB per month):** {Dtu}
    - **Customer Service Calls (Number of calls):** {CusCall}
    - **Daytime Minutes Used:** {Dmin}
    - **Daytime Calls Made:** {Dcall}
    - **Monthly Charge ($):** {Bill}
    - **Overage Fee ($):** {Ofee}
    - **Roaming Minutes Used:** {Roam}

    Provide **two concrete suggestions** that can help reduce churn risk for this customer.
    """

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Generate assistant response
    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=st.session_state.messages,
    )

    # Extract response text
    bot_response = response.choices[0].message.content

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

    # Display response
    st.subheader("Churn Prevention Suggestions:")
    st.write(bot_response)
