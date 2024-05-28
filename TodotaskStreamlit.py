import streamlit as st

# Define a Node class for the linked list
class Node:
    def __init__(self, task, priority, category, completed=False):
        self.task = task
        self.priority = priority
        self.category = category
        self.completed = completed
        self.next = None

# Define a LinkedList class
class LinkedList:
    def __init__(self):
        self.head = None

    def add_task(self, task, priority, category):
        new_node = Node(task, priority, category)
        new_node.next = self.head
        self.head = new_node

    def remove_task(self, task):
        current = self.head
        previous = None

        while current is not None:
            if current.task == task:
                if previous is not None:
                    previous.next = current.next
                else:
                    self.head = current.next
                break
            previous = current
            current = current.next

    def mark_task_completed(self, task):
        current = self.head

        while current is not None:
            if current.task == task:
                current.completed = True
                break
            current = current.next

    def edit_task(self, old_task, new_task, new_priority, new_category):
        current = self.head

        while current is not None:
            if current.task == old_task:
                current.task = new_task
                current.priority = new_priority
                current.category = new_category
                break
            current = current.next

    def display_tasks(self, filter_completed=None, filter_category=None):
        tasks = []
        current = self.head

        while current is not None:
            if (filter_completed is None or current.completed == filter_completed) and (filter_category is None or current.category == filter_category):
                tasks.append(current)
            current = current.next

        return tasks

# Create a Streamlit app
def main():
    st.title("Enhanced To-Do List App")

    # Initialize or retrieve the dictionary of tasks lists from session state
    if 'user_tasks' not in st.session_state:
        st.session_state.user_tasks = {}

    user_tasks = st.session_state.user_tasks

    # Sidebar for user identification
    st.sidebar.header("User Identification")
    user_email = st.sidebar.text_input("Your Email:")
    
    if user_email:
        if user_email not in user_tasks:
            user_tasks[user_email] = LinkedList()
        
        tasks_list = user_tasks[user_email]
        
        st.sidebar.subheader("Add Task")
        task_input = st.sidebar.text_input("Task:")
        priority_input = st.sidebar.slider("Priority (1-5):", 1, 5, 3)
        category_input = st.sidebar.text_input("Category:")
        if st.sidebar.button("Add Task"):
            if task_input and category_input:
                tasks_list.add_task(task_input, priority_input, category_input)

        # Sidebar for removing tasks
        st.sidebar.subheader("Remove Task")
        task_to_remove = st.sidebar.text_input("Task to Remove:")
        if st.sidebar.button("Remove Task"):
            if task_to_remove:
                tasks_list.remove_task(task_to_remove)

        # Sidebar for marking tasks as completed
        st.sidebar.subheader("Mark Task as Completed")
        task_to_complete = st.sidebar.text_input("Task to Complete:")
        if st.sidebar.button("Mark as Completed"):
            if task_to_complete:
                tasks_list.mark_task_completed(task_to_complete)

        # Sidebar for editing tasks
        st.sidebar.subheader("Edit Task")
        old_task = st.sidebar.text_input("Current Task Name:")
        new_task = st.sidebar.text_input("New Task Name:")
        new_priority = st.sidebar.slider("New Priority (1-5):", 1, 5, 3)
        new_category = st.sidebar.text_input("New Category:")
        if st.sidebar.button("Edit Task"):
            if old_task and new_task and new_category:
                tasks_list.edit_task(old_task, new_task, new_priority, new_category)

        # Sidebar for filtering tasks
        st.sidebar.subheader("Filter Tasks")
        filter_completed = st.sidebar.radio("Filter by Completion Status:", options=["All", "Completed", "Pending"])
        filter_category = st.sidebar.text_input("Filter by Category:")

        # Main content to display tasks
        st.write(f"## Your To-Do List ({user_email}):")
        filter_option = None if filter_completed == "All" else (filter_completed == "Completed")
        tasks = tasks_list.display_tasks(filter_completed=filter_option, filter_category=filter_category if filter_category else None)

        if not tasks:
            st.write("No tasks yet. Add some tasks using the sidebar!")

        for i, task_node in enumerate(tasks, start=1):
            status = "Completed" if task_node.completed else "Pending"
            st.write(f"{i}. {task_node.task} (Priority: {task_node.priority}, Status: {status}, Category: {task_node.category})")
    else:
        st.write("Please enter your email in the sidebar to manage your tasks.")

if __name__ == "__main__":
    main()
