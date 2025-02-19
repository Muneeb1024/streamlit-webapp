import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(
    page_title="Travel Website",
    page_icon="✈️",
    layout="wide"
)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 2rem;
    }
    .destination-card {
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #f0f0f0;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Create sample destination data
destinations = pd.DataFrame({
    'name': ['Paris', 'Tokyo', 'New York', 'Bali', 'London'],
    'country': ['France', 'Japan', 'USA', 'Indonesia', 'UK'],
    'price_per_day': [150, 200, 180, 100, 170],
    'description': [
        'The City of Light with iconic Eiffel Tower and world-class cuisine',
        'Modern metropolis with ancient temples and amazing street food',
        'The Big Apple with iconic skyline and diverse culture',
        'Tropical paradise with beautiful beaches and rich culture',
        'Historic city with royal heritage and modern attractions'
    ],
    'rating': [4.8, 4.7, 4.6, 4.9, 4.7]
})

def main():
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Destinations", "Book a Trip"])

    if page == "Home":
        show_home()
    elif page == "Destinations":
        show_destinations()
    else:
        show_booking()

def show_home():
    st.title("✈️ Welcome to Our Travel Website")
    st.subheader("Popular Destinations")
    
    # Display top 3 rated destinations
    top_destinations = destinations.nlargest(3, 'rating')
    
    cols = st.columns(3)
    for idx, (_, dest) in enumerate(top_destinations.iterrows()):
        with cols[idx]:
            st.markdown(f"### {dest['name']}, {dest['country']}")
            st.write(f"⭐ Rating: {dest['rating']}/5.0")
            st.write(dest['description'])
            st.write(f"💰 ${dest['price_per_day']} per day")
            if st.button(f"Book {dest['name']}", key=f"book_home_{dest['name']}"):
                st.session_state.selected_destination = dest['name']
                st.experimental_rerun()

def show_destinations():
    st.title("🌍 Explore Destinations")
    
    # Filters
    col1, col2 = st.columns(2)
    
    with col1:
        price_range = st.slider(
            "Price range per day ($)",
            0, 300, (50, 250)
        )
    
    with col2:
        selected_countries = st.multiselect(
            "Select Countries",
            options=destinations['country'].unique(),
            default=[]
        )
    
    # Filter destinations
    filtered_destinations = destinations[
        destinations['price_per_day'].between(price_range[0], price_range[1])
    ]
    
    if selected_countries:
        filtered_destinations = filtered_destinations[
            filtered_destinations['country'].isin(selected_countries)
        ]
    
    # Display filtered destinations
    for _, dest in filtered_destinations.iterrows():
        st.markdown("---")
        cols = st.columns([2, 1])
        
        with cols[0]:
            st.markdown(f"### {dest['name']}, {dest['country']}")
            st.write(dest['description'])
            st.write(f"⭐ Rating: {dest['rating']}/5.0")
        
        with cols[1]:
            st.write(f"💰 ${dest['price_per_day']} per day")
            if st.button(f"Book Now: {dest['name']}", key=f"book_{dest['name']}"):
                st.session_state.selected_destination = dest['name']
                st.experimental_rerun()

def show_booking():
    st.title("🎫 Book Your Trip")
    
    # Initialize session state for selected destination
    if 'selected_destination' not in st.session_state:
        st.session_state.selected_destination = destinations['name'].iloc[0]
    
    # Booking form
    col1, col2 = st.columns(2)
    
    with col1:
        # Destination selection
        destination = st.selectbox(
            "Select Destination",
            options=destinations['name'].tolist(),
            index=destinations['name'].tolist().index(st.session_state.selected_destination)
        )
        
        # Get destination details
        dest_info = destinations[destinations['name'] == destination].iloc[0]
        
        # Date selection
        start_date = st.date_input(
            "Start Date",
            min_value=datetime.now().date(),
            value=datetime.now().date() + timedelta(days=1)
        )
        
        # Duration selection
        duration = st.number_input(
            "Number of Days",
            min_value=1,
            max_value=30,
            value=7
        )
        
        # Number of travelers
        travelers = st.number_input(
            "Number of Travelers",
            min_value=1,
            max_value=10,
            value=2
        )
    
    with col2:
        st.markdown("### Trip Summary")
        st.write(f"Destination: {destination}, {dest_info['country']}")
        st.write(f"Check-in: {start_date}")
        st.write(f"Check-out: {start_date + timedelta(days=duration)}")
        
        # Calculate total price
        total_price = dest_info['price_per_day'] * duration * travelers
        st.write(f"Total Price: ${total_price:,.2f}")
        
        # Contact information
        st.markdown("### Contact Information")
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
    
    # Booking confirmation
    if st.button("Confirm Booking"):
        if name and email and phone:
            st.success(f"""
                ✅ Booking Confirmed!
                
                Thank you {name} for your booking!
                
                📍 Destination: {destination}, {dest_info['country']}
                📅 Dates: {start_date} to {start_date + timedelta(days=duration)}
                👥 Travelers: {travelers}
                💰 Total Cost: ${total_price:,.2f}
                
                A confirmation email has been sent to {email}.
            """)
        else:
            st.error("Please fill in all required contact information.")

if __name__ == "__main__":
    main()