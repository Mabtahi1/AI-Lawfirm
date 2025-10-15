import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

def show():
    """Display the Time & Billing page"""
    
    st.markdown("""
    <div class="main-header">
        <h1>💰 Time & Billing</h1>
        <p>Track billable hours, generate invoices, and manage client billing</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for time entries and invoices
    if 'time_entries' not in st.session_state:
        st.session_state.time_entries = load_sample_time_entries()
    
    if 'invoices' not in st.session_state:
        st.session_state.invoices = load_sample_invoices()
    
    # Quick stats at the top
    show_billing_metrics()
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "⏱️ Time Tracking", 
        "📄 Generate Invoice", 
        "💳 Invoices", 
        "📊 Reports", 
        "⚙️ Settings"
    ])
    
    with tab1:
        show_time_tracking()
    
    with tab2:
        show_invoice_generator()
    
    with tab3:
        show_invoices_list()
    
    with tab4:
        show_billing_reports()
    
    with tab5:
        show_billing_settings()

def show_billing_metrics():
    """Display key billing metrics"""
    
    time_entries = st.session_state.time_entries
    invoices = st.session_state.invoices
    
    # Calculate metrics
    unbilled_hours = sum(entry['hours'] for entry in time_entries if not entry['billed'])
    unbilled_amount = sum(entry['hours'] * entry['rate'] for entry in time_entries if not entry['billed'])
    
    outstanding_invoices = [inv for inv in invoices if inv['status'] == 'sent']
    outstanding_amount = sum(inv['total'] for inv in outstanding_invoices)
    
    paid_invoices = [inv for inv in invoices if inv['status'] == 'paid']
    paid_amount = sum(inv['total'] for inv in paid_invoices)
    
    # Calculate this month's billable hours
    current_month = datetime.now().month
    current_year = datetime.now().year
    this_month_hours = sum(
        entry['hours'] for entry in time_entries 
        if datetime.strptime(entry['date'], '%Y-%m-%d').month == current_month
        and datetime.strptime(entry['date'], '%Y-%m-%d').year == current_year
    )
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: #666; font-size: 0.9rem;">Unbilled Hours</h4>
            <h2 style="color: #2E86AB; margin: 0.5rem 0;">{:.1f} hrs</h2>
            <p style="color: #28a745; font-size: 0.85rem;">${:,.2f}</p>
        </div>
        """.format(unbilled_hours, unbilled_amount), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: #666; font-size: 0.9rem;">Outstanding</h4>
            <h2 style="color: #ffc107; margin: 0.5rem 0;">${:,.2f}</h2>
            <p style="color: #666; font-size: 0.85rem;">{} invoices</p>
        </div>
        """.format(outstanding_amount, len(outstanding_invoices)), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: #666; font-size: 0.9rem;">Paid This Month</h4>
            <h2 style="color: #28a745; margin: 0.5rem 0;">${:,.2f}</h2>
            <p style="color: #666; font-size: 0.85rem;">{} invoices</p>
        </div>
        """.format(paid_amount, len(paid_invoices)), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: #666; font-size: 0.9rem;">Hours This Month</h4>
            <h2 style="color: #2E86AB; margin: 0.5rem 0;">{:.1f} hrs</h2>
            <p style="color: #666; font-size: 0.85rem;">Billable time</p>
        </div>
        """.format(this_month_hours), unsafe_allow_html=True)

def show_time_tracking():
    """Time tracking interface"""
    
    st.markdown("### ⏱️ Time Entry")
    
    # Quick timer at the top
    col_timer1, col_timer2 = st.columns([2, 1])
    
    with col_timer1:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 16px;
            margin-bottom: 1rem;
        ">
            <h3 style="margin: 0 0 0.5rem 0;">Quick Timer</h3>
            <h1 style="margin: 0; font-size: 3rem;">00:00:00</h1>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Click Start to begin tracking time</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_timer2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("▶️ Start Timer", use_container_width=True, type="primary"):
            st.info("Timer feature coming soon!")
        if st.button("⏸️ Pause", use_container_width=True):
            st.info("Timer feature coming soon!")
        if st.button("⏹️ Stop & Save", use_container_width=True):
            st.info("Timer feature coming soon!")
    
    st.markdown("---")
    
    # Manual time entry form
    st.markdown("### 📝 Manual Time Entry")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Get matters for dropdown
        matters = st.session_state.get('matters', [])
        matter_options = ["Select a matter..."] + [m['title'] for m in matters]
        
        with st.form("time_entry_form"):
            selected_matter = st.selectbox("Matter/Case", matter_options)
            
            col_form1, col_form2 = st.columns(2)
            
            with col_form1:
                entry_date = st.date_input("Date", datetime.now())
                hours = st.number_input("Hours", min_value=0.0, max_value=24.0, step=0.25, value=1.0)
            
            with col_form2:
                activity_type = st.selectbox("Activity Type", [
                    "Client Meeting",
                    "Court Appearance",
                    "Document Review",
                    "Research",
                    "Phone Call",
                    "Email",
                    "Drafting",
                    "Travel",
                    "Other"
                ])
                rate = st.number_input("Hourly Rate ($)", min_value=0.0, step=25.0, value=250.0)
            
            description = st.text_area("Description", placeholder="Describe the work performed...")
            
            billable = st.checkbox("Billable", value=True)
            
            submitted = st.form_submit_button("💾 Save Time Entry", use_container_width=True, type="primary")
            
            if submitted:
                if selected_matter == "Select a matter...":
                    st.error("Please select a matter")
                elif not description:
                    st.error("Please provide a description")
                else:
                    # Add time entry
                    new_entry = {
                        'id': len(st.session_state.time_entries) + 1,
                        'date': entry_date.strftime('%Y-%m-%d'),
                        'matter': selected_matter,
                        'activity': activity_type,
                        'description': description,
                        'hours': hours,
                        'rate': rate,
                        'amount': hours * rate,
                        'billable': billable,
                        'billed': False,
                        'user': st.session_state.get('user_data', {}).get('name', 'Demo User')
                    }
                    
                    st.session_state.time_entries.append(new_entry)
                    st.success(f"✅ Time entry saved: {hours} hours for {selected_matter}")
                    st.rerun()
    
    with col2:
        st.markdown("### 💡 Quick Tips")
        st.info("""
        **Best Practices:**
        - Log time daily for accuracy
        - Be specific in descriptions
        - Use activity types consistently
        - Review unbilled time weekly
        """)
        
        # Quick stats
        st.markdown("### 📊 Today's Time")
        today = datetime.now().strftime('%Y-%m-%d')
        today_entries = [e for e in st.session_state.time_entries if e['date'] == today]
        today_hours = sum(e['hours'] for e in today_entries)
        today_amount = sum(e['amount'] for e in today_entries)
        
        st.metric("Hours Logged", f"{today_hours:.1f}")
        st.metric("Amount", f"${today_amount:,.2f}")
    
    # Recent time entries table
    st.markdown("---")
    st.markdown("### 📋 Recent Time Entries")
    
    # Filter options
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        filter_matter = st.selectbox("Filter by Matter", ["All"] + [m['title'] for m in matters])
    
    with col_filter2:
        filter_status = st.selectbox("Status", ["All", "Unbilled", "Billed"])
    
    with col_filter3:
        filter_date = st.selectbox("Period", ["Last 7 days", "Last 30 days", "This Month", "All Time"])
    
    # Apply filters
    filtered_entries = st.session_state.time_entries.copy()
    
    if filter_matter != "All":
        filtered_entries = [e for e in filtered_entries if e['matter'] == filter_matter]
    
    if filter_status == "Unbilled":
        filtered_entries = [e for e in filtered_entries if not e['billed']]
    elif filter_status == "Billed":
        filtered_entries = [e for e in filtered_entries if e['billed']]
    
    # Display entries
    if filtered_entries:
        df = pd.DataFrame(filtered_entries)
        df = df[['date', 'matter', 'activity', 'description', 'hours', 'rate', 'amount', 'billed']]
        df = df.sort_values('date', ascending=False)
        
        # Style the dataframe
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "date": st.column_config.DateColumn("Date", format="MMM DD, YYYY"),
                "matter": "Matter",
                "activity": "Activity",
                "description": st.column_config.TextColumn("Description", width="large"),
                "hours": st.column_config.NumberColumn("Hours", format="%.2f"),
                "rate": st.column_config.NumberColumn("Rate", format="$%.2f"),
                "amount": st.column_config.NumberColumn("Amount", format="$%.2f"),
                "billed": st.column_config.CheckboxColumn("Billed")
            }
        )
        
        # Summary
        total_hours = df['hours'].sum()
        total_amount = df['amount'].sum()
        
        st.markdown(f"""
        **Summary:** {len(df)} entries | {total_hours:.1f} hours | ${total_amount:,.2f}
        """)
    else:
        st.info("No time entries found matching your filters.")

def show_invoice_generator():
    """Invoice generation interface"""
    
    st.markdown("### 📄 Generate New Invoice")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Get matters and clients
        matters = st.session_state.get('matters', [])
        clients = st.session_state.get('clients', [])
        
        # Select client
        client_options = ["Select a client..."] + [c['name'] for c in clients]
        selected_client = st.selectbox("Client", client_options)
        
        if selected_client != "Select a client...":
            # Get unbilled entries for this client
            client_matters = [m['title'] for m in matters if m.get('client') == selected_client]
            unbilled_entries = [
                e for e in st.session_state.time_entries 
                if not e['billed'] and e['matter'] in client_matters
            ]
            
            if unbilled_entries:
                st.success(f"Found {len(unbilled_entries)} unbilled time entries")
                
                # Show unbilled entries
                st.markdown("#### Unbilled Time Entries")
                
                df = pd.DataFrame(unbilled_entries)
                df['select'] = True
                
                # Let user select which entries to include
                edited_df = st.data_editor(
                    df[['select', 'date', 'matter', 'activity', 'description', 'hours', 'rate', 'amount']],
                    hide_index=True,
                    use_container_width=True,
                    column_config={
                        "select": st.column_config.CheckboxColumn("Include", default=True),
                        "date": "Date",
                        "matter": "Matter",
                        "activity": "Activity",
                        "description": "Description",
                        "hours": st.column_config.NumberColumn("Hours", format="%.2f"),
                        "rate": st.column_config.NumberColumn("Rate", format="$%.2f"),
                        "amount": st.column_config.NumberColumn("Amount", format="$%.2f")
                    }
                )
                
                # Calculate totals for selected entries
                selected_entries = edited_df[edited_df['select'] == True]
                subtotal = selected_entries['amount'].sum()
                
                # Invoice details
                st.markdown("---")
                st.markdown("#### Invoice Details")
                
                col_inv1, col_inv2 = st.columns(2)
                
                with col_inv1:
                    invoice_date = st.date_input("Invoice Date", datetime.now())
                    due_date = st.date_input("Due Date", datetime.now() + timedelta(days=30))
                
                with col_inv2:
                    invoice_number = st.text_input("Invoice Number", value=f"INV-{datetime.now().strftime('%Y%m%d')}-{len(st.session_state.invoices)+1:03d}")
                    payment_terms = st.selectbox("Payment Terms", ["Net 30", "Net 15", "Net 60", "Due on Receipt"])
                
                notes = st.text_area("Notes", placeholder="Additional notes or payment instructions...")
                
                # Calculate taxes and total
                col_calc1, col_calc2 = st.columns(2)
                
                with col_calc1:
                    tax_rate = st.number_input("Tax Rate (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
                
                with col_calc2:
                    discount = st.number_input("Discount ($)", min_value=0.0, value=0.0, step=10.0)
                
                tax_amount = subtotal * (tax_rate / 100)
                total = subtotal + tax_amount - discount
                
                # Show calculation
                st.markdown("---")
                st.markdown("#### Invoice Summary")
                
                st.markdown(f"""
                | Description | Amount |
                |------------|--------|
                | Subtotal | ${subtotal:,.2f} |
                | Tax ({tax_rate}%) | ${tax_amount:,.2f} |
                | Discount | -${discount:,.2f} |
                | **Total** | **${total:,.2f}** |
                """)
                
                # Generate button
                st.markdown("---")
                
                col_btn1, col_btn2 = st.columns(2)
                
                with col_btn1:
                    if st.button("📄 Generate Invoice", type="primary", use_container_width=True):
                        # Create invoice
                        new_invoice = {
                            'id': len(st.session_state.invoices) + 1,
                            'invoice_number': invoice_number,
                            'client': selected_client,
                            'date': invoice_date.strftime('%Y-%m-%d'),
                            'due_date': due_date.strftime('%Y-%m-%d'),
                            'subtotal': subtotal,
                            'tax': tax_amount,
                            'discount': discount,
                            'total': total,
                            'status': 'draft',
                            'payment_terms': payment_terms,
                            'notes': notes,
                            'entries': selected_entries.to_dict('records')
                        }
                        
                        st.session_state.invoices.append(new_invoice)
                        
                        # Mark entries as billed
                        for idx in selected_entries.index:
                            for entry in st.session_state.time_entries:
                                if (entry['date'] == unbilled_entries[idx]['date'] and 
                                    entry['matter'] == unbilled_entries[idx]['matter'] and
                                    entry['hours'] == unbilled_entries[idx]['hours']):
                                    entry['billed'] = True
                                    break
                        
                        st.success(f"✅ Invoice {invoice_number} created successfully!")
                        st.balloons()
                        st.rerun()
                
                with col_btn2:
                    if st.button("👁️ Preview Invoice", use_container_width=True):
                        show_invoice_preview(selected_client, invoice_number, selected_entries, subtotal, tax_amount, discount, total)
            
            else:
                st.info(f"No unbilled time entries found for {selected_client}")
        
        else:
            st.info("Please select a client to generate an invoice")
    
    with col2:
        st.markdown("### 💡 Invoice Tips")
        st.info("""
        **Before Generating:**
        - Review all time entries
        - Verify hourly rates
        - Add relevant notes
        - Set proper due date
        
        **After Generating:**
        - Review invoice preview
        - Send to client
        - Track payment status
        """)

def show_invoice_preview(client, invoice_number, entries, subtotal, tax, discount, total):
    """Show invoice preview"""
    
    st.markdown("---")
    st.markdown("### 👁️ Invoice Preview")
    
    # Invoice header
    st.markdown(f"""
    <div style="
        background: white;
        padding: 2rem;
        border-radius: 16px;
        border: 2px solid #e9ecef;
        margin: 1rem 0;
    ">
        <div style="display: flex; justify-content: space-between; margin-bottom: 2rem;">
            <div>
                <h1 style="color: #2E86AB; margin: 0;">INVOICE</h1>
                <p style="margin: 0.5rem 0 0 0; color: #666;">#{invoice_number}</p>
            </div>
            <div style="text-align: right;">
                <h3 style="margin: 0;">Your Law Firm</h3>
                <p style="margin: 0.25rem 0; color: #666;">123 Legal Street</p>
                <p style="margin: 0.25rem 0; color: #666;">City, ST 12345</p>
            </div>
        </div>
        
        <div style="margin: 2rem 0;">
            <h4 style="color: #666;">Bill To:</h4>
            <h3 style="margin: 0.5rem 0;">{client}</h3>
        </div>
        
        <table style="width: 100%; border-collapse: collapse; margin: 2rem 0;">
            <thead>
                <tr style="background: #f8f9fa; border-bottom: 2px solid #dee2e6;">
                    <th style="padding: 0.75rem; text-align: left;">Date</th>
                    <th style="padding: 0.75rem; text-align: left;">Description</th>
                    <th style="padding: 0.75rem; text-align: right;">Hours</th>
                    <th style="padding: 0.75rem; text-align: right;">Rate</th>
                    <th style="padding: 0.75rem; text-align: right;">Amount</th>
                </tr>
            </thead>
            <tbody>
    """, unsafe_allow_html=True)
    
    # Add each entry
    for _, entry in entries.iterrows():
        st.markdown(f"""
                <tr style="border-bottom: 1px solid #e9ecef;">
                    <td style="padding: 0.75rem;">{entry['date']}</td>
                    <td style="padding: 0.75rem;">{entry['description']}</td>
                    <td style="padding: 0.75rem; text-align: right;">{entry['hours']:.2f}</td>
                    <td style="padding: 0.75rem; text-align: right;">${entry['rate']:.2f}</td>
                    <td style="padding: 0.75rem; text-align: right;">${entry['amount']:.2f}</td>
                </tr>
        """, unsafe_allow_html=True)
    
    # Totals
    st.markdown(f"""
            </tbody>
        </table>
        
        <div style="text-align: right; margin: 2rem 0;">
            <p style="margin: 0.5rem 0;"><strong>Subtotal:</strong> ${subtotal:,.2f}</p>
            <p style="margin: 0.5rem 0;"><strong>Tax:</strong> ${tax:,.2f}</p>
            <p style="margin: 0.5rem 0;"><strong>Discount:</strong> -${discount:,.2f}</p>
            <h2 style="margin: 1rem 0; color: #2E86AB;"><strong>Total:</strong> ${total:,.2f}</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_invoices_list():
    """Display list of invoices"""
    
    st.markdown("### 💳 Invoices")
    
    invoices = st.session_state.invoices
    
    if not invoices:
        st.info("No invoices yet. Generate your first invoice in the 'Generate Invoice' tab!")
        return
    
    # Filter options
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        status_filter = st.selectbox("Status", ["All", "Draft", "Sent", "Paid", "Overdue"])
    
    with col_filter2:
        # Get unique clients from invoices
        clients = list(set(inv['client'] for inv in invoices))
        client_filter = st.selectbox("Client", ["All"] + clients)
    
    with col_filter3:
        date_filter = st.selectbox("Period", ["All Time", "This Month", "Last Month", "Last 3 Months"])
    
    # Apply filters
    filtered_invoices = invoices.copy()
    
    if status_filter != "All":
        filtered_invoices = [inv for inv in filtered_invoices if inv['status'].lower() == status_filter.lower()]
    
    if client_filter != "All":
        filtered_invoices = [inv for inv in filtered_invoices if inv['client'] == client_filter]
    
    # Display invoices as cards
    for invoice in sorted(filtered_invoices, key=lambda x: x['date'], reverse=True):
        # Status color
        status_colors = {
            'draft': '#6c757d',
            'sent': '#ffc107',
            'paid': '#28a745',
            'overdue': '#dc3545'
        }
        
        status_color = status_colors.get(invoice['status'], '#6c757d')
        
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])
            
            with col1:
                st.markdown(f"**{invoice['invoice_number']}**")
                st.caption(invoice['client'])
            
            with col2:
                st.write(f"Date: {invoice['date']}")
                st.caption(f"Due: {invoice['due_date']}")
            
            with col3:
                st.markdown(f"""
                <span style="
                    background: {status_color};
                    color: white;
                    padding: 0.25rem 0.75rem;
                    border-radius: 12px;
                    font-size: 0.85rem;
                    font-weight: 600;
                ">{invoice['status'].upper()}</span>
                """, unsafe_allow_html=True)
            
            with col4:
                st.metric("Total", f"${invoice['total']:,.2f}")
            
            with col5:
                if st.button("View", key=f"view_{invoice['id']}", use_container_width=True):
                    show_invoice_detail(invoice)
            
            st.markdown("---")

