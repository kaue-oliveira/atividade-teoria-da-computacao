let currentAutomataId = null;
let currentAutomataType = 'afd';
const API_URL = 'http://localhost:8000';

function switchTab(type) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById(type).classList.add('active');
    document.querySelector(`button[onclick="switchTab('${type}')"]`).classList.add('active');
    currentAutomataType = type;
}

async function createAutomata(type, data) {
    try {
        const response = await fetch(`${API_URL}/${type}/create`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        showResult(`Automata created with ID: ${result.id}`, true);
        console.log("Created automata ID:", result.id);
        currentAutomataId = result.id;
        document.getElementById('test-section').classList.remove('hidden');
        updateVisualization();
        return true;
    } catch (error) {
        showResult(`Error: ${error.message}`, false);
        return false;
    }
}

async function testInput() {
  const input = document.getElementById('test-input').value.trim();
  try {
      const response = await fetch(`${API_URL}/${currentAutomataType}/${currentAutomataId}/accept?string=${input}`, {
          method: 'POST'
      });
      const result = await response.json();
      showResult(`Input '${input}' ${result.accepted ? 'accepted' : 'rejected'}`, result.accepted);
      console.log('Test result:', result);
  } catch (error) {
      console.error('Test error:', error);
      showResult(`Error testing input: ${error.message}`, false);
  }
}

async function updateVisualization() {
    try {
        const img = document.createElement('img');
        img.src = `${API_URL}/${currentAutomataType}/${currentAutomataId}/visualize`;
        const vizDiv = document.getElementById('visualization');
        vizDiv.innerHTML = '';
        vizDiv.appendChild(img);
    } catch (error) {
        console.error('Error updating visualization:', error);
    }
}

function showResult(message, success) {
    const resultDiv = document.getElementById('result');
    resultDiv.textContent = message;
    resultDiv.className = success ? 'success' : 'error';
}

// Form submission handlers
document.getElementById('afd-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        states: document.getElementById('afd-states').value.split(',').map(s => s.trim()),
        input_symbols: document.getElementById('afd-symbols').value.split(',').map(s => s.trim()),
        transitions: JSON.parse(document.getElementById('afd-transitions').value),
        initial_state: document.getElementById('afd-initial').value.trim(),
        final_states: document.getElementById('afd-final').value.split(',').map(s => s.trim())
    };
    await createAutomata('afd', data);
});

document.getElementById('pda-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        states: document.getElementById('pda-states').value.split(',').map(s => s.trim()),
        input_symbols: document.getElementById('pda-symbols').value.split(',').map(s => s.trim()),
        stack_symbols: document.getElementById('pda-stack-symbols').value.split(',').map(s => s.trim()),
        transitions: JSON.parse(document.getElementById('pda-transitions').value),
        initial_state: document.getElementById('pda-initial').value.trim(),
        initial_stack_symbol: document.getElementById('pda-initial-stack').value.trim(),
        final_states: document.getElementById('pda-final').value.split(',').map(s => s.trim())
    };
    await createAutomata('pda', data);
});

document.getElementById('tm-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        states: document.getElementById('tm-states').value.split(',').map(s => s.trim()),
        input_symbols: document.getElementById('tm-symbols').value.split(',').map(s => s.trim()),
        tape_symbols: document.getElementById('tm-tape-symbols').value.split(',').map(s => s.trim()),
        transitions: JSON.parse(document.getElementById('tm-transitions').value),
        initial_state: document.getElementById('tm-initial').value.trim(),
        blank_symbol: document.getElementById('tm-blank').value.trim(),
        final_states: document.getElementById('tm-final').value.split(',').map(s => s.trim())
    };
    await createAutomata('tm', data);
});
