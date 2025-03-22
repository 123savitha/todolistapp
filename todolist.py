import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt

# Function to load tasks from session state
def load_tasks():
    if 'tasks' not in st.session_state:
        st.session_state.tasks = []
    if 'completed_tasks' not in st.session_state:
        st.session_state.completed_tasks = []

# Function to add a new task with timestamp
def add_task(task):
    if task:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.tasks.append({"task": task, "timestamp": timestamp})

# Function to remove a task
def remove_task(index):
    if 0 <= index < len(st.session_state.tasks):
        st.session_state.tasks.pop(index)

# Function to complete a task with timestamp
def complete_task(index):
    if 0 <= index < len(st.session_state.tasks):
        completed_task = st.session_state.tasks.pop(index)
        completed_task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.completed_tasks.append(completed_task)

# Load tasks from session state
load_tasks()

# yellow gradient background
st.markdown(
    """
    <style>
    @keyframes sunset {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    .stApp {
        background: linear-gradient(45deg, #ff9a9e, #fad0c4, #fbc2eb, #a18cd1, #fad0c4);
        background-size: 300% 300%;
        animation: sunset 12s ease infinite;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# To create Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["To-Do List", "About", "History"])

if page == "To-Do List":
    st.markdown("<div class='quote'>\"The only way to do great work is to love what you do.\" - Steve Jobs</div>", unsafe_allow_html=True)
    st.title("To-Do List")

    new_task = st.text_input("Enter a new task:")
    if st.button("Add Task"):
        add_task(new_task)
        st.success(f'Task "{new_task}" added!')

    if st.session_state.tasks:
        st.subheader("Your Tasks:")
        for i, task_data in enumerate(st.session_state.tasks):
            task_label = f"{i + 1}. {task_data['task']} (Added: {task_data['timestamp']})"
            col1, col2, col3 = st.columns([6, 2, 2])
            with col1:
                st.write(task_label)
            with col2:
                if st.button("Complete", key=f"complete_{i}"):
                    complete_task(i)
                    st.success(f'Task "{task_data["task"]}" completed!')
            with col3:
                if st.button("Remove", key=f"remove_{i}"):
                    remove_task(i)
                    st.success(f'Task "{task_data["task"]}" removed!')

    if st.button("Clear All Tasks"):
        st.session_state.tasks.clear()
        st.success("All tasks cleared!")

    # To get Task Progress Visualization
    total_tasks = len(st.session_state.tasks) + len(st.session_state.completed_tasks)
    completed_tasks = len(st.session_state.completed_tasks)
    remaining_tasks = len(st.session_state.tasks)

    # Create a bar chart
    labels = ['Completed', 'Remaining']
    sizes = [completed_tasks, remaining_tasks]

    fig, ax = plt.subplots()
    ax.bar(labels, sizes, color=['#4CAF50', '#FF9800'])
    ax.set_ylabel('Number of Tasks')
    ax.set_title('Task Progress')

    st.pyplot(fig)

elif page == "About":
    st.title("About This App")
    st.write("""
    This To-Do List application is designed to help you manage your tasks efficiently. 
    You can easily add, remove, and clear tasks to keep track of what you need to do.
    """)
    
    st.write("### Features:")
    st.write("- **Add Tasks**: Quickly add new tasks to your list.")
    st.write("- **Remove Tasks**: Easily remove tasks that you have completed.")
    st.write("- **Complete Tasks**: Mark tasks as completed and view them in the history.")
    st.write("- **Clear All Tasks**: Clear your entire task list with a single click.")
    st.write("- **Track Task Time**: View the time when tasks were added and completed.")
    
    st.write("### How to Use:")
    st.write("1. Enter a task in the input box.")
    st.write("2. Click the 'Add Task' button to add it to your list.")
    st.write("3. Use the 'Complete' button next to each task to mark it as completed.")
    st.write("4. Use the 'Remove' button to delete a task.")
    st.write("5. Click 'Clear All Tasks' to remove all tasks from the list.")
    st.write("6. Go to 'History' to view completed tasks with timestamps.")
    
    st.write("## 🎉 What's New:")
    st.write("✅ Add Timestamp for New Tasks – Each task now records the date and time it was added.")
    st.write("✅ Add Timestamp When Task is Completed – Completion time is stored and displayed in the History tab.")
    st.write("✅ Display Timestamp in Task List and History – See both when a task was added and when it was completed.")

    st.write("## 📅 How It Works:")
    st.write("When you add a task, it shows the date and time in the task list.")
    st.write("Completed tasks move to the History tab, showing when they were added and completed.")

elif page == "History":
    st.title("Task History")
    if st.session_state.completed_tasks:
        st.subheader("Completed Tasks:")
        for i, task_data in enumerate(st.session_state.completed_tasks):
            st.write(f"{i + 1}. {task_data['task']} (Added: {task_data['timestamp']}) - ✅ Completed at: {task_data['completed_at']}")
    else:
        st.write("No tasks have been completed yet.")