def show_invoice_detail(invoice):
    """Show detailed invoice view"""
    
    st.markdown("### 📄 Invoice Details")
    
    # Action buttons
    col_action1, col_action2, col_action3, col_action4 = st.columns(4)
    
    with col_action1:
        if invoice['status'] == 'draft':
            if st.button("📧 Send to Client", use_container_width=True, type="primary"):
                invoice['status'] = 'sent'
                st.success("✅ Invoice sent to client!")
                st.rerun()
    
    with col_action2:
        if invoice['status'] in ['sent', 'overdue']:
            if st.button("💰 Mark as Paid", use_container_width=True):
                invoice['status'] = 'paid'
                st.success("✅ Invoice marked as paid!")
                st.balloons()
                st.rerun()
    
    with col_action3:
        if st.button("📥 Download PDF", use_container_width=True):
            st.info("PDF download coming soon!")
    
    with col_action4:
        if st.button("✏️ Edit", use_container_width=True):
            st.info("Edit functionality coming soon!")
    
    # Show invoice preview
    entries_df = pd.DataFrame(invoice['entries'])
    show_invoice_preview(
        invoice['client'],
        invoice['invoice_number'],
        entries_df,
        invoice['subtotal'],
        invoice['tax'],
        invoice['discount'],
        invoice['total']
    )

