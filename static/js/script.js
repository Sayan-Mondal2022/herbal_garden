// Note modal display handling
const noteButton = document.querySelector('.note-button');
const noteModal = document.querySelector('.note-modal');
const notesList = document.getElementById('notes-list');
const closeNoteButton = document.getElementById('close-note');

noteButton.addEventListener('click', () => {
    noteModal.style.display = 'flex';
});

closeNoteButton.addEventListener('click', () => {
    noteModal.style.display = 'none';
});

document.getElementById('save-note').addEventListener('click', () => {
    const noteText = document.getElementById('note-textarea').value;
    if (noteText) {
        addNoteToList(noteText);
        saveNoteToLocalStorage(noteText);
        document.getElementById('note-textarea').value = '';
        noteModal.style.display = 'none';
    }
});

function addNoteToList(noteText) {
    const noteItem = document.createElement('li');
    noteItem.textContent = noteText;

    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Delete';
    deleteButton.addEventListener('click', () => {
        noteItem.remove();
        deleteNoteFromLocalStorage(noteText);
    });

    noteItem.appendChild(deleteButton);
    notesList.appendChild(noteItem);
}

function saveNoteToLocalStorage(noteText) {
    const notes = JSON.parse(localStorage.getItem('notes')) || [];
    notes.push(noteText);
    localStorage.setItem('notes', JSON.stringify(notes));
}

function deleteNoteFromLocalStorage(noteText) {
    let notes = JSON.parse(localStorage.getItem('notes')) || [];
    notes = notes.filter(note => note !== noteText);
    localStorage.setItem('notes', JSON.stringify(notes));
}

function loadNotes() {
    const notes = JSON.parse(localStorage.getItem('notes')) || [];
    notes.forEach(note => addNoteToList(note));
}

window.onload = loadNotes;
