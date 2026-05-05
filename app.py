import streamlit as st
import pandas as pd
from datetime import datetime

# পেজ কনফিগারেশন
st.set_page_config(page_title="Ops Support Tool", layout="wide")

# সেশন ইনিশিয়ালাইজেশন
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.user_email = ""
    st.session_state.entries = []  # এখানে সব এন্ট্রি জমা থাকবে

if "form_version" not in st.session_state:
    st.session_state.form_version = 0 # ফর্ম রিসেট করার জন্য কি-ভার্সন

# এজেন্ট এবং অ্যাডমিন লগইন ক্রেডেনশিয়াল
AGENTS = {
    "asikul.islam@pathao.com": "M198961",
    "agent2@email.com": "pass456"
}

ADMINS = {
    "asikul.islam@pathao.com": "Win@1234"
}

# লগইন স্ক্রিন
def login_screen():
    st.title("🔑 Ops Support Tool - Login")
    role = st.selectbox("Select Role", ["Agent", "Admin"])
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if role == "Agent":
            if email in AGENTS and AGENTS[email] == password:
                st.session_state.logged_in = True
                st.session_state.role = "Agent"
                st.session_state.user_email = email
                st.rerun()
            else:
                st.error("Invalid Agent Credentials")
        elif role == "Admin":
            if email in ADMINS and ADMINS[email] == password:
                st.session_state.logged_in = True
                st.session_state.role = "Admin"
                st.session_state.user_email = email
                st.rerun()
            else:
                st.error("Invalid Admin Credentials")