def show_billing_reports():
    """Display billing reports and analytics"""
    
    st.markdown("### 📊 Billing Reports & Analytics")
    
    time_entries = st.session_state.time_entries
    invoices = st.session_state.invoices
    
    # Date range selector
    col_date1, col_date2 = st.columns(2)
    
    with col_date1:
        start_date = st.date_input("From", datetime.now() - timedelta(days=90))
    
    with col_date2:
        end_date = st.date_input("To", datetime.now())
    
    # Revenue trends
    st.markdown("#### 💰 Revenue Trends")
    
    # Prepare revenue data
    revenue_by_month = {}
    for invoice in invoices:
        if invoice['status'] == 'paid':
            inv_date = datetime.strptime(invoice['date'], '%Y-%m-%d')
            month_key = inv_date.strftime('%Y-%m')
            revenue_by_month[month_key] = revenue_by_month.get(month_key, 0) + invoice['total']
    
    if revenue_by_month:
        revenue_df = pd.DataFrame(list(revenue_by_month.items()), columns=['Month', 'Revenue'])
        revenue_df = revenue_df.sort_values('Month')
        
        fig = px.line(revenue_df, x='Month', y='Revenue', markers=True,
                     title="Monthly Revenue Trend")
        fig.update_layout(yaxis_tickprefix="$")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No revenue data available yet")
    
    # Billable hours by matter
    st.markdown("#### ⏱️ Billable Hours by Matter")
    
    hours_by_matter = {}
    for entry in time_entries:
        if entry['billable']:
            matter = entry['matter']
            hours_by_matter[matter] = hours_by_matter.get(matter, 0) + entry['hours']
    
    if hours_by_matter:
        hours_df = pd.DataFrame(list(hours_by_matter.items()), columns=['Matter', 'Hours'])
        hours_df = hours_df.sort_values('Hours', ascending=False)
        
        fig = px.bar(hours_df, x='Matter', y='Hours', 
                    title="Billable Hours by Matter")
        st.plotly_chart(fig, use_container_width=True)
    
    # Activity breakdown
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("#### 📋 Time by Activity")
        
        hours_by_activity = {}
        for entry in time_entries:
            activity = entry['activity']
            hours_by_activity[activity] = hours_by_activity.get(activity, 0) + entry['hours']
        
        if hours_by_activity:
            activity_df = pd.DataFrame(list(hours_by_activity.items()), 
                                      columns=['Activity', 'Hours'])
            
            fig = px.pie(activity_df, values='Hours', names='Activity',
                        title="Time Distribution")
            st.plotly_chart(fig, use_container_width=True)
    
    with col_chart2:
        st.markdown("#### 💳 Invoice Status")
        
        status_counts = {}
        for invoice in invoices:
            status = invoice['status'].title()
            status_counts[status] = status_counts.get(status, 0) + 1
        
        if status_counts:
            status_df = pd.DataFrame(list(status_counts.items()), 
                                    columns=['Status', 'Count'])
            
            fig = px.pie(status_df, values='Count', names='Status',
                        title="Invoice Status Distribution",
                        color='Status',
                        color_discrete_map={
                            'Draft': '#6c757d',
                            'Sent': '#ffc107',
                            'Paid': '#28a745',
                            'Overdue': '#dc3545'
                        })
            st.plotly_chart(fig, use_container_width=True)
    
    # Top clients by revenue
    st.markdown("#### 🏆 Top Clients by Revenue")
    
    revenue_by_client = {}
    for invoice in invoices:
        if invoice['status'] == 'paid':
            client = invoice['client']
            revenue_by_client[client] = revenue_by_client.get(client, 0) + invoice['total']
    
    if revenue_by_client:
        client_df = pd.DataFrame(list(revenue_by_client.items()), 
                                columns=['Client', 'Revenue'])
        client_df = client_df.sort_values('Revenue', ascending=False).head(10)
        
        fig = px.bar(client_df, x='Client', y='Revenue',
                    title="Top 10 Clients by Revenue")
        fig.update_layout(yaxis_tickprefix="$")
        st.plotly_chart(fig, use_container_width=True)
    
    # Collection metrics
    st.markdown("---")
    st.markdown("#### 💵 Collection Metrics")
    
    col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)
    
    total_invoiced = sum(inv['total'] for inv in invoices)
    total_paid = sum(inv['total'] for inv in invoices if inv['status'] == 'paid')
    total_outstanding = sum(inv['total'] for inv in invoices if inv['status'] == 'sent')
    collection_rate = (total_paid / total_invoiced * 100) if total_invoiced > 0 else 0
    
    with col_metric1:
        st.metric("Total Invoiced", f"${total_invoiced:,.2f}")
    
    with col_metric2:
        st.metric("Total Collected", f"${total_paid:,.2f}")
    
    with col_metric3:
        st.metric("Outstanding", f"${total_outstanding:,.2f}")
    
    with col_metric4:
        st.metric("Collection Rate", f"{collection_rate:.1f}%")
    
    # Average invoice amount and payment time
    st.markdown("---")
    
    col_avg1, col_avg2, col_avg3 = st.columns(3)
    
    with col_avg1:
        avg_invoice = total_invoiced / len(invoices) if invoices else 0
        st.metric("Average Invoice", f"${avg_invoice:,.2f}")
    
    with col_avg2:
        avg_hours_per_invoice = sum(e['hours'] for e in time_entries) / len(invoices) if invoices else 0
        st.metric("Avg Hours/Invoice", f"{avg_hours_per_invoice:.1f}")
    
    with col_avg3:
        # Calculate average days to payment (for paid invoices)
        paid_invoices = [inv for inv in invoices if inv['status'] == 'paid']
        if paid_invoices:
            avg_days = 25  # Mock data - in real app, calculate from payment dates
            st.metric("Avg Days to Payment", f"{avg_days}")
        else:
            st.metric("Avg Days to Payment", "N/A")
    
    # Export report
    st.markdown("---")
    
    col_export1, col_export2 = st.columns(2)
    
    with col_export1:
        if st.button("📥 Export Time Entries (CSV)", use_container_width=True):
            df = pd.DataFrame(time_entries)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"time_entries_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    with col_export2:
        if st.button("📥 Export Invoice Report (CSV)", use_container_width=True):
            df = pd.DataFrame(invoices)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"invoices_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

