// Mini App Suite - Frontend JavaScript

let currentUser = null;

// Tab Switching
function switchTab(tabId) {
  const tabs = ['calc', 'ai-math', 'auth', 'ai-sec', 'pw-gen', 'ai-chat', 'history'];
  tabs.forEach(id => {
    const panel = document.getElementById(`tab-${id}`);
    const btn = document.getElementById(`tab-btn-${id}`);
    if (panel) {
      if (id === tabId) {
        panel.classList.remove('hidden');
        btn.classList.add('active', 'border-b-2', 'border-indigo-500', 'text-indigo-400', 'bg-slate-800/50');
        btn.classList.remove('text-slate-400');
      } else {
        panel.classList.add('hidden');
        btn.classList.remove('active', 'border-b-2', 'border-indigo-500', 'text-indigo-400', 'bg-slate-800/50');
        btn.classList.add('text-slate-400');
      }
    }
  });

  if (tabId === 'history') {
    refreshHistory();
  }
}

// ---------------- Calculator ----------------
function onOpChange() {
  const op = document.getElementById('calc-op').value;
  const bContainer = document.getElementById('calc-b-container');
  if (op === 'sqrt') {
    bContainer.classList.add('opacity-40', 'pointer-events-none');
    document.getElementById('calc-b').value = '';
  } else {
    bContainer.classList.remove('opacity-40', 'pointer-events-none');
  }
}

async function executeCalculate() {
  const a = document.getElementById('calc-a').value;
  const b = document.getElementById('calc-b').value;
  const op = document.getElementById('calc-op').value;
  const resultSpan = document.getElementById('calc-result');

  if (a === '') {
    alert('Please enter the first number.');
    return;
  }

  try {
    const payload = { operation: op, a: parseFloat(a) };
    if (op !== 'sqrt') {
      if (b === '') {
        alert('Please enter the second number.');
        return;
      }
      payload.b = parseFloat(b);
    }

    const res = await fetch('/api/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();

    if (data.success) {
      resultSpan.innerText = `${data.result}`;
      resultSpan.classList.remove('text-rose-400');
      resultSpan.classList.add('text-emerald-400');
    } else {
      resultSpan.innerText = `Error: ${data.error}`;
      resultSpan.classList.remove('text-emerald-400');
      resultSpan.classList.add('text-rose-400');
    }
  } catch (err) {
    resultSpan.innerText = `Network error: ${err}`;
  }
}

function clearCalcInputs() {
  document.getElementById('calc-a').value = '';
  document.getElementById('calc-b').value = '';
  document.getElementById('calc-result').innerText = '--';
}

// ---------------- AI Math Solver ----------------
function fillAiMath(text) {
  document.getElementById('ai-math-input').value = text;
  solveAiMath();
}

async function solveAiMath() {
  const query = document.getElementById('ai-math-input').value.trim();
  if (!query) return;

  const card = document.getElementById('ai-math-output');
  card.classList.remove('hidden');
  document.getElementById('ai-math-type').innerText = 'Computing...';
  document.getElementById('ai-math-form').innerText = 'Parsing...';
  document.getElementById('ai-math-result').innerText = '...';
  document.getElementById('ai-math-steps').innerHTML = '<li>Analyzing natural language math query...</li>';

  try {
    const res = await fetch('/api/ai/solve-math', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query }),
    });
    const data = await res.json();

    if (data.success) {
      document.getElementById('ai-math-type').innerText = data.type || 'Solved';
      document.getElementById('ai-math-form').innerText = data.interpreted_as || query;
      document.getElementById('ai-math-result').innerText = data.result;

      const stepsList = document.getElementById('ai-math-steps');
      stepsList.innerHTML = '';
      (data.steps || []).forEach(step => {
        const li = document.createElement('li');
        li.innerText = step;
        stepsList.appendChild(li);
      });
    } else {
      document.getElementById('ai-math-type').innerText = 'Failed';
      document.getElementById('ai-math-form').innerText = 'N/A';
      document.getElementById('ai-math-result').innerText = `Error: ${data.error}`;
      document.getElementById('ai-math-steps').innerHTML = `<li>${data.error}</li>`;
    }
  } catch (err) {
    document.getElementById('ai-math-result').innerText = `Network error: ${err}`;
  }
}

// ---------------- User & Auth ----------------
function togglePasswordVis() {
  const pw = document.getElementById('auth-password');
  pw.type = pw.type === 'password' ? 'text' : 'password';
}