# এজেন্ট ড্যাশবোর্ড
def agent_dashboard():
    st.sidebar.title(f"Agent Panel ({st.session_state.user_email})")
    page = st.sidebar.radio("Navigate Pages", ["User", "Driver", "All Entries"])
    
    # এজেন্টের সফল সাবমিশনের পর অ্যানিমেশন
    if "agent_action_done" in st.session_state:
        st.success("Entry successfully submitted to Admin dashboard!")
        st.balloons()
        del st.session_state["agent_action_done"]
    
    # 1. User Page
    if page == "User":
        st.subheader("👤 User Module")
        sub_page = st.selectbox("Select Action", ["Suspension", "Unsuspension", "Pay Later Due Adjustment", "Promos"])
        
        form_data = {}
        
        if sub_page == "Suspension":
            with st.form(f"user_suspension_form_{st.session_state.form_version}"):
                trip_id = st.text_input("Trip ID")
                user_name = st.text_input("User Name")
                user_number = st.text_input("User Number")
                user_id = st.text_input("User ID")
                suspension_sop = st.text_area("Suspension SOP")
                remarks = st.text_input("Remarks")
                penalty = st.number_input("Penalty Amount", min_value=0.0)
                
                submitted = st.form_submit_button("Review")
                if submitted:
                    form_data = {
                        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Agent": st.session_state.user_email,
                        "Type": "User",
                        "Category": "Suspension",
                        "Trip ID": trip_id,
                        "Name": user_name,
                        "Number": user_number,
                        "ID": user_id,
                        "SOP/Reason": suspension_sop,
                        "Remarks": remarks,
                        "Amount": penalty,
                        "Interaction ID": "",
                        "Tx ID": "",
                        "Status": "Pending",
                        "Note": f"{trip_id} | {suspension_sop} | Requested by {st.session_state.user_email}"
                    }
                    st.session_state["review_entry"] = form_data

        elif sub_page == "Unsuspension":
            with st.form(f"user_unsuspension_form_{st.session_state.form_version}"):
                trip_id = st.text_input("Trip ID")
                user_name = st.text_input("User Name")
                user_number = st.text_input("User Number")
                user_id = st.text_input("User ID")
                reason = st.text_area("Unsuspension Reason")
                tx_id = st.text_input("Transaction ID")
                amount = st.number_input("Amount", min_value=0.0)
                
                submitted = st.form_submit_button("Review")
                if submitted:
                    form_data = {
                        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Agent": st.session_state.user_email,
                        "Type": "User",
                        "Category": "Unsuspension",
                        "Trip ID": trip_id,
                        "Name": user_name,
                        "Number": user_number,
                        "ID": user_id,
                        "SOP/Reason": reason,
                        "Remarks": "",
                        "Amount": amount,
                        "Interaction ID": "",
                        "Tx ID": tx_id,
                        "Status": "Pending",
                        "Note": f"{trip_id} | {reason} | {tx_id} | Requested by {st.session_state.user_email}"
                    }
                    st.session_state["review_entry"] = form_data
                    
        elif sub_page == "Pay Later Due Adjustment":
            with st.form(f"user_paylater_form_{st.session_state.form_version}"):
                trip_id = st.text_input("Trip ID")
                user_name = st.text_input("User Name")
                user_number = st.text_input("User Number")
                user_id = st.text_input("User ID")
                reason = st.text_area("Adjustment Reason")
                tx_id = st.text_input("Reverse Transaction ID")
                amount = st.number_input("Amount", min_value=0.0)
                
                submitted = st.form_submit_button("Review")
                if submitted:
                    form_data = {
                        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Agent": st.session_state.user_email,
                        "Type": "User",
                        "Category": "Pay Later Due Adjustment",
                        "Trip ID": trip_id,
                        "Name": user_name,
                        "Number": user_number,
                        "ID": user_id,
                        "SOP/Reason": reason,
                        "Remarks": "",
                        "Amount": amount,
                        "Interaction ID": "",
                        "Tx ID": tx_id,
                        "Status": "Pending",
                        "Note": ""
                    }
                    st.session_state["review_entry"] = form_data
                    
        elif sub_page == "Promos":
            with st.form(f"user_promo_form_{st.session_state.form_version}"):
                trip_id = st.text_input("Trip ID")
                user_name = st.text_input("User Name")
                user_number = st.text_input("User Number")
                user_id = st.text_input("User ID")
                reason = st.text_area("Promo Reason")
                remarks = st.text_input("Remarks")
                amount = st.number_input("Amount", min_value=0.0)
                interaction_id = st.text_input("Interaction ID")
                
                submitted = st.form_submit_button("Review")
                if submitted:
                    form_data = {
                        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Agent": st.session_state.user_email,
                        "Type": "User",
                        "Category": "Promos",
                        "Trip ID": trip_id,
                        "Name": user_name,
                        "Number": user_number,
                        "ID": user_id,
                        "SOP/Reason": reason,
                        "Remarks": remarks,
                        "Amount": amount,
                        "Interaction ID": interaction_id,
                        "Tx ID": "",
                        "Status": "Pending",
                        "Note": ""
                    }
                    st.session_state["review_entry"] = form_data

    # 2. Driver Page
    elif page == "Driver":
        st.subheader("🚗 Driver Module")
        sub_page = st.selectbox("Select Action", ["Suspension", "Unsuspension"])
        
        form_data = {}
        if sub_page == "Suspension":
            with st.form(f"driver_suspension_form_{st.session_state.form_version}"):
                trip_id = st.text_input("Trip ID")
                driver_name = st.text_input("Driver Name")
                driver_number = st.text_input("Driver Number")
                driver_id = st.text_input("Driver ID")
                reason = st.text_area("Suspension Reason")
                remarks = st.text_input("Remarks")
                penalty = st.number_input("Penalty Amount (If any)", min_value=0.0)
                
                submitted = st.form_submit_button("Review")
                if submitted:
                    form_data = {
                        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Agent": st.session_state.user_email,
                        "Type": "Driver",
                        "Category": "Suspension",
                        "Trip ID": trip_id,
                        "Name": driver_name,
                        "Number": driver_number,
                        "ID": driver_id,
                        "SOP/Reason": reason,
                        "Remarks": remarks,
                        "Amount": penalty,
                        "Interaction ID": "",
                        "Tx ID": "",
                        "Status": "Pending",
                        "Note": ""
                    }
                    st.session_state["review_entry"] = form_data
                    
        elif sub_page == "Unsuspension":
            with st.form(f"driver_unsuspension_form_{st.session_state.form_version}"):
                trip_id = st.text_input("Trip ID")
                driver_name = st.text_input("Driver Name")
                driver_number = st.text_input("Driver Number")
                driver_id = st.text_input("Driver ID")
                reason = st.text_area("Unsuspension Reason")
                tx_id = st.text_input("Reverse Transaction ID")
                remarks = st.text_input("Remarks")
                
                submitted = st.form_submit_button("Review")
                if submitted:
                    form_data = {
                        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Agent": st.session_state.user_email,
                        "Type": "Driver",
                        "Category": "Unsuspension",
                        "Trip ID": trip_id,
                        "Name": driver_name,
                        "Number": driver_number,
                        "ID": driver_id,
                        "SOP/Reason": reason,
                        "Remarks": remarks,
                        "Amount": 0.0,
                        "Interaction ID": "",
                        "Tx ID": tx_id,
                        "Status": "Pending",
                        "Note": ""
                    }
                    st.session_state["review_entry"] = form_data

    # Reviewing Section and Submission
    if "review_entry" in st.session_state and page != "All Entries":
        st.markdown("---")
        st.markdown("### 📋 Review Entry Details")
        st.json(st.session_state["review_entry"])
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Confirm Submission", use_container_width=True):
                st.session_state.entries.append(st.session_state["review_entry"])
                del st.session_state["review_entry"]
                st.session_state.form_version += 1  # ফর্ম ফিল্ড ক্লিয়ার করার জন্য
                st.session_state.agent_action_done = True
                st.rerun()
        with col2:
            if st.button("Cancel", use_container_width=True):
                del st.session_state["review_entry"]
                st.rerun()

    # 3. All Entries Page (Agent View)
    elif page == "All Entries":
        st.subheader("📋 All Entries Status")
        
        tab_u, tab_d = st.tabs(["User", "Driver"])
        
        if st.session_state.entries:
            df = pd.DataFrame(st.session_state.entries)
            
            with tab_u:
                user_df = df[df["Type"] == "User"]
                if not user_df.empty:
                    st.dataframe(user_df[["Time", "Agent", "Category", "Trip ID", "Name", "ID", "Status"]], use_container_width=True)
                else:
                    st.info("No user entries yet.")
            
            with tab_d:
                driver_df = df[df["Type"] == "Driver"]
                if not driver_df.empty:
                    st.dataframe(driver_df[["Time", "Agent", "Category", "Trip ID", "Name", "ID", "Status"]], use_container_width=True)
                else:
                    st.info("No driver entries yet.")
        else:
            st.info("No entries found.")
            
    if st.sidebar.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.rerun()