def show_billing_settings():
    """Billing settings and configuration"""
    
    st.markdown("### ⚙️ Billing Settings")
    
    tab_set1, tab_set2, tab_set3 = st.tabs(["Rate Settings", "Invoice Templates", "Payment Methods"])
    
    with tab_set1:
        st.markdown("#### 💰 Default Hourly Rates")
        
        col_rate1, col_rate2 = st.columns(2)
        
        with col_rate1:
            st.markdown("**By Activity Type**")
            
            activities = [
                "Client Meeting",
                "Court Appearance",
                "Document Review",
                "Research",
                "Phone Call",
                "Email",
                "Drafting",
                "Travel"
            ]
            
            for activity in activities:
                default_rate = 250.0
                if activity == "Court Appearance":
                    default_rate = 350.0
                elif activity in ["Email", "Phone Call"]:
                    default_rate = 150.0
                
                st.number_input(f"{activity}", min_value=0.0, step=25.0, 
                              value=default_rate, key=f"rate_{activity}")
        
        with col_rate2:
            st.markdown("**By Team Member**")
            
            team_members = [
                ("Senior Partner", 500.0),
                ("Partner", 400.0),
                ("Senior Associate", 300.0),
                ("Associate", 250.0),
                ("Paralegal", 150.0)
            ]
            
            for member, rate in team_members:
                st.number_input(f"{member}", min_value=0.0, step=25.0, 
                              value=rate, key=f"rate_{member}")
        
        st.markdown("---")
        
        if st.button("💾 Save Rate Settings", type="primary"):
            st.success("✅ Rate settings saved successfully!")
    
    with tab_set2:
        st.markdown("#### 📄 Invoice Template Settings")
        
        col_template1, col_template2 = st.columns(2)
        
        with col_template1:
            st.markdown("**Firm Information**")
            
            firm_name = st.text_input("Firm Name", value="Your Law Firm")
            firm_address = st.text_area("Address", value="123 Legal Street\nCity, ST 12345")
            firm_phone = st.text_input("Phone", value="(555) 123-4567")
            firm_email = st.text_input("Email", value="billing@lawfirm.com")
        
        with col_template2:
            st.markdown("**Invoice Defaults**")
            
            default_terms = st.selectbox("Default Payment Terms", 
                                        ["Net 30", "Net 15", "Net 60", "Due on Receipt"],
                                        index=0)
            
            invoice_prefix = st.text_input("Invoice Number Prefix", value="INV-")
            
            include_logo = st.checkbox("Include Firm Logo", value=True)
            
            default_notes = st.text_area("Default Invoice Notes", 
                                        value="Thank you for your business. Please remit payment within the specified terms.")
        
        st.markdown("---")
        
        col_template_action1, col_template_action2 = st.columns(2)
        
        with col_template_action1:
            if st.button("💾 Save Template Settings", type="primary", use_container_width=True):
                st.success("✅ Template settings saved successfully!")
        
        with col_template_action2:
            if st.button("👁️ Preview Template", use_container_width=True):
                st.info("Template preview coming soon!")
    
    with tab_set3:
        st.markdown("#### 💳 Payment Methods")
        
        st.markdown("**Accepted Payment Methods**")
        
        payment_methods = {
            "Bank Transfer/ACH": st.checkbox("Bank Transfer/ACH", value=True),
            "Check": st.checkbox("Check", value=True),
            "Credit Card": st.checkbox("Credit Card", value=True),
            "PayPal": st.checkbox("PayPal", value=False),
            "Stripe": st.checkbox("Stripe", value=False)
        }
        
        st.markdown("---")
        st.markdown("**Payment Instructions**")
        
        for method, enabled in payment_methods.items():
            if enabled:
                with st.expander(f"📝 {method} Instructions"):
                    if method == "Bank Transfer/ACH":
                        st.text_input("Bank Name", value="First National Bank")
                        st.text_input("Account Number", value="****1234")
                        st.text_input("Routing Number", value="****5678")
                    elif method == "Check":
                        st.text_area("Mailing Address", 
                                    value="Your Law Firm\n123 Legal Street\nCity, ST 12345")
                    elif method == "Credit Card":
                        st.info("Credit card processing integration coming soon!")
                    elif method == "PayPal":
                        st.text_input("PayPal Email", value="billing@lawfirm.com")
                    elif method == "Stripe":
                        st.text_input("Stripe Account ID")
        
        st.markdown("---")
        
        st.markdown("**Late Payment Settings**")
        
        col_late1, col_late2 = st.columns(2)
        
        with col_late1:
            late_fee_enabled = st.checkbox("Enable Late Fees", value=True)
            
            if late_fee_enabled:
                late_fee_type = st.selectbox("Late Fee Type", 
                                            ["Percentage", "Fixed Amount"])
                
                if late_fee_type == "Percentage":
                    late_fee_percent = st.number_input("Late Fee (%)", 
                                                      min_value=0.0, max_value=25.0, 
                                                      value=5.0, step=0.5)
                else:
                    late_fee_amount = st.number_input("Late Fee Amount ($)", 
                                                     min_value=0.0, step=10.0, 
                                                     value=50.0)
        
        with col_late2:
            grace_period = st.number_input("Grace Period (days)", 
                                          min_value=0, max_value=30, 
                                          value=5)
            
            reminder_enabled = st.checkbox("Send Payment Reminders", value=True)
            
            if reminder_enabled:
                reminder_days = st.multiselect("Send Reminders Before Due Date",
                                              [7, 3, 1, 0],
                                              default=[7, 3])
        
        st.markdown("---")
        
        if st.button("💾 Save Payment Settings", type="primary"):
            st.success("✅ Payment settings saved successfully!")

