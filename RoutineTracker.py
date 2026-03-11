import streamlit as st
from streamlit_option_menu import option_menu


# Set page configuration
st.set_page_config(
    page_title="Routine Tracker",
    page_icon="📅",
    layout="centered"
)


# Background and layout styling
st.markdown(
    """
    <style>
    .stApp {     
        background: linear-gradient(135deg, #000000, #061d40);
    }


    /* ###### Custom class for title ####### */
    .HomeTitle {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 70px !important;
        font-style: italic;
        color: #ffffff;
        text-transform: uppercase;
    }

    /* ###### Custom class for The other text ####### */
    .Hometext {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 20px !important;
        font-style: italic;
        color: #ffffff;
    }



    </style>

    <!-- Load Google font -->
    <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True
)   

# Navigation menu
selected = option_menu(
    menu_title=None,
    options=["Home", "Routine", "Consistency Tracker", "Daily Report", "About"],
    icons=["house", "arrow-repeat", "bullseye", "journal-text", "info-circle"],
    orientation="horizontal",
    styles={
        "nav-link": {
            "font-size": "14px", 
            "text-align": "center", 
            "padding": "12px 18px",
            "white-space": "nowrap"
        }, 

        "nav-link-selected": {
            "background-color": "#275996", 
            "color": "white"
        }
    }
)

# Pages
if selected == "Home":
    st.image("ruotinepic.png")
    st.markdown('<div class="HomeTitle">Welcome to Routine Tracker!</div>', unsafe_allow_html=True)
    st.markdown('<div class="Hometext">This app helps you build and maintain healthy habits by tracking your daily routines and consistency.</div>', unsafe_allow_html=True)
    st.markdown('<div class="Hometext">Use the navigation menu above to start a more consistent and productive lifestyle!</div>', unsafe_allow_html=True)




# ---- Initialize session ----
if "consistency_days" not in st.session_state:
    st.session_state.consistency_days = 0

if "today_completed" not in st.session_state:
    st.session_state.today_completed = False

if "reset_tasks" not in st.session_state:
    st.session_state.reset_tasks = False

if "delete_index" not in st.session_state:
    st.session_state.delete_index = None

if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Convert old tasks (strings) to new format
for i, task in enumerate(st.session_state.tasks):
    if isinstance(task, str):
        st.session_state.tasks[i] = {
            "name": task,
            "done": False
        }

if "consistency_history" not in st.session_state:
    st.session_state.consistency_history = []

if "daily_reports" not in st.session_state:
    st.session_state.daily_reports = []

if "delete_report_index" not in st.session_state:
    st.session_state.delete_report_index = None

if "open_report" not in st.session_state:
    st.session_state.open_report = None





#---- Routine Page ----
if selected == "Routine":
    st.title("My Routine")



    # ---- Add Task ----
    @st.dialog("Create New Task")
    def add_task_dialog():

        task = st.text_input("Task name")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Create"):
                if task:
                    st.session_state.tasks.append({
                        "name": task,
                        "done": False
                    })
                    st.rerun()

        with col2:
            if st.button("Cancel"):
                st.rerun()


    if st.button("Add Task", icon="➕", help = "Click to add a new task"):
        add_task_dialog()


    #---- Delete Confirmation ----
    @st.dialog("Confirm Delete")
    def delete_task_dialog(task_index):

        st.write("Are you sure you want to delete this task?")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Yes, Delete"):
               st.session_state.pop(f"task_{task_index}", None)
               st.session_state.tasks.pop(task_index)
               st.session_state.delete_index = None
               st.rerun()

        with col2:
            if st.button("Cancel"):
                st.session_state.delete_index = None
                st.rerun()

    if st.session_state.reset_tasks:
        for i, task in enumerate(st.session_state.tasks):
            task["done"] = False
            st.session_state[f"task_{i}"] = False  # reset checkbox widget

        st.session_state.reset_tasks = False




    #---- Display Tasks ----
    for i, task in enumerate(st.session_state.tasks):

        col1, col2 = st.columns([6,1])

        with col1:
            checked = st.checkbox(
                task["name"],
                value=task["done"],
                key=f"task_{i}"
            )
            st.session_state.tasks[i]["done"] = checked

        with col2:
            if st.button("🗑️", key=f"delete_{i}"):
                st.session_state.delete_index = i
                st.rerun()


    st.divider()

    # ---- Display saved reports ----

    if len(st.session_state.tasks) == 0:
        st.subheader("Task List")
        st.write("No Task Routine Yet")

    else:
        if st.session_state.delete_index is not None:
            delete_task_dialog(st.session_state.delete_index)



    completed = [task["done"] for task in st.session_state.tasks]


    # --- Counts Conplition Percentage ---
    completed_count = sum(completed)
    total_tasks = len(st.session_state.tasks)

    if total_tasks > 0:
        percentage = (completed_count / total_tasks) * 100
    else:
        percentage = 0



    if completed and all(completed):

        st.success("🎉 All tasks completed today!")

    if completed and all(completed) and not st.session_state.today_completed:
        st.session_state.consistency_days += 1
        st.session_state.today_completed = True


    # ---- Reset Dialog ----
    @st.dialog("Confirm Reset")
    def reset_tasks_dialog():

        st.write(
            "This will uncheck all tasks to prepare for the next day. "
            "Do you want to proceed?"
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Yes"):

                completed_count = sum(completed)
                total_tasks = len(st.session_state.tasks)

                if total_tasks > 0:
                    percentage = (completed_count / total_tasks) * 100
                else:
                    percentage = 0

                st.session_state.consistency_history.append(round(percentage, 2))
                st.session_state.reset_tasks = True
                st.session_state.today_completed = False
                st.rerun()

        with col2:
            if st.button("No"):
               st.rerun()
    
    col1, col2 = st.columns([4,1])

    with col1:
        st.write("")  # spacer

    with col2:
        if len(st.session_state.tasks) == 0:
            if st.button("Start New Day", help = "Click to reset tasks for the next day"):
                st.error("No task yet")

        else: 
            if st.button("Start New Day", help = "Click to reset tasks for the next day"):
                reset_tasks_dialog()
    


#---- Consistency Tracker Page ----
if selected == "Consistency Tracker":
    st.title("Consistency Tracker")

    st.divider()

    # ---- Metrics Dashboard ----
    col1, col2, col3 = st.columns(3)

    total_tasks = len(st.session_state.tasks)
    completed_today = sum(
        st.session_state.get(f"task_{i}", False)
        for i in range(len(st.session_state.tasks))
    )
    consistency_days = st.session_state.consistency_days

    with col1:
        st.metric("Total Tasks", total_tasks)

    with col2:
        st.metric("Completed Today", completed_today)

    with col3:
        st.metric("Consistency Days", consistency_days)


    # ---- Display Consistency Tracker ----
    st.title("Consistency Tracker")

    if len(st.session_state.consistency_history) == 0 :
        st.write("No day completed yet")

    else:
        if st.session_state.consistency_history is not None:

            history = st.session_state.get("consistency_history", [])

            st.subheader("Consistency Progress")
            st.line_chart(history)

            for i, percent in enumerate(history):

                st.write(f"Day {i+1} — {percent}% Complete")

                # Convert percent to decimal for progress bar
                progress_value = percent / 100

                st.progress(progress_value)



# ---- Daily Report Page ----
if selected == "Daily Report":
    st.title("Daily Report")

    @st.dialog("Daily Report")
    def daily_report_dialog():

        daily_report = st.text_area("Daily Report", key="report_notes")

        report_date = st.date_input("Select Date", key="report_date")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Save Report"):

                if report_date and daily_report:

                    st.session_state.daily_reports.append({
                        "date": report_date,
                        "text": daily_report
                    })

                    st.success("Report saved!")

                    st.session_state.pop("report_date", None)
                    st.session_state.pop("report_notes", None)


                    st.rerun()

        with col2:
            if st.button("Cancel"):
               st.session_state.pop("report_date", None)
               st.session_state.pop("report_notes", None)

               st.rerun()

    if st.button("Write Daily Report", help="Click to write your daily report"):
        daily_report_dialog()


    @st.dialog("Confirm Delete")
    def delete_report_dialog(report_index):

        st.write("Are you sure you want to delete this report?")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Yes, Delete"):
                st.session_state.daily_reports.pop(report_index)
                st.session_state.delete_report_index = None

                if st.session_state.open_report == report_index:
                    st.session_state.open_report = None

                st.rerun()

        with col2:
            if st.button("Cancel"):
                st.session_state.delete_report_index = None
                st.rerun()


    st.divider()


    # ----Display Reports ----
    st.subheader("Saved Reports")

    if len(st.session_state.daily_reports) == 0:
        st.write("No reports yet.")

    else:
        for i, report in enumerate(st.session_state.daily_reports):

            col1, col2 = st.columns([6,1])

            date_label = str(report["date"])

            with col1:
                if st.button(date_label, key=f"report_btn_{i}"):

                    if st.session_state.open_report == i:
                        st.session_state.open_report = None
                    else:
                        st.session_state.open_report = i

            with col2:
                if st.button("🗑️", key=f"delete_report_{i}"):
                    st.session_state.delete_report_index = i
                    st.rerun()

            if st.session_state.open_report == i:
                st.write("### Report")
                st.write(report["text"])
                st.divider()

    if st.session_state.delete_report_index is not None:
        delete_report_dialog(st.session_state.delete_report_index)


# ---- About page ----
if selected == "About":
    st.title("About Routine Tracker")
    st.write("Routine Tracker is a simple app designed to help you build and maintain healthy habits by tracking your daily routines and " \
             "consistency. It allows you to create tasks, track your progress, and stay motivated on your journey to a more consistent and " \
             "productive lifestyle.")
    
    st.space = st.empty()  

    st.write("This web app is designed to help users, specifically the youth to keep track on their daily activities, find out what blocks or stops them " \
             "in there consisency, allowing them to be aware of unhealthy habits, and avoid distractions, promoting a more consistent" \
             " lifestyle.")

    st.space = st.empty()

    st.write ("It mostly take in textual data, specifically, daily task list and routine documentation (Daily Report page). With the collected data " \
    " in the Routine list it ouputs the consistency tracker by converting their list into numeric data to have a more precise complition rate, while the"\
    " purpose of the documentation is just to record events that effected the users rouotine consistency")

    st.space = st.empty()

    st.write("The purpose of the 1st page or the home page is to welcome the user, this is like the face of the web-app ensuring that it " \
             "is presentable, aesthetic, and gives a direct or obvious theme of sport, discipline, and energetic vibe") 
       
    st.space = st.empty()

    st.write("The 2nd page or the “Routine” page is the main service of my web app, giving option for the user to create their own daily " \
    "routine tasks. Giving them option to both add, delete and restart the cycle once the day is over.")

    st.space = st.empty()

    st.write("The 3rd page or the “Consistency Tracker” page is a list that tracks how consistent you are in applying your daily routine, it " \
             "tracks the percentage of how you completed your daily task, and compile them to see your progress.")

    st.space = st.empty()

    st.write("The 4th page is to allow the users to record the events in their day, allowing theme to highlight what blocks them from doing their " \
             "daily task, or what motivates theme in doing their routine. It gives the user an option to type down important events that happen in that  specific day.")

    st.space = st.empty()

    st.write("This web app is a combination of a to-do list, tracker, and journal. Tools that are all useful in maintaining the consistency of your" \
             "daily routine. Promoting discipline and at the same time a healthy lifestyle")

    st.write("")
    st.write("")

    st.subheader("For documentation, here's the 20 main Streamlit UI components used for this web app \n"\
             "1. st.set_page_config()\n"\
             "2. st.markdown()\n"\
             "3. st.image()\n"\
             "4. st.title()\n"\
             "5. st.subheader()\n"\
             "6. st.write()\n"\
             "7. st.button()\n"\
             "8. st.checkbox()\n"\
             "9. st.columns()\n"\
             "10. st.divider()\n"\
             "11. st.success()\n"\
             "12. st.error()\n"\
             "13. st.empty()\n"\
             "14. st.text_input()\n"\
             "15. st.text_area()\n"\
             "16. st.date_input()\n"\
             "17. st.metric()\n"\
             "18. st.line_chart()\n"\
             "19. st.progress()\n"\
             "20. st.dialog()"
             )