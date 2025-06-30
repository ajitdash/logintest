import streamlit as st
import sys
import os

# Set page configuration
st.set_page_config(
    page_title="Authentication Dashboard",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Simple credential store for MVP (in production, this would be from a secure database)
VALID_CREDENTIALS = {
    "admin": "admin123",
    "auditor1": "audit2024",
    "user001": "access001",
    "demo": "demo123"
}

def initialize_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_id' not in st.session_state:
        st.session_state.user_id = ""
    if 'login_error' not in st.session_state:
        st.session_state.login_error = ""

def authenticate_user(user_id, access_key):
    """Validate user credentials"""
    if user_id in VALID_CREDENTIALS and VALID_CREDENTIALS[user_id] == access_key:
        return True
    return False

def login_screen():
    """Display the login screen"""
    st.title("🔐 Authentication Dashboard")
    st.markdown("---")
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("Login")
        
        # Create login form
        with st.form("login_form"):
            user_id = st.text_input("User ID", placeholder="Enter your User ID")
            access_key = st.text_input("Access Key", type="password", placeholder="Enter your Access Key")
            
            col_login, col_exit = st.columns(2)
            
            with col_login:
                login_button = st.form_submit_button("Login", use_container_width=True)
            
            with col_exit:
                exit_button = st.form_submit_button("Exit", use_container_width=True)
        
        # Handle login button click
        if login_button:
            if not user_id or not access_key:
                st.session_state.login_error = "Please enter both User ID and Access Key"
            elif authenticate_user(user_id, access_key):
                st.session_state.authenticated = True
                st.session_state.user_id = user_id
                st.session_state.login_error = ""
                st.success("Login successful! Redirecting to dashboard...")
                st.rerun()
            else:
                st.session_state.login_error = "Invalid User ID or Access Key"
        
        # Handle exit button click
        if exit_button:
            st.warning("Application terminated by user")
            st.stop()
        
        # Display error message if any
        if st.session_state.login_error:
            st.error(st.session_state.login_error)
        
        # Display valid credentials for demo purposes
        st.markdown("---")
        st.info("**Demo Credentials:**\n\n"
                "• User ID: `admin` | Access Key: `admin123`\n\n"
                "• User ID: `auditor1` | Access Key: `audit2024`\n\n"
                "• User ID: `user001` | Access Key: `access001`\n\n"
                "• User ID: `demo` | Access Key: `demo123`")

def auditor_suggestions_tab():
    """Content for Auditor Suggestions tab"""
    st.header("📋 Auditor Suggestions")
    st.markdown("---")
    
    # Add some example functionality for auditor suggestions
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Recent Suggestions")
        
        # Display message for empty state
        st.info("No auditor suggestions available at this time.")
        
        # Add form to create new suggestions
        st.subheader("Submit New Suggestion")
        with st.form("suggestion_form"):
            suggestion_title = st.text_input("Suggestion Title")
            suggestion_category = st.selectbox(
                "Category",
                ["Financial Controls", "Process Improvement", "Compliance", "Risk Management", "Other"]
            )
            suggestion_priority = st.selectbox(
                "Priority",
                ["Low", "Medium", "High", "Critical"]
            )
            suggestion_description = st.text_area("Description", height=100)
            
            submitted = st.form_submit_button("Submit Suggestion")
            
            if submitted:
                if suggestion_title and suggestion_description:
                    st.success(f"Suggestion '{suggestion_title}' submitted successfully!")
                else:
                    st.error("Please fill in all required fields (Title and Description)")
    
    with col2:
        st.subheader("Statistics")
        st.metric("Total Suggestions", "0")
        st.metric("Pending Review", "0")
        st.metric("Implemented", "0")
        st.metric("In Progress", "0")

def activity_logs_tab():
    """Content for Activity Logs tab"""
    st.header("📊 Activity Logs")
    st.markdown("---")
    
    # Add filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        log_type = st.selectbox(
            "Log Type",
            ["All", "Login", "Logout", "Data Access", "System Changes", "Error"]
        )
    
    with col2:
        date_filter = st.date_input("Date Filter")
    
    with col3:
        user_filter = st.text_input("User Filter", placeholder="Filter by user...")
    
    # Search and filter buttons
    col_search, col_export = st.columns([1, 1])
    with col_search:
        if st.button("Apply Filters", use_container_width=True):
            st.info("Filters applied successfully")
    
    with col_export:
        if st.button("Export Logs", use_container_width=True):
            st.info("Export functionality would be implemented here")
    
    st.markdown("---")
    
    # Display logs area
    st.subheader("Activity Log Entries")
    
    # Display message for empty state
    st.info("No activity logs available at this time.")
    
    # Add some example log structure (but no fake data)
    with st.expander("Log Entry Structure"):
        st.json({
            "timestamp": "ISO 8601 format",
            "user_id": "string",
            "action": "string",
            "resource": "string",
            "ip_address": "string",
            "status": "success/failure",
            "details": "string"
        })

def dashboard():
    """Display the main dashboard with tabs"""
    # Header with user info and logout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title("📊 Dashboard")
        st.caption(f"Welcome, {st.session_state.user_id}")
    
    with col2:
        if st.button("Logout", use_container_width=True):
            # Clear session state
            st.session_state.authenticated = False
            st.session_state.user_id = ""
            st.session_state.login_error = ""
            st.success("Logged out successfully!")
            st.rerun()
    
    st.markdown("---")
    
    # Create tabs
    tab1, tab2 = st.tabs(["📋 Auditor Suggestions", "📊 Activity Logs"])
    
    with tab1:
        auditor_suggestions_tab()
    
    with tab2:
        activity_logs_tab()

def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Route to appropriate screen based on authentication status
    if st.session_state.authenticated:
        dashboard()
    else:
        login_screen()

# Run the application
if __name__ == "__main__":
    main()