async function checkLiveStrength() {
  const pw = document.getElementById('auth-password').value;
  const bar = document.getElementById('strength-bar');
  const label = document.getElementById('strength-label');

  if (!pw) {
    bar.style.width = '0%';
    label.innerText = 'None';
    return;
  }

  try {
    const res = await fetch('/api/password/strength', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password: pw }),
    });
    const data = await res.json();
    const s = data.analysis.score; // 0 - 5
    const pct = (s / 5) * 100;
    bar.style.width = `${pct}%`;

    if (s <= 2) {
      bar.className = 'h-full bg-rose-500 transition-all duration-300';
      label.innerText = 'Weak';
      label.className = 'text-xs text-rose-400 font-medium';
    } else if (s <= 4) {
      bar.className = 'h-full bg-amber-500 transition-all duration-300';
      label.innerText = 'Good';
      label.className = 'text-xs text-amber-400 font-medium';
    } else {
      bar.className = 'h-full bg-emerald-500 transition-all duration-300';
      label.innerText = 'Strong';
      label.className = 'text-xs text-emerald-400 font-medium';
    }
  } catch (err) {}
}

async function handleLogin() {
  const username = document.getElementById('auth-username').value.trim();
  const password = document.getElementById('auth-password').value;
  const msgBox = document.getElementById('auth-msg');

  if (!username || !password) {
    showAuthMsg('Please enter both username and password.', 'error');
    return;
  }

  try {
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    const data = await res.json();

    if (data.success) {
      currentUser = data.username;
      showAuthMsg(data.message, 'success');
      document.getElementById('session-text').innerText = `Logged in as: ${data.username} (${data.role})`;
      document.getElementById('logout-btn').classList.remove('hidden');
    } else {
      showAuthMsg(data.error, 'error');
    }
  } catch (err) {
    showAuthMsg(`Network error: ${err}`, 'error');
  }
}

async function handleRegister() {
  const username = document.getElementById('auth-username').value.trim();
  const password = document.getElementById('auth-password').value;

  if (!username || !password) {
    showAuthMsg('Please enter username and password to register.', 'error');
    return;
  }

  try {
    const res = await fetch('/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    const data = await res.json();

    if (data.success) {
      showAuthMsg(data.message, 'success');
      handleLogin();
    } else {
      showAuthMsg(data.error, 'error');
    }
  } catch (err) {
    showAuthMsg(`Network error: ${err}`, 'error');
  }
}

function logout() {
  currentUser = null;
  document.getElementById('session-text').innerText = 'Guest (Not logged in)';
  document.getElementById('logout-btn').classList.add('hidden');
  showAuthMsg('Logged out successfully.', 'info');
}

function showAuthMsg(text, type) {
  const msg = document.getElementById('auth-msg');
  msg.classList.remove('hidden', 'bg-rose-950/80', 'border-rose-700', 'text-rose-200', 'bg-emerald-950/80', 'border-emerald-700', 'text-emerald-200', 'bg-slate-900', 'text-slate-300');
  if (type === 'error') {
    msg.classList.add('bg-rose-950/80', 'border-rose-700', 'text-rose-200');
  } else if (type === 'success') {
    msg.classList.add('bg-emerald-950/80', 'border-emerald-700', 'text-emerald-200');
  } else {
    msg.classList.add('bg-slate-900', 'border-slate-700', 'text-slate-300');
  }
  msg.innerText = text;
}

// ---------------- AI Security Audit ----------------
async function runSecurityAudit(customPw = null) {
  const password = customPw || document.getElementById('sec-audit-input').value;
  if (!password) {
    alert('Please enter a password to audit.');
    return;
  }

  try {
    const res = await fetch('/api/ai/audit-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password }),
    });
    const data = await res.json();

    if (data.success) {
      const card = document.getElementById('audit-result-card');
      card.classList.remove('hidden');

      document.getElementById('audit-score').innerText = `${data.security_score}/100`;
      document.getElementById('audit-entropy').innerText = `${data.entropy_bits} bits`;
      document.getElementById('audit-length').innerText = `${data.password_length} chars`;
      document.getElementById('audit-level').innerText = data.security_level;
      document.getElementById('audit-crack-time').innerText = data.estimated_crack_time;

      const vulnList = document.getElementById('audit-vulnerabilities');
      vulnList.innerHTML = '';
      data.vulnerabilities.forEach(v => {
        const li = document.createElement('li');
        li.innerText = v;
        vulnList.appendChild(li);
      });

      const recList = document.getElementById('audit-recommendations');
      recList.innerHTML = '';
      data.recommendations.forEach(r => {
        const li = document.createElement('li');
        li.innerText = r;
        recList.appendChild(li);
      });
    }
  } catch (err) {
    alert(`Audit failed: ${err}`);
  }
}