def load_sample_time_entries():
    """Load sample time entries for demo"""
    
    sample_entries = [
        {
            'id': 1,
            'date': (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'),
            'matter': 'Johnson Custody Case',
            'activity': 'Client Meeting',
            'description': 'Initial consultation regarding custody arrangements',
            'hours': 2.0,
            'rate': 250.0,
            'amount': 500.0,
            'billable': True,
            'billed': False,
            'user': 'John Smith'
        },
        {
            'id': 2,
            'date': (datetime.now() - timedelta(days=4)).strftime('%Y-%m-%d'),
            'matter': 'Smith Contract Dispute',
            'activity': 'Document Review',
            'description': 'Reviewed employment contracts and supporting documentation',
            'hours': 3.5,
            'rate': 250.0,
            'amount': 875.0,
            'billable': True,
            'billed': False,
            'user': 'John Smith'
        },
        {
            'id': 3,
            'date': (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'),
            'matter': 'TechCorp Merger',
            'activity': 'Research',
            'description': 'Legal research on merger compliance requirements',
            'hours': 4.0,
            'rate': 300.0,
            'amount': 1200.0,
            'billable': True,
            'billed': True,
            'user': 'Sarah Johnson'
        },
        {
            'id': 4,
            'date': (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
            'matter': 'Johnson Custody Case',
            'activity': 'Phone Call',
            'description': 'Phone conference with opposing counsel',
            'hours': 0.5,
            'rate': 150.0,
            'amount': 75.0,
            'billable': True,
            'billed': False,
            'user': 'John Smith'
        },
        {
            'id': 5,
            'date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
            'matter': 'Smith Contract Dispute',
            'activity': 'Drafting',
            'description': 'Drafted response to opposing counsel demands',
            'hours': 2.5,
            'rate': 250.0,
            'amount': 625.0,
            'billable': True,
            'billed': False,
            'user': 'John Smith'
        },
        {
            'id': 6,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'matter': 'TechCorp Merger',
            'activity': 'Email',
            'description': 'Email correspondence with client regarding due diligence',
            'hours': 0.25,
            'rate': 150.0,
            'amount': 37.5,
            'billable': True,
            'billed': False,
            'user': 'Sarah Johnson'
        },
        {
            'id': 7,
            'date': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
            'matter': 'Anderson Real Estate',
            'activity': 'Court Appearance',
            'description': 'Hearing on motion for summary judgment',
            'hours': 3.0,
            'rate': 350.0,
            'amount': 1050.0,
            'billable': True,
            'billed': True,
            'user': 'Michael Davis'
        },
        {
            'id': 8,
            'date': (datetime.now() - timedelta(days=6)).strftime('%Y-%m-%d'),
            'matter': 'Johnson Custody Case',
            'activity': 'Document Review',
            'description': 'Reviewed financial disclosures and custody evaluation',
            'hours': 1.5,
            'rate': 250.0,
            'amount': 375.0,
            'billable': True,
            'billed': False,
            'user': 'John Smith'
        }
    ]
    
    return sample_entries

def load_sample_invoices():
    """Load sample invoices for demo"""
    
    sample_invoices = [
        {
            'id': 1,
            'invoice_number': 'INV-20251001-001',
            'client': 'TechCorp Industries',
            'date': '2025-10-01',
            'due_date': '2025-10-31',
            'subtotal': 2400.0,
            'tax': 0.0,
            'discount': 0.0,
            'total': 2400.0,
            'status': 'paid',
            'payment_terms': 'Net 30',
            'notes': 'Thank you for your business.',
            'entries': []
        },
        {
            'id': 2,
            'invoice_number': 'INV-20251005-002',
            'client': 'Anderson Real Estate LLC',
            'date': '2025-10-05',
            'due_date': '2025-11-04',
            'subtotal': 1575.0,
            'tax': 0.0,
            'discount': 0.0,
            'total': 1575.0,
            'status': 'sent',
            'payment_terms': 'Net 30',
            'notes': 'Payment due within 30 days.',
            'entries': []
        },
        {
            'id': 3,
            'invoice_number': 'INV-20251010-003',
            'client': 'Smith & Associates',
            'date': '2025-10-10',
            'due_date': '2025-11-09',
            'subtotal': 3250.0,
            'tax': 0.0,
            'discount': 100.0,
            'total': 3150.0,
            'status': 'sent',
            'payment_terms': 'Net 30',
            'notes': 'Volume discount applied.',
            'entries': []
        },
        {
            'id': 4,
            'invoice_number': 'INV-20251012-004',
            'client': 'Johnson Family Trust',
            'date': '2025-10-12',
            'due_date': '2025-11-11',
            'subtotal': 950.0,
            'tax': 0.0,
            'discount': 0.0,
            'total': 950.0,
            'status': 'draft',
            'payment_terms': 'Net 30',
            'notes': '',
            'entries': []
        }
    ]
    
    return sample_invoices
if __name__ == "__main__":
    show()
