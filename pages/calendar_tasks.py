import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import calendar
import json
import os

# ADD THIS IMPORT
from services.data_security import DataSecurity

# KEEP ONLY THIS:
def auto_save_calendar_data():
    """SECURE auto-save calendar data"""
    from services.data_security import DataSecurity
    
    if 'events' in st.session_state:
        DataSecurity.save_user_data('events', st.session_state.events)
    
    if 'tasks' in st.session_state:
        DataSecurity.save_user_data('tasks', st.session_state.tasks)
    
    if 'court_deadlines' in st.session_state:
        DataSecurity.save_user_data('court_deadlines', st.session_state.court_deadlines)

def show():
     from services.data_security import DataSecurity
    
    # Require authentication
    DataSecurity.require_auth("Calendar & Tasks")
        
    # Professional header styling
    st.markdown("""
    <style>
    /* Match main app background */
    .stApp {
        background: linear-gradient(135deg, 
            #1a0b2e 0%,
            #2d1b4e 15%,
            #1e3a8a 35%,
            #0f172a 50%,
            #1e3a8a 65%,
            #16537e 85%,
            #0891b2 100%) !important;
        min-height: 100vh;
        position: relative;
    }
    
    /* Geometric overlay pattern */
    .stApp::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(168, 85, 247, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(14, 165, 233, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(59, 130, 246, 0.05) 0%, transparent 50%);
        pointer-events: none;
    }
    /* Sidebar styling - must be in each page file */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%) !important;
        padding: 0 !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding: 2rem 1rem !important;
    }
    
    [data-testid="stSidebar"] .css-17eq0hr {
        color: white !important;
    }
    
    [data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] button {
        background: rgba(255,255,255,0.15) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        width: 100% !important;
    }
    
    [data-testid="stSidebar"] button:hover {
        background: rgba(255,255,255,0.25) !important;
    }
    .ai-header {
        background: rgba(30, 58, 138, 0.6);
        backdrop-filter: blur(10px);
        padding: 3rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    .ai-header h1 {
        color: white;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    /* Default: Light text everywhere EXCEPT inside white containers */
    body, .stApp, p, span, div {
        color: #e2e8f0;
    }
    
    /* Headers - light */
    h1, h2, h3, h4, h5, h6 {
        color: #f1f5f9 !important;
    }
    
    /* Dark text ONLY inside white expander boxes */
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
        background: white !important;
    }
    
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] * {
        color: #1e293b !important;
    }
    
    /* Query Suggestions - white boxes with dark text */
    .element-container:has(.stButton) {
        background: white !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
    }
    
    .element-container:has(.stButton) * {
        color: #1e293b !important;
    }
    
    /* Any white/light background containers should have dark text */
    [style*="background: white"],
    [style*="background: #fff"],
    [style*="background-color: white"],
    [style*="background-color: #fff"],
    [style*="background: rgb(255, 255, 255)"] {
        color: #1e293b !important;
    }
    
    [style*="background: white"] *,
    [style*="background: #fff"] *,
    [style*="background-color: white"] *,
    [style*="background-color: #fff"] *,
    [style*="background: rgb(255, 255, 255)"] * {
        color: #1e293b !important;
    }
    
    /* White containers in general */
    .stContainer[style*="background"],
    div[style*="background: white"],
    div[style*="background-color: white"],
    div[style*="background: #ffffff"] {
        background: white !important;
    }
    
    .stContainer[style*="background"] *,
    div[style*="background: white"] *,
    div[style*="background-color: white"] *,
    div[style*="background: #ffffff"] * {
        color: #1e293b !important;
    }
    
    /* Markdown content in white boxes */
    .stMarkdown[style*="background"] * {
        color: #1e293b !important;
    }
    
    /* Dark text in forms */
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.95) !important;
    }
    
    [data-testid="stForm"] * {
        color: #1e293b !important;
    }
    
    /* Metrics - keep colored */
    [data-testid="stMetricValue"] {
        color: #60a5fa !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #cbd5e1 !important;
    }
    
    /* Input fields */
    input, textarea, select {
        color: #1e293b !important;
        background: white !important;
    }
    
    /* Buttons */
    .stButton button * {
        color: white !important;
    }
    
    /* Info/warning/error boxes - keep light text */
    .stAlert, .stSuccess, .stWarning, .stError, .stInfo {
        color: #1e293b !important;
    }

    /* Dropdown menus - comprehensive fix */
    .stSelectbox,
    [data-testid="stSelectbox"] {
        background: white !important;
        border-radius: 8px !important;
    }
    
    .stSelectbox [data-baseweb="select"],
    [data-testid="stSelectbox"] [data-baseweb="select"],
    .stSelectbox [data-baseweb="select"] > div,
    [data-testid="stSelectbox"] [data-baseweb="select"] > div {
        background: white !important;
        color: #1e293b !important;
    }
    
    .stSelectbox [data-baseweb="select"] *,
    [data-testid="stSelectbox"] [data-baseweb="select"] * {
        color: #1e293b !important;
    }
    
    [data-baseweb="popover"],
    [role="listbox"],
    [data-baseweb="menu"] {
        background: white !important;
    }
    
    [data-baseweb="popover"] *,
    [role="listbox"] *,
    [role="option"],
    [role="option"] *,
    [data-baseweb="menu"] li,
    [data-baseweb="menu"] li * {
        color: #1e293b !important;
        background: white !important;
    }
    
    [aria-selected="true"] {
        background: rgba(59, 130, 246, 0.1) !important;
        color: #1e293b !important;
    }
    
    [role="option"]:hover,
    [data-baseweb="menu"] li:hover {
        background: rgba(59, 130, 246, 0.15) !important;
        color: #1e293b !important;
    }
    
    .stMultiSelect [data-baseweb="tag"],
    .stMultiSelect [data-baseweb="tag"] * {
        background: rgba(59, 130, 246, 0.2) !important;
        color: #1e293b !important;
    }
    
    .stSelectbox svg,
    [data-testid="stSelectbox"] svg {
        fill: #1e293b !important;
    }

    div[data-baseweb="select"] {
        background: white !important;
    }
    
    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] > div > div,
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] input {
        color: #1e293b !important;
        background: white !important;
    }
    
    ul[role="listbox"] {
        background: white !important;
    }
    
    ul[role="listbox"] li,
    ul[role="listbox"] li * {
        color: #1e293b !important;
    }
    
    [data-baseweb="select"] [data-baseweb="select-dropdown"] *,
    [data-baseweb="popover-content"] *,
    .stSelectbox * {
        color: #1e293b !important;
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        border-left: 4px solid #3b82f6;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        background-color: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(10px);
        border-radius: 8px;
        font-weight: 600;
        color: #cbd5e1;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(59, 130, 246, 0.8);
        color: white;
    }
    </style>
    <div class="ai-header">
        <h1>📅 Calendar & Tasks</h1>
        <p>Manage deadlines, appointments, and to-do lists</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize real user data
    user_email = st.session_state.get('user_data', {}).get('email', 'demo@example.com')
    
    # SECURE DATA LOADING
    if 'events' not in st.session_state:
        st.session_state.events = DataSecurity.get_user_events()
    
    if 'tasks' not in st.session_state:
        st.session_state.tasks = DataSecurity.get_user_tasks()
    
    if 'court_deadlines' not in st.session_state:
        st.session_state.court_deadlines = DataSecurity.load_user_data('court_deadlines', [])
    
    # Calendar tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📅 Calendar View", 
        "✅ Task Management", 
        "⚖️ Court Deadlines", 
        "📋 Matter Schedule"
    ])
    
    with tab1:
        show_calendar_view()
    
    with tab2:
        show_task_management()
    
    with tab3:
        show_court_deadlines()
    
    with tab4:
        show_matter_schedule()

def show_calendar_view():
    st.subheader("📅 Calendar Overview")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Calendar controls
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            view_type = st.selectbox("View:", ["Month", "Week", "Day", "Agenda"])
        with col_b:
            selected_date = st.date_input("Date:", datetime.now())
        with col_c:
            filter_type = st.selectbox("Filter:", ["All Events", "Meetings", "Deadlines", "Court Dates"])
        
        # Calendar display
        st.markdown("#### Calendar Events")
        
        if not st.session_state.events:
            st.info("📅 No events yet. Add your first event using the form on the right.")
        
        for event in st.session_state.events:
            with st.expander(f"{event.get('time', 'N/A')} - {event.get('title', 'Untitled')}"):
                col_x, col_y = st.columns(2)
                with col_x:
                    st.write(f"**Type:** {event.get('type', 'N/A')}")
                    st.write(f"**Duration:** {event.get('duration', 'N/A')}")
                with col_y:
                    st.write(f"**Location:** {event.get('location', 'N/A')}")
                    st.write(f"**Attendees:** {event.get('attendees', 'N/A')}")
                
                col_action1, col_action2, col_action3 = st.columns(3)
                with col_action1:
                    if st.button("✏️ Edit", key=f"edit_event_{event.get('id')}"):
                        st.session_state.editing_event_id = event.get('id')
                        st.info(f"Editing: {event.get('title')}")
                        st.rerun()
                
                with col_action2:
                    if st.button("📧 Notify", key=f"notify_event_{event.get('id')}"):
                        st.success(f"✓ Notifications sent for {event.get('title')}")
                
                with col_action3:
                    if st.button("🗑️ Delete", key=f"delete_event_{event.get('id')}"):
                        st.session_state.events = [e for e in st.session_state.events if e.get('id') != event.get('id')]
                        auto_save_calendar_data()
                        st.success(f"✓ Event '{event.get('title')}' deleted")
                        st.rerun()
    
    with col2:
        st.markdown("#### Quick Add Event")
        
        with st.form("add_event"):
            event_title = st.text_input("Event Title:")
            event_date = st.date_input("Date:")
            event_time = st.time_input("Time:")
            event_type = st.selectbox("Type:", ["Meeting", "Deadline", "Court Date", "Other"])
            event_duration = st.selectbox("Duration:", ["15 min", "30 min", "1 hour", "2 hours", "All day"])
            event_location = st.text_input("Location:", value="Office")
            event_attendees = st.text_input("Attendees:", value="Team")
            
            if st.form_submit_button("➕ Add Event"):
                if event_title:
                    new_event = {
                        "id": len(st.session_state.events) + 1,
                        "time": event_time.strftime("%I:%M %p"),
                        "date": event_date.strftime("%Y-%m-%d"),
                        "title": event_title,
                        "type": event_type,
                        "duration": event_duration,
                        "location": event_location,
                        "attendees": event_attendees
                    }
                    st.session_state.events.append(new_event)
                    auto_save_calendar_data()
                    st.success(f"✓ Event '{event_title}' added successfully!")
                    st.rerun()
                else:
                    st.error("Please enter an event title")
        
        st.markdown("#### Today's Summary")
        total_events = len(st.session_state.events)
        meetings = len([e for e in st.session_state.events if e.get('type') == 'Meeting'])
        deadlines = len([e for e in st.session_state.events if e.get('type') == 'Deadline'])
        court_dates = len([e for e in st.session_state.events if e.get('type') == 'Court Date'])
        
        st.metric("Total Events", total_events)
        st.metric("Meetings", meetings)
        st.metric("Deadlines", deadlines)
        st.metric("Court Dates", court_dates)

def show_task_management():
    st.subheader("✅ Task Management Dashboard")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Task filters
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            task_filter = st.selectbox("Filter by:", ["All Tasks", "My Tasks", "Overdue", "This Week"])
        with col_b:
            priority_filter = st.selectbox("Priority:", ["All", "High", "Medium", "Low"])
        with col_c:
            status_filter = st.selectbox("Status:", ["All", "Pending", "In Progress", "Completed"])
        
        # Task list
        st.markdown("#### Task List")
        
        if not st.session_state.tasks:
            st.info("✅ No tasks yet. Create your first task using the form on the right.")
        
        # Apply filters
        filtered_tasks = st.session_state.tasks
        
        if priority_filter != "All":
            filtered_tasks = [t for t in filtered_tasks if t.get('priority') == priority_filter]
        
        if status_filter != "All":
            filtered_tasks = [t for t in filtered_tasks if t.get('status') == status_filter]
        
        for task in filtered_tasks:
            priority_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
            status_color = {"Pending": "⭕", "In Progress": "🔄", "Completed": "✅"}
            
            with st.expander(f"{priority_color.get(task.get('priority'), '⚪')} {task.get('title', 'Untitled')} - Due: {task.get('due_date', 'N/A')}"):
                col_x, col_y = st.columns(2)
                with col_x:
                    st.write(f"**Assignee:** {task.get('assignee', 'Unassigned')}")
                    st.write(f"**Matter:** {task.get('matter', 'N/A')}")
                    st.write(f"**Status:** {status_color.get(task.get('status'), '❓')} {task.get('status', 'Unknown')}")
                with col_y:
                    st.write(f"**Priority:** {task.get('priority', 'N/A')}")
                    st.write(f"**Task ID:** {task.get('id', 'N/A')}")
                    st.progress(task.get('progress', 0) / 100)
                
                if task.get('description'):
                    st.write(f"**Description:** {task.get('description')}")
                
                # Task actions
                col_action1, col_action2, col_action3, col_action4 = st.columns(4)
                
                with col_action1:
                    if st.button("✏️ Edit", key=f"edit_task_{task.get('id')}"):
                        st.session_state.editing_task_id = task.get('id')
                        st.info(f"Editing task: {task.get('title')}")
                
                with col_action2:
                    if task.get('status') != 'Completed':
                        if st.button("✓ Complete", key=f"complete_task_{task.get('id')}"):
                            for t in st.session_state.tasks:
                                if t.get('id') == task.get('id'):
                                    t['status'] = 'Completed'
                                    t['progress'] = 100
                                    auto_save_calendar_data()
                                    st.success(f"✓ Task '{task.get('title')}' completed!")
                                    st.rerun()
                
                with col_action3:
                    if st.button("💬 Comment", key=f"comment_task_{task.get('id')}"):
                        st.info(f"Add comment to: {task.get('title')}")
                
                with col_action4:
                    if st.button("🗑️ Delete", key=f"delete_task_{task.get('id')}"):
                        st.session_state.tasks = [t for t in st.session_state.tasks if t.get('id') != task.get('id')]
                        auto_save_calendar_data()
                        st.success(f"✓ Task deleted")
                        st.rerun()
    
    with col2:
        st.markdown("#### Create New Task")
        
        # Get matters for dropdown
        matters = st.session_state.get('matters', [])
        if matters:
            matter_names = [m.get('name', 'Untitled') if isinstance(m, dict) else getattr(m, 'name', 'Untitled') for m in matters]
        else:
            matter_names = ["General"]
        
        with st.form("new_task"):
            task_title = st.text_input("Task Title:")
            task_assignee = st.text_input("Assign to:", value=st.session_state.get('user_data', {}).get('name', 'Me'))
            task_priority = st.selectbox("Priority:", ["High", "Medium", "Low"])
            task_due = st.date_input("Due Date:")
            task_matter = st.selectbox("Related Matter:", matter_names)
            task_description = st.text_area("Description:")
            
            if st.form_submit_button("➕ Create Task"):
                if task_title:
                    new_task = {
                        "id": f"T{len(st.session_state.tasks) + 1:03d}",
                        "title": task_title,
                        "assignee": task_assignee,
                        "priority": task_priority,
                        "status": "Pending",
                        "due_date": task_due.strftime("%Y-%m-%d"),
                        "matter": task_matter,
                        "progress": 0,
                        "description": task_description
                    }
                    st.session_state.tasks.append(new_task)
                    auto_save_calendar_data()
                    st.success(f"✓ Task '{task_title}' created successfully!")
                    st.rerun()
                else:
                    st.error("Please enter a task title")
        
        st.markdown("#### Task Statistics")
        total_tasks = len(st.session_state.tasks)
        completed_tasks = len([t for t in st.session_state.tasks if t.get('status') == 'Completed'])
        pending_tasks = len([t for t in st.session_state.tasks if t.get('status') == 'Pending'])
        high_priority = len([t for t in st.session_state.tasks if t.get('priority') == 'High'])
        
        st.metric("Total Tasks", total_tasks)
        st.metric("Completed", completed_tasks)
        st.metric("Pending", pending_tasks)
        st.metric("High Priority", high_priority)

def show_court_deadlines():
    st.subheader("⚖️ Court Deadlines & Filing Management")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("#### Upcoming Court Deadlines")
        
        # Deadline filters
        col_a, col_b = st.columns(2)
        with col_a:
            deadline_filter = st.selectbox("Time Frame:", ["Next 30 Days", "Next 7 Days", "Overdue", "All"])
        with col_b:
            court_filter = st.selectbox("Court:", ["All Courts", "Federal Court", "State Court", "Superior Court"])
        
        if not st.session_state.court_deadlines:
            st.info("⚖️ No court deadlines yet. Add your first deadline using the form on the right.")
        
        # Deadlines list
        for deadline in st.session_state.court_deadlines:
            # Calculate days remaining
            due_date_str = deadline.get('due_date', '')
            if due_date_str:
                try:
                    due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
                    days_remaining = (due_date - datetime.now()).days
                except:
                    days_remaining = 0
            else:
                days_remaining = 0
            
            # Color coding based on urgency
            if days_remaining <= 1:
                urgency_color = "🔴"
                border_color = "red"
            elif days_remaining <= 7:
                urgency_color = "🟡"
                border_color = "orange"
            else:
                urgency_color = "🟢"
                border_color = "green"
            
            st.markdown(f"""
            <div style="border-left: 4px solid {border_color}; padding-left: 10px; margin: 10px 0;">
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander(f"{urgency_color} {deadline.get('deadline_type', 'Deadline')} - {deadline.get('case', 'Unknown')} (Due: {due_date_str})"):
                col_x, col_y = st.columns(2)
                with col_x:
                    st.write(f"**Court:** {deadline.get('court', 'N/A')}")
                    st.write(f"**Assigned:** {deadline.get('assigned', 'Unassigned')}")
                with col_y:
                    st.write(f"**Status:** {deadline.get('status', 'Pending')}")
                    st.write(f"**Days Remaining:** {days_remaining}")
                
                # Action buttons
                col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
                with col_btn1:
                    if st.button("📄 View Details", key=f"view_deadline_{deadline.get('id')}"):
                        st.info(f"Viewing details for: {deadline.get('case')}")
                
                with col_btn2:
                    if st.button("📝 Update Status", key=f"status_deadline_{deadline.get('id')}"):
                        st.info("Update status form...")
                
                with col_btn3:
                    if st.button("📧 Send Reminder", key=f"remind_deadline_{deadline.get('id')}"):
                        st.success("Reminder sent!")
                
                with col_btn4:
                    if st.button("🗑️ Delete", key=f"delete_deadline_{deadline.get('id')}"):
                        st.session_state.court_deadlines = [d for d in st.session_state.court_deadlines if d.get('id') != deadline.get('id')]
                        auto_save_calendar_data()
                        st.success("Deadline deleted")
                        st.rerun()
    
    with col2:
        st.markdown("#### Add Court Deadline")
        
        with st.form("add_deadline"):
            case_name = st.text_input("Case Name:")
            deadline_type = st.selectbox("Deadline Type:", [
                "Motion to Dismiss",
                "Discovery Response",
                "Regulatory Filing",
                "Summary Judgment Brief",
                "Other"
            ])
            due_date = st.date_input("Due Date:")
            court = st.selectbox("Court:", ["Federal Court", "State Court", "Superior Court", "Other"])
            assigned_to = st.text_input("Assigned To:", value=st.session_state.get('user_data', {}).get('name', 'Me'))
            status = st.selectbox("Status:", ["Pending", "In Progress", "Draft Complete", "Filed"])
            
            if st.form_submit_button("➕ Add Deadline"):
                if case_name and deadline_type:
                    new_deadline = {
                        "id": len(st.session_state.court_deadlines) + 1,
                        "case": case_name,
                        "deadline_type": deadline_type,
                        "due_date": due_date.strftime("%Y-%m-%d"),
                        "court": court,
                        "assigned": assigned_to,
                        "status": status
                    }
                    st.session_state.court_deadlines.append(new_deadline)
                    auto_save_calendar_data()
                    st.success(f"✓ Deadline added: {deadline_type} for {case_name}")
                    st.rerun()
                else:
                    st.error("Please fill in case name and deadline type")
        
        st.markdown("#### Deadline Statistics")
        total_deadlines = len(st.session_state.court_deadlines)
        
        # Count urgent deadlines
        urgent = 0
        for d in st.session_state.court_deadlines:
            due_date_str = d.get('due_date', '')
            if due_date_str:
                try:
                    due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
                    days_remaining = (due_date - datetime.now()).days
                    if days_remaining <= 7:
                        urgent += 1
                except:
                    pass
        
        st.metric("Total Deadlines", total_deadlines)
        st.metric("Urgent (7 days)", urgent)

def show_matter_schedule():
    st.subheader("📋 Matter Schedule & Milestones")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Get matters
        matters = st.session_state.get('matters', [])
        
        if not matters:
            st.info("📋 No matters available. Create matters in Matter Management first.")
            return
        
        # Matter selection
        matter_names = [m.get('name', 'Untitled') if isinstance(m, dict) else getattr(m, 'name', 'Untitled') for m in matters]
        selected_matter = st.selectbox("Select Matter:", matter_names)
        
        st.markdown(f"#### Timeline for {selected_matter}")
        
        # Get selected matter details
        selected_matter_obj = None
        for m in matters:
            matter_name = m.get('name', 'Untitled') if isinstance(m, dict) else getattr(m, 'name', 'Untitled')
            if matter_name == selected_matter:
                selected_matter_obj = m
                break
        
        if selected_matter_obj:
            # Show matter details
            col_detail1, col_detail2 = st.columns(2)
            
            with col_detail1:
                client = selected_matter_obj.get('client_name', 'N/A') if isinstance(selected_matter_obj, dict) else getattr(selected_matter_obj, 'client_name', 'N/A')
                status = selected_matter_obj.get('status', 'N/A') if isinstance(selected_matter_obj, dict) else getattr(selected_matter_obj, 'status', 'N/A')
                st.write(f"**Client:** {client}")
                st.write(f"**Status:** {status}")
            
            with col_detail2:
                created = selected_matter_obj.get('created_date', 'N/A') if isinstance(selected_matter_obj, dict) else getattr(selected_matter_obj, 'created_date', 'N/A')
                if isinstance(created, datetime):
                    created = created.strftime('%Y-%m-%d')
                st.write(f"**Created:** {created}")
        
        # Timeline events (simplified)
        st.markdown("#### Matter Milestones")
        
        st.info("📅 Matter timeline and milestones coming soon. Track progress through tasks and calendar events.")
        
        st.markdown("#### Matter Resources")
        
        col_res1, col_res2, col_res3 = st.columns(3)
        with col_res1:
            if st.button("📁 View Documents"):
                st.success("✓ Opening document library...")
        with col_res2:
            if st.button("👥 Team Members"):
                st.success("✓ Opening team view...")
        with col_res3:
            if st.button("💰 Budget Tracking"):
                st.success("✓ Opening budget tracker...")
    
    with col2:
        st.markdown("#### Matter Progress")
        
        if selected_matter_obj:
            # Get actual progress from matter
            estimated_hours = selected_matter_obj.get('estimated_hours', 0) if isinstance(selected_matter_obj, dict) else getattr(selected_matter_obj, 'estimated_hours', 0)
            actual_hours = selected_matter_obj.get('actual_hours', 0) if isinstance(selected_matter_obj, dict) else getattr(selected_matter_obj, 'actual_hours', 0)
            budget = selected_matter_obj.get('budget', 0) if isinstance(selected_matter_obj, dict) else getattr(selected_matter_obj, 'budget', 0)
            
            progress = (actual_hours / estimated_hours * 100) if estimated_hours > 0 else 0
            
            st.metric("Overall Progress", f"{progress:.0f}%")
            st.progress(progress / 100)
            
            st.metric("Hours Logged", f"{actual_hours:.1f} / {estimated_hours:.1f}")
            st.metric("Budget", f"${budget:,.0f}")
        
        st.markdown("#### Quick Actions")
        
        if st.button("➕ Add Milestone"):
            st.info("Milestone feature coming soon...")
        
        if st.button("📊 View Timeline"):
            st.info("Timeline view coming soon...")
        
        if st.button("📧 Send Update"):
            st.info("Sending matter update...")

# Main application entry point
if __name__ == "__main__":
    show()
