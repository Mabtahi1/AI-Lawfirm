import streamlit as st
from datetime import datetime, timedelta
from services.email_service import EmailService

class EmailScheduler:
    """Schedule and send automated emails"""
    
    def __init__(self):
        self.email_service = EmailService()
    
    def check_trial_expiration(self):
        """Check for trials expiring soon and send reminders"""
        
        if 'subscriptions' not in st.session_state or 'users' not in st.session_state:
            return
        
        for org_code, subscription in st.session_state.subscriptions.items():
            if subscription.get('status') == 'trial':
                trial_end = datetime.fromisoformat(subscription['trial_end_date'])
                days_left = (trial_end - datetime.now()).days
                
                # Send reminders at 7 days, 3 days, and 1 day
                if days_left in [7, 3, 1]:
                    # Find user with this org_code
                    for email, user_info in st.session_state.users.items():
                        user_data = user_info['data']
                        if user_data.get('organization_code') == org_code:
                            # Check if we already sent this reminder
                            reminder_key = f"trial_reminder_{org_code}_{days_left}"
                            if reminder_key not in st.session_state.get('sent_reminders', set()):
                                self.email_service.send_trial_expiring_email(
                                    email,
                                    user_data['first_name'],
                                    days_left
                                )
                                
                                # Mark as sent
                                if 'sent_reminders' not in st.session_state:
                                    st.session_state.sent_reminders = set()
                                st.session_state.sent_reminders.add(reminder_key)
    
    def run_scheduled_tasks(self):
        """Run all scheduled email tasks"""
        self.check_trial_expiration()

