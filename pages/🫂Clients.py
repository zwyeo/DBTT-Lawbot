import streamlit as st
import pandas as pd
st.markdown("# Clients")
st.write("""Here you may find information of your clients!
""")

df = pd.read_csv("Customers.csv") 

df.fillna({'Name': 'Unknown', 'Category': 'Unknown', 'Age': 0 , 'Satisfaction': 0}, inplace=True)

client = st.text_input('Client Name:', " ")
if client:
    df = df[df["Name"].str.contains(client, case=False)]
    df = df.head(20)
    
# Diplaying results
    if not df.empty:
        st.write(f'Showing results for "{client}"')
        for index, row in df.iterrows():
            expander = st.expander(f"{row['Name']}")

            with expander:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Name:** {row['Name']}")
                with col2:
                    st.write(f"**Gender:** {row['Gender']}")
                with col3:
                    st.write(f"**Age:** {row['Age']}")

                col4, col5 = st.columns(2)
                with col4:
                    st.write(f"**Case Type:** {row['Category']}")
                with col5: 
                    star_rating = ":star:" * row['Satisfaction']
                    st.write(f"**Satisfaction:** {star_rating}")

    else:
        st.write("No results found, please try again!")

else:
    st.write("Please enter a client's name to search.")