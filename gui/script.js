const startBtn = document.getElementById('start-btn');
const repoInput = document.getElementById('repo_path');
const promptInput = document.getElementById('prompt');
const consoleEl = document.getElementById('console');
const consoleWrapper = document.getElementById('console-wrapper');
const statusText = document.getElementById('status-text');
const statusContainer = document.getElementById('status');
const clearBtn = document.getElementById('clear-btn');
const scrollBtn = document.getElementById('scroll-btn');

let autoScroll = true;
let ws;

// Connect to WebSocket
function connect() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    ws = new WebSocket(`${protocol}//${window.location.host}/ws`);

    ws.onopen = () => {
        statusText.innerText = 'Connected';
        statusContainer.classList.add('connected');
    };

    ws.onclose = () => {
        statusText.innerText = 'Disconnected';
        statusContainer.classList.remove('connected');
        setTimeout(connect, 3000); // Reconnect after 3s
    };

    ws.onmessage = (event) => {
        const message = JSON.parse(event.data);
        if (message.type === 'log') {
            appendLog(message.data);
        }
    };
}

// Format and filter logs to be concise
function appendLog(data) {
    const entry = document.createElement('div');
    entry.className = 'console-entry';

    // Concise logic: Only show important events
    let text = data.trim();
    
    // Agent Start
    if (text.includes('Agent:')) {
        const agentName = text.match(/Agent: (.*)/)?.[1] || 'Agent';
        text = `🤖 ${agentName} is thinking...`;
        entry.classList.add('agent');
    } 
    // Tool Execution
    else if (text.includes('Tool:')) {
        const toolName = text.match(/Tool: (.*)/)?.[1] || 'Tool';
        text = `🔧 Executing tool: ${toolName}`;
        entry.classList.add('tool');
    }
    // Success/Completion
    else if (text.includes('COMPLETE') || text.includes('Final Answer')) {
        text = `✅ ${text}`;
        entry.classList.add('success');
        setRunning(false);
    }
    // Error
    else if (text.includes('Error:') || text.includes('Exception:')) {
        text = `❌ ${text}`;
        entry.classList.add('error');
        setRunning(false);
    }
    // System messages
    else if (text.includes('Initiating') || text.includes('Starting')) {
        entry.classList.add('system');
    }
    // Skip noise
    else if (text.length < 5 || text.includes('┌') || text.includes('└') || text.includes('│')) {
        return; 
    }

    entry.innerText = text;
    consoleEl.appendChild(entry);

    if (autoScroll) {
        consoleWrapper.scrollTop = consoleWrapper.scrollHeight;
    }
}

function setRunning(isRunning) {
    if (isRunning) {
        startBtn.classList.add('running');
        startBtn.disabled = true;
    } else {
        startBtn.classList.remove('running');
        startBtn.disabled = false;
    }
}

// Start Analysis
startBtn.addEventListener('click', async () => {
    const repo_path = repoInput.value.trim();
    const prompt = promptInput.value.trim();

    if (!repo_path || !prompt) {
        alert('Please fill in both fields.');
        return;
    }

    setRunning(true);
    appendLog(`[SYSTEM] Starting analysis on ${repo_path}...`);

    try {
        const response = await fetch('/api/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ repo_path, prompt })
        });
        const result = await response.json();
        if (result.status !== 'success') {
            appendLog(`[ERROR] ${result.message}`);
            setRunning(false);
        }
    } catch (err) {
        appendLog(`[ERROR] Failed to connect to backend.`);
        setRunning(false);
    }
});

// Console Actions
clearBtn.addEventListener('click', () => {
    consoleEl.innerHTML = '';
});

scrollBtn.addEventListener('click', () => {
    autoScroll = !autoScroll;
    scrollBtn.classList.toggle('active', autoScroll);
});

// Initialize
connect();
