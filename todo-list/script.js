const input = document.getElementById('todo-input');
const addBtn = document.getElementById('add-btn');
const list = document.getElementById('todo-list');

addBtn.addEventListener('click', addTodo);
input.addEventListener('keydown', function(event) {
  if (event.key === 'Enter') {
    addTodo();
  }
});

function addTodo() {
  const text = input.value.trim();
  if (text === '') return;
  const li = document.createElement('li');
  li.textContent = text;
  li.addEventListener('click', () => {
    li.classList.toggle('completed');
  });
  list.appendChild(li);
  input.value = '';
}