// ---------------- Password Generator ----------------
async function handleGeneratePassword() {
  const length = parseInt(document.getElementById('gen-length').value, 10);
  const include_uppercase = document.getElementById('gen-upper').checked;
  const include_digits = document.getElementById('gen-digits').checked;
  const include_special = document.getElementById('gen-special').checked;

  try {
    const res = await fetch('/api/password/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ length, include_uppercase, include_digits, include_special }),
    });
    const data = await res.json();

    if (data.success) {
      document.getElementById('gen-pw-container').classList.remove('hidden');
      document.getElementById('gen-pw-output').innerText = data.password;
    }
  } catch (err) {
    alert(`Generation error: ${err}`);
  }
}

function copyGeneratedPassword() {
  const pw = document.getElementById('gen-pw-output').innerText;
  if (!pw) return;
  navigator.clipboard.writeText(pw);
  alert('Password copied to clipboard!');
}

function sendGeneratedToAudit() {
  const pw = document.getElementById('gen-pw-output').innerText;
  if (!pw) return;
  document.getElementById('sec-audit-input').value = pw;
  switchTab('ai-sec');
  runSecurityAudit(pw);
}

// ---------------- AI Assistant Chat ----------------
async function sendChatMessage() {
  const input = document.getElementById('chat-input');
  const prompt = input.value.trim();
  if (!prompt) return;

  const chatContainer = document.getElementById('chat-messages');
  const apiKey = document.getElementById('gemini-api-key').value.trim();

  // Append user message
  const userDiv = document.createElement('div');
  userDiv.className = 'flex items-start space-x-2 justify-end';
  userDiv.innerHTML = `
    <div class="bg-indigo-600 text-white p-3 rounded-xl rounded-tr-none text-xs max-w-xl">
      ${prompt}
    </div>
    <div class="w-7 h-7 rounded-lg bg-slate-700 flex items-center justify-center text-xs font-bold shrink-0">YOU</div>
  `;
  chatContainer.appendChild(userDiv);
  input.value = '';
  chatContainer.scrollTop = chatContainer.scrollHeight;

  // Append AI loading placeholder
  const aiLoadingDiv = document.createElement('div');
  aiLoadingDiv.className = 'flex items-start space-x-2';
  aiLoadingDiv.innerHTML = `
    <div class="w-7 h-7 rounded-lg bg-indigo-600 flex items-center justify-center text-xs font-bold shrink-0">AI</div>
    <div class="bg-slate-900 border border-slate-800 p-3 rounded-xl rounded-tl-none text-xs text-slate-400 italic max-w-xl">
      Thinking...
    </div>
  `;
  chatContainer.appendChild(aiLoadingDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;

  try {
    const res = await fetch('/api/ai/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt, api_key: apiKey }),
    });
    const data = await res.json();

    const providerTag = data.provider ? `<div class="mt-2 text-[10px] text-slate-500 font-mono">Powered by ${data.provider}</div>` : '';
    aiLoadingDiv.querySelector('.bg-slate-900').innerHTML = `
      <div class="text-slate-200 whitespace-pre-wrap">${data.reply}</div>
      ${providerTag}
    `;
    aiLoadingDiv.querySelector('.bg-slate-900').classList.remove('italic', 'text-slate-400');
  } catch (err) {
    aiLoadingDiv.querySelector('.bg-slate-900').innerText = `Error: ${err}`;
  }
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

// ---------------- Calculation History ----------------
async function refreshHistory() {
  const container = document.getElementById('history-container');
  try {
    const res = await fetch('/api/history');
    const data = await res.json();

    if (data.success && data.history && data.history.length > 0) {
      container.innerHTML = '';
      data.history.forEach((item, idx) => {
        const div = document.createElement('div');
        div.className = 'p-2 rounded bg-slate-900/80 border border-slate-800/80 flex items-center justify-between text-slate-300';
        div.innerHTML = `<span><strong class="text-indigo-400 font-semibold mr-2">#${idx + 1}</strong>${item}</span>`;
        container.appendChild(div);
      });
    } else {
      container.innerHTML = '<div class="text-slate-500 italic">No calculations recorded yet.</div>';
    }
  } catch (err) {
    container.innerHTML = `<div class="text-rose-400">Failed to load history: ${err}</div>`;
  }
}

async function clearHistory() {
  if (!confirm('Are you sure you want to clear calculation history?')) return;
  try {
    await fetch('/api/history', { method: 'DELETE' });
    refreshHistory();
  } catch (err) {
    alert(`Error clearing history: ${err}`);
  }
}
