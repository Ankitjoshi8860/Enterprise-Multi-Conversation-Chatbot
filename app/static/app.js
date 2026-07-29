const state = { conversations: [], selectedId: null, loading: false };
const $ = (selector) => document.querySelector(selector);

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (character) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[character]));
}

function inlineMarkdown(value) {
  let html = escapeHtml(value);
  html = html.replace(/`([^`]+)`/g, "<code>$1</code>");
  html = html.replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');
  html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  return html;
}

// Small safe Markdown renderer: escape first, then add only known tags.
function renderMarkdown(markdown) {
  const lines = String(markdown).replace(/\r\n/g, "\n").split("\n");
  const output = []; let paragraph = []; let list = null; let inCode = false; let code = [];
  const flushParagraph = () => { if (paragraph.length) { output.push(`<p>${inlineMarkdown(paragraph.join(" "))}</p>`); paragraph = []; } };
  const closeList = () => { if (list) { output.push(`</${list}>`); list = null; } };
  for (const line of lines) {
    if (line.trim().startsWith("```")) { flushParagraph(); closeList(); if (inCode) { output.push(`<pre><code>${escapeHtml(code.join("\n"))}</code></pre>`); code = []; } inCode = !inCode; continue; }
    if (inCode) { code.push(line); continue; }
    const heading = line.match(/^(#{1,3})\s+(.+)$/); const item = line.match(/^\s*[-*]\s+(.+)$/); const ordered = line.match(/^\s*\d+\.\s+(.+)$/);
    if (heading) { flushParagraph(); closeList(); const level = heading[1].length; output.push(`<h${level}>${inlineMarkdown(heading[2])}</h${level}>`); continue; }
    if (item || ordered) { flushParagraph(); const kind = item ? "ul" : "ol"; if (list !== kind) { closeList(); output.push(`<${kind}>`); list = kind; } output.push(`<li>${inlineMarkdown((item || ordered)[1])}</li>`); continue; }
    if (!line.trim()) { flushParagraph(); closeList(); continue; }
    closeList(); paragraph.push(line.trim());
  }
  if (inCode) output.push(`<pre><code>${escapeHtml(code.join("\n"))}</code></pre>`); flushParagraph(); closeList(); return output.join("");
}

function showToast(message) { const toast = $("#toast"); toast.textContent = message; toast.classList.add("show"); setTimeout(() => toast.classList.remove("show"), 4000); }
async function request(url, options = {}) { const response = await fetch(url, { headers: { "Content-Type": "application/json" }, ...options }); if (!response.ok) { const error = await response.json().catch(() => ({})); throw new Error(error.detail || "Something went wrong. Please try again."); } return response.status === 204 ? null : response.json(); }
function formatTime(timestamp) { return new Date(timestamp).toLocaleString([], { dateStyle: "medium", timeStyle: "short" }); }
function renderConversations() { const list = $("#conversation-list"); list.innerHTML = state.conversations.map((conversation) => `<div class="conversation-item ${conversation.id === state.selectedId ? "active" : ""}"><button class="conversation-name" data-id="${conversation.id}" type="button">${escapeHtml(conversation.title)}</button><button class="delete-button" data-delete="${conversation.id}" type="button" aria-label="Delete ${escapeHtml(conversation.title)}">×</button></div>`).join(""); }
function renderMessages(messages) { const list = $("#message-list"); if (!messages.length) { list.innerHTML = '<div id="empty-state" class="empty-state"><div class="empty-icon">✦</div><h2>How can I help you today?</h2><p>Ask about common health topics in simple language. MediAssist AI provides educational information, not a diagnosis.</p></div>'; return; } list.innerHTML = messages.map((message) => `<article class="message ${message.role === "user" ? "user" : "assistant"}"><div class="avatar">${message.role === "user" ? "You" : "MA"}</div><div><div class="message-body">${message.role === "assistant" ? renderMarkdown(message.content) : `<p>${escapeHtml(message.content)}</p>`}</div><div class="timestamp">${formatTime(message.timestamp)}</div></div></article>`).join(""); list.scrollTop = list.scrollHeight; }
async function loadConversations() { state.conversations = await request("/conversations"); renderConversations(); if (state.selectedId && state.conversations.some((c) => c.id === state.selectedId)) await selectConversation(state.selectedId); else if (state.conversations.length) await selectConversation(state.conversations[0].id); }
async function selectConversation(id) { state.selectedId = id; const conversation = await request(`/conversations/${id}`); $("#conversation-title").textContent = conversation.title; $("#rename-chat").disabled = false; renderConversations(); renderMessages(conversation.messages); $(".sidebar").classList.remove("open"); }
async function createConversation() { const conversation = await request("/conversations", { method: "POST", body: JSON.stringify({ title: "New conversation" }) }); state.conversations.unshift(conversation); await selectConversation(conversation.id); }
async function renameConversation() { if (!state.selectedId) return; const title = window.prompt("Conversation title", $("#conversation-title").textContent); if (!title || !title.trim()) return; const conversation = await request(`/conversations/${state.selectedId}`, { method: "PATCH", body: JSON.stringify({ title: title.trim() }) }); state.conversations = state.conversations.map((item) => item.id === conversation.id ? conversation : item); $("#conversation-title").textContent = conversation.title; renderConversations(); }
async function deleteConversation(id) { await request(`/conversations/${id}`, { method: "DELETE" }); state.conversations = state.conversations.filter((conversation) => conversation.id !== id); state.selectedId = null; $("#rename-chat").disabled = true; $("#conversation-title").textContent = "New conversation"; renderConversations(); renderMessages([]); if (state.conversations.length) await selectConversation(state.conversations[0].id); }
async function sendMessage(event) { event.preventDefault(); const input = $("#message-input"); const content = input.value.trim(); if (!content || state.loading) return; if (!state.selectedId) { await createConversation(); } state.loading = true; $("#send-button").disabled = true; input.disabled = true; try { const result = await request(`/conversations/${state.selectedId}/messages`, { method: "POST", body: JSON.stringify({ content }) }); const conversation = await request(`/conversations/${state.selectedId}`); renderMessages(conversation.messages); input.value = ""; } catch (error) { showToast(error.message); } finally { state.loading = false; $("#send-button").disabled = false; input.disabled = false; input.focus(); } }
$("#new-chat").addEventListener("click", () => createConversation().catch((error) => showToast(error.message))); $("#rename-chat").addEventListener("click", () => renameConversation().catch((error) => showToast(error.message))); $("#message-form").addEventListener("submit", sendMessage); $("#menu-toggle").addEventListener("click", () => $(".sidebar").classList.toggle("open")); $("#conversation-list").addEventListener("click", (event) => { const id = Number(event.target.dataset.id || event.target.dataset.delete); if (!id) return; if (event.target.dataset.delete) deleteConversation(id).catch((error) => showToast(error.message)); else selectConversation(id).catch((error) => showToast(error.message)); }); loadConversations().catch((error) => showToast(error.message));
