"""
app.py
 
Streamlit UI for PawPal+. Thin presentation layer over the backend logic
in pawpal_system.py -- all scheduling intelligence (sorting, filtering,
conflict detection, recurrence) lives in Scheduler/Task and is simply
displayed here.
"""
 
import streamlit as st
 
from pawpal_system import Owner, Pet, Scheduler, Task
 
st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("Smart pet care scheduling for busy owners.")
 
# ---------------------------------------------------------------------------
# Session state ("memory" across Streamlit reruns)
# ---------------------------------------------------------------------------
if "owner" not in st.session_state:
    st.session_state.owner = Owner("My Household")
 
owner: Owner = st.session_state.owner
scheduler = Scheduler(owner)
 
# ---------------------------------------------------------------------------
# Add a pet
# ---------------------------------------------------------------------------
st.subheader("Pets")
 
with st.form("add_pet_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        pet_name = st.text_input("Pet name")
    with col2:
        species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Other"])
    with col3:
        age = st.number_input("Age", min_value=0, max_value=40, value=1)
    submitted_pet = st.form_submit_button("Add pet")
 
if submitted_pet:
    if pet_name.strip():
        owner.add_pet(Pet(pet_name.strip(), species, age))
        st.success(f"Added {pet_name} the {species}.")
    else:
        st.warning("Please enter a pet name.")
 
if not owner.pets:
    st.info("No pets yet. Add one above to get started.")
else:
    st.write(", ".join(f"{p.name} ({p.species})" for p in owner.pets))
 
st.divider()
 
# ---------------------------------------------------------------------------
# Add a task
# ---------------------------------------------------------------------------
st.subheader("Schedule a Task")
 
if owner.pets:
    with st.form("add_task_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            target_pet_name = st.selectbox("Pet", [p.name for p in owner.pets])
            description = st.text_input("Task description", value="Morning walk")
        with col2:
            time_value = st.time_input("Time")
            frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        submitted_task = st.form_submit_button("Add task")
 
    if submitted_task:
        pet = owner.find_pet(target_pet_name)
        time_str = time_value.strftime("%H:%M")
        pet.add_task(Task(description, time_str, frequency=frequency))
        st.success(f"Added '{description}' at {time_str} for {target_pet_name}.")
else:
    st.caption("Add a pet first to schedule tasks for them.")
 
st.divider()
 
# ---------------------------------------------------------------------------
# Today's schedule (sorted, with conflict warnings)
# ---------------------------------------------------------------------------
st.subheader("Today's Schedule")
 
filter_col1, filter_col2 = st.columns(2)
with filter_col1:
    pet_filter = st.selectbox("Filter by pet", ["All"] + [p.name for p in owner.pets])
with filter_col2:
    status_filter = st.selectbox("Filter by status", ["All", "Completed", "Incomplete"])
 
completed_arg = {"All": None, "Completed": True, "Incomplete": False}[status_filter]
pet_arg = None if pet_filter == "All" else pet_filter
 
tasks = scheduler.filter_tasks(pet_name=pet_arg, completed=completed_arg)
tasks = sorted(tasks, key=lambda t: t.time)
 
if tasks:
    st.table(
        [
            {
                "Time": t.time,
                "Task": t.description,
                "Frequency": t.frequency,
                "Done": "Yes" if t.completed else "No",
            }
            for t in tasks
        ]
    )
 
    for t in tasks:
        if not t.completed:
            if st.button(f"Mark '{t.description}' ({t.time}) complete", key=f"complete-{t.id}"):
                next_task = scheduler.mark_task_complete(t)
                if next_task:
                    st.success(f"Done! Next occurrence scheduled for {next_task.date}.")
                else:
                    st.success("Marked complete.")
                st.rerun()
else:
    st.info("No tasks match the current filters.")
 
# ---------------------------------------------------------------------------
# Conflict warnings
# ---------------------------------------------------------------------------
conflicts = scheduler.detect_conflicts()
if conflicts:
    st.subheader("Conflicts")
    for warning in conflicts:
        st.warning(warning)