# অ্যাডমিন ড্যাশবোর্ড
def admin_dashboard():
    st.sidebar.title("Admin Panel")
    page = st.sidebar.radio("Navigate Pages", ["Approvals", "Analytics"])
    
    if page == "Approvals":
        st.title("⚙️ Admin Execution Dashboard")
        
        # অ্যাডমিন অ্যানিমেশন চেক (রিস্টার্টের পর মেসেজ দেখানোর জন্য)
        if "admin_action_status" in st.session_state:
            status = st.session_state.admin_action_status
            if status == "Done":
                st.success("🎉 Entry successfully approved (Done)!")
                st.balloons()
            elif status == "Rejected":
                st.error("❌ Entry has been rejected!")
                st.snow() # রিজেকশনের জন্য স্নো অ্যানিমেশন
            del st.session_state["admin_action_status"]
            
        if not st.session_state.entries:
            st.info("No entries submitted yet.")
        else:
            df = pd.DataFrame(st.session_state.entries)
            st.dataframe(df, use_container_width=True)
            
            st.markdown("---")
            st.subheader("Update Request")
            selected_idx = st.selectbox("Select row index to execute", df.index)
            selected_entry = st.session_state.entries[selected_idx]
            
            col1, col2 = st.columns(2)
            with col1:
                note_text = st.text_input("Note Section", value=selected_entry["Note"])
            with col2:
                new_status = st.selectbox("Status", ["Pending", "Done", "Rejected"], index=["Pending", "Done", "Rejected"].index(selected_entry["Status"]))
            
            if st.button("Save Changes & Execute"):
                st.session_state.entries[selected_idx]["Note"] = note_text
                st.session_state.entries[selected_idx]["Status"] = new_status
                
                # অ্যানিমেশন ট্রিগার করার জন্য স্টেট সেভ
                st.session_state.admin_action_status = new_status
                st.rerun()
                
    elif page == "Analytics":
        st.title("📊 Analytics Dashboard")
        
        if not st.session_state.entries:
            st.info("No data available for analytics.")
        else:
            # ফিল্টার
            col1, col2, col3 = st.columns(3)
            with col1:
                start_date = st.date_input("Start Date", datetime.today())
            with col2:
                end_date = st.date_input("End Date", datetime.today())
            with col3:
                customer_type = st.selectbox("Customer Type", ["All", "User", "Driver"])
                
            df = pd.DataFrame(st.session_state.entries)
            if not df.empty:
                df['Time'] = pd.to_datetime(df['Time'])
                # ফিল্টার অ্যাপ্লাই
                mask = (df['Time'].dt.date >= start_date) & (df['Time'].dt.date <= end_date)
                if customer_type != "All":
                    mask = mask & (df['Type'] == customer_type)
                
                filtered_df = df[mask]
                
                # শুধুমাত্র Done স্ট্যাটাস ওয়ালা এন্ট্রিগুলো দিয়ে ক্যালকুলেশন
                done_df = filtered_df[filtered_df["Status"] == "Done"]
                
                st.write(f"### Report for: {customer_type} (Status: Done only)")
                
                # ক্যালকুলেশন
                total_suspension = len(done_df[done_df["Category"] == "Suspension"])
                total_unsuspension = len(done_df[done_df["Category"] == "Unsuspension"])
                
                penalty_amount = done_df[done_df["Category"].isin(["Suspension", "Pay Later Due Adjustment", "Promos"])]["Amount"].sum()
                collected_amount = done_df[done_df["Category"].isin(["Unsuspension"])]["Amount"].sum()
                remaining_needed = penalty_amount - collected_amount
                
                # রেশিও ক্যালকুলেশন (শতাংশে)
                ratio_pct = (total_suspension / total_unsuspension * 100) if total_unsuspension > 0 else (total_suspension * 100.0)
                
                # ডিসপ্লে মেট্রিক্স
                m1, m2, m3 = st.columns(3)
                m1.metric("Suspension Count", total_suspension)
                m2.metric("Unsuspension Count", total_unsuspension)
                m3.metric("Total Penalty/Required", f"Tk {penalty_amount:,.2f}")
                
                m4, m5, m6 = st.columns(3)
                m4.metric("Amount Collected", f"Tk {collected_amount:,.2f}")
                m5.metric("Still Collection Needed", f"Tk {remaining_needed:,.2f}")
                m6.metric("Suspension vs Unsuspension Ratio", f"{ratio_pct:,.2f}%")

                st.markdown("---")
                # প্রগ্রেস বার
                if penalty_amount > 0:
                    collected_pct = (collected_amount / penalty_amount) * 100
                    remaining_pct = (remaining_needed / penalty_amount) * 100
                    st.write(f"**Collected Amount Percentage:** {collected_pct:.2f}%")
                    st.progress(min(collected_pct/100, 1.0))
                    st.write(f"**Need to Collect Percentage:** {remaining_pct:.2f}%")
                    st.progress(min(max(remaining_pct/100, 0.0), 1.0))
                
    if st.sidebar.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.rerun()

# মেইন অ্যাপ ফ্লো
if not st.session_state.logged_in:
    login_screen()
else:
    if st.session_state.role == "Agent":
        agent_dashboard()
    elif st.session_state.role == "Admin":
        admin_dashboard()
