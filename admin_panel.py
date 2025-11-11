# pages/admin.py

import streamlit as st
from services.local_storage import LocalStorage
import json

def show():
    st.title("🔧 Admin Panel")
    
    # Simple admin password check
    if 'admin_logged_in' not in st.session_state:
        st.session_state.admin_logged_in = False
    
    if not st.session_state.admin_logged_in:
        password = st.text_input("Admin Password", type="password")
        if st.button("Login"):
            if password == "admin123medi1369":  # Change this!
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Wrong password")
        st.stop()
    
    # Admin is logged in
    st.markdown("---")
    
    # Load all users
    all_users = LocalStorage.load_all_users()
    
    st.metric("Total Users", len(all_users))
    
    st.markdown("### 👥 Registered Users")
    
    if not all_users:
        st.info("No users registered yet")
        return
    
    # Display each user
    for email, user_data in all_users.items():
        with st.expander(f"📧 {email}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Name:** {user_data.get('name')}")
                st.write(f"**Organization:** {user_data.get('organization_name')}")
                st.write(f"**Org Code:** {user_data.get('organization_code')}")
                st.write(f"**Created:** {user_data.get('created_at', 'N/A')[:10]}")
            
            with col2:
                # Change plan
                new_plan = st.selectbox(
                    "Change Plan",
                    ["basic", "professional", "enterprise"],
                    key=f"plan_{email}"
                )
                
                if st.button("Update Plan", key=f"update_{email}"):
                    # Update subscription in session
                    org_code = user_data.get('organization_code')
                    if org_code in st.session_state.subscriptions:
                        st.session_state.subscriptions[org_code]['plan'] = new_plan
                    st.success(f"Plan updated to {new_plan}")
                
                # Delete user
                if st.button("🗑️ Delete User", key=f"delete_{email}"):
                    del all_users[email]
                    LocalStorage.save_all_users(all_users)
                    st.success("User deleted!")
                    st.rerun()

if __name__ == "__main__":
    show()
