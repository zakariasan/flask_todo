
function addTask() {
    const inputBox = document.getElementById("inputBox");
    console.log(inputBox.value)
    if (inputBox.value === "") {
        alert("You must write something")
        return;
    } else {
        fetch('/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content: inputBox.value.trim() })
        }).then(res => {
            if (res.ok) { return res.json(); }
            else { throw new Error('Error adding task') }
        })
            .then(_ => { window.location.reload(); })
            .catch(err => { console.error('Error:', err) })
    }
    inputBox.value = "";
    saveData();
}
document.addEventListener('DOMContentLoaded', function() {
    const listContainer = document.getElementById("listContainer");
    listContainer.addEventListener("click", function(e) {
        const item = e.target.parentElement.parentElement;
        const itemChecked = e.target;
        if (e.target.tagName === "LI") {
            e.target.classList.toggle("checked");
            updateTask(itemChecked.id, {completed : e.target.classList.contains('checked')});
            saveData();

        } else if (e.target.tagName === "SPAN") {
            
            item.remove();
            deleteTask(item.id);
            saveData();

        }
    })
});

function saveData() {
    localStorage.setItem("Todo", listContainer.innerHTML);
}

function deleteTask(id) {
    fetch(`/delete/${id}`, { method: 'DELETE' })
        .then(res => {
            if (res.ok)
                return res.json()
            else
                throw new Error('Failed to delete Task')
        })
        .catch(err => console.log(err))
}

function updateTask(id, data) {
    fetch(`/update/${id}`, {
        method : 'PATCH',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(res=> {
            if (res.ok) {
                return res.json();
            } else {
                throw new Error('Failed to update the Task')
            }
        })
    .catch(err=> console.log('Error', err))
}
