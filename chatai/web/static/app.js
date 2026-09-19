// Private Character Chat — frontend. No build step, no external requests
// beyond this same-origin API.
"use strict";

const state = {
  characters: [],
  personas: [],
  chats: [],
  activeChat: null,       // full ChatSession object
  activeCharacter: null,
  activeTab: "chats",
  settings: null,
};

const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

async function api(path, opts = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...opts,
  });
  if (!res.ok) {
    let detail = res.statusText;
    try { detail = (await res.json()).detail || detail; } catch (_) {}
    throw new Error(detail);
  }
  const ct = res.headers.get("content-type") || "";
  return ct.includes("application/json") ? res.json() : res.text();
}

function initials(name) {
  return (name || "?").trim().split(/\s+/).slice(0, 2).map(w => w[0]?.toUpperCase() || "").join("");
}

function avatarHtml(entity, kind) {
  if (entity && entity.avatar) {
    return `<img src="/media/${kind}/${entity.avatar}" alt="">`;
  }
  return initials(entity ? entity.name : "?");
}

// ---------- Bootstrapping ----------

async function loadAll() {
  const [characters, personas, chats, settings] = await Promise.all([
    api("/api/characters"),
    api("/api/personas"),
    api("/api/chats"),
    api("/api/settings"),
  ]);
  state.characters = characters;
  state.personas = personas;
  state.chats = chats;
  state.settings = settings;

  if (state.personas.length === 0) {
    const p = await api("/api/personas", { method: "POST", body: JSON.stringify({ name: "You", description: "" }) });
    state.personas.push(p);
  }
  renderPersonaSelect();
  renderSidebar();
}

function renderPersonaSelect() {
  const sel = $("#persona-select");
  sel.innerHTML = state.personas.map(p => `<option value="${p.id}">${escapeHtml(p.name)}</option>`).join("")
    + `<option value="__manage__">+ Manage personas…</option>`;
  const saved = localStorage.getItem("chatai_persona_id");
  if (saved && state.personas.some(p => p.id === saved)) sel.value = saved;
}

document.addEventListener("change", (e) => {
  if (e.target && e.target.id === "persona-select") {
    if (e.target.value === "__manage__") {
      openPersonaModal();
      renderPersonaSelect();
      return;
    }
    localStorage.setItem("chatai_persona_id", e.target.value);
    if (state.activeChat) renderChatHeader();
  }
});

function escapeHtml(s) {
  return (s || "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

// ---------- Sidebar ----------

function renderSidebar() {
  $$(".tab").forEach(t => t.classList.toggle("active", t.dataset.tab === state.activeTab));
  $("#chats-list").style.display = state.activeTab === "chats" ? "" : "none";
  $("#characters-list").style.display = state.activeTab === "characters" ? "" : "none";

  const charById = Object.fromEntries(state.characters.map(c => [c.id, c]));

  $("#chats-list").innerHTML = state.chats.length
    ? state.chats.map(c => {
        const ch = charById[c.character_id];
        return `<div class="list-item ${state.activeChat && state.activeChat.id === c.id ? "active" : ""}" data-chat-id="${c.id}">
          <div class="avatar">${ch ? avatarHtml(ch, "characters") : "?"}</div>
          <div class="list-item-text">
            <div class="list-item-title">${escapeHtml(ch ? ch.name : "Unknown")}</div>
            <div class="list-item-sub">${escapeHtml(c.last_message || "No messages yet")}</div>
          </div>
        </div>`;
      }).join("")
    : `<div class="tiny-note" style="padding:12px">No chats yet. Open the Characters tab and start one.</div>`;

  $("#characters-list").innerHTML = state.characters.length
    ? state.characters.map(c => `
      <div class="list-item" data-char-id="${c.id}">
        <div class="avatar">${avatarHtml(c, "characters")}</div>
        <div class="list-item-text">
          <div class="list-item-title">${escapeHtml(c.name)}</div>
          <div class="list-item-sub">${escapeHtml(c.tags.join(", ") || c.description || "")}</div>
        </div>
        <button class="btn small char-start-chat" data-char-id="${c.id}">Chat</button>
        <button class="btn small icon char-edit" data-char-id="${c.id}" title="Edit">✎</button>
      </div>`).join("")
    : `<div class="tiny-note" style="padding:12px">No characters yet. Click "+ Character" below, or import a SillyTavern card.</div>`;
}

document.addEventListener("click", async (e) => {
  const tab = e.target.closest(".tab");
  if (tab) { state.activeTab = tab.dataset.tab; renderSidebar(); return; }

  const chatItem = e.target.closest("[data-chat-id]");
  if (chatItem && !e.target.closest("button")) {
    await openChat(chatItem.dataset.chatId);
    return;
  }

  const startBtn = e.target.closest(".char-start-chat");
  if (startBtn) {
    await startChatWithCharacter(startBtn.dataset.charId);
    return;
  }

  const editBtn = e.target.closest(".char-edit");
  if (editBtn) {
    openCharacterModal(state.characters.find(c => c.id === editBtn.dataset.charId));
    return;
  }
});

$("#btn-new-character").addEventListener("click", () => openCharacterModal(null));
$("#btn-settings").addEventListener("click", openSettingsModal);

// ---------- Chat ----------

function currentPersonaId() {
  return $("#persona-select").value !== "__manage__" ? $("#persona-select").value : null;
}

async function startChatWithCharacter(characterId) {
  const chat = await api("/api/chats", {
    method: "POST",
    body: JSON.stringify({ character_id: characterId, persona_id: currentPersonaId() || null }),
  });
  state.chats = await api("/api/chats");
  state.activeTab = "chats";
  await openChat(chat.id);
}

async function openChat(chatId) {
  const chat = await api(`/api/chats/${chatId}`);
  state.activeChat = chat;
  state.activeCharacter = state.characters.find(c => c.id === chat.character_id) || null;
  renderSidebar();
  renderChatHeader();
  renderMessages();
  $("#composer").style.display = "flex";
}

function renderChatHeader() {
  const ch = state.activeCharacter;
  $("#header-avatar").innerHTML = ch ? avatarHtml(ch, "characters") : "?";
  $("#header-name").textContent = ch ? ch.name : "No chat open";
  const persona = state.personas.find(p => p.id === currentPersonaId());
  $("#header-sub").textContent = persona ? `Playing as ${persona.name}` : "";
  $("#btn-export-char").style.display = ch ? "" : "none";
  $("#btn-delete-chat").style.display = state.activeChat ? "" : "none";
}

$("#btn-export-char").addEventListener("click", () => {
  if (state.activeCharacter) window.open(`/api/characters/${state.activeCharacter.id}/export`, "_blank");
});

$("#btn-delete-chat").addEventListener("click", async () => {
  if (!state.activeChat) return;
  if (!confirm("Delete this chat? This cannot be undone.")) return;
  await api(`/api/chats/${state.activeChat.id}`, { method: "DELETE" });
  state.chats = await api("/api/chats");
  state.activeChat = null;
  state.activeCharacter = null;
  $("#composer").style.display = "none";
  $("#messages").innerHTML = `<div class="empty-state"><h2>Pick or create a character</h2></div>`;
  renderChatHeader();
  renderSidebar();
});

function renderMessages() {
  const box = $("#messages");
  if (!state.activeChat) return;
  box.innerHTML = state.activeChat.messages.map(m => messageHtml(m)).join("");
  box.scrollTop = box.scrollHeight;
}

function messageHtml(m) {
  const isAssistant = m.role === "assistant";
  const text = isAssistant && m.swipes.length ? m.swipes[Math.max(0, Math.min(m.active_swipe, m.swipes.length - 1))] : m.content;
  const swipeControls = isAssistant && m.swipes.length > 1
    ? `<button class="swipe-prev" data-msg-id="${m.id}">‹</button><span>${m.active_swipe + 1}/${m.swipes.length}</span><button class="swipe-next" data-msg-id="${m.id}">›</button>`
    : "";
  return `<div class="msg-row ${m.role}" data-msg-id="${m.id}">
    <div class="msg-bubble">${escapeHtml(text)}</div>
    <div class="msg-meta">
      ${swipeControls}
      ${isAssistant ? `<button class="msg-regenerate" data-msg-id="${m.id}">Regenerate</button>` : ""}
      <button class="msg-edit" data-msg-id="${m.id}">Edit</button>
      <button class="msg-delete" data-msg-id="${m.id}">Delete</button>
    </div>
  </div>`;
}

$("#messages").addEventListener("click", async (e) => {
  const id = e.target.dataset && e.target.dataset.msgId;
  if (!id || !state.activeChat) return;

  if (e.target.classList.contains("msg-delete")) {
    if (!confirm("Delete this message?")) return;
    state.activeChat = await api(`/api/chats/${state.activeChat.id}/messages/${id}`, { method: "DELETE" });
    renderMessages();
  } else if (e.target.classList.contains("msg-edit")) {
    const msg = state.activeChat.messages.find(m => m.id === id);
    const current = msg.swipes.length ? msg.swipes[msg.active_swipe] : msg.content;
    const next = prompt("Edit message:", current);
    if (next !== null) {
      state.activeChat = await api(`/api/chats/${state.activeChat.id}/messages/${id}`, {
        method: "PUT", body: JSON.stringify({ content: next }),
      });
      renderMessages();
    }
  } else if (e.target.classList.contains("msg-regenerate")) {
    await streamGeneration("regenerate");
  } else if (e.target.classList.contains("swipe-prev") || e.target.classList.contains("swipe-next")) {
    const direction = e.target.classList.contains("swipe-next") ? "next" : "prev";
    state.activeChat = await api(`/api/chats/${state.activeChat.id}/swipe`, {
      method: "POST", body: JSON.stringify({ direction }),
    });
    renderMessages();
  }
});

const composerInput = $("#composer-input");
composerInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(); }
});
composerInput.addEventListener("input", () => {
  composerInput.style.height = "auto";
  composerInput.style.height = Math.min(140, composerInput.scrollHeight) + "px";
});
$("#btn-send").addEventListener("click", sendMessage);

async function sendMessage() {
  const text = composerInput.value.trim();
  if (!text || !state.activeChat) return;
  composerInput.value = "";
  composerInput.style.height = "auto";
  state.activeChat = await api(`/api/chats/${state.activeChat.id}/messages`, {
    method: "POST", body: JSON.stringify({ content: text }),
  });
  renderMessages();
  await streamGeneration("generate");
}

function streamGeneration(mode) {
  return new Promise((resolve) => {
    const chatId = state.activeChat.id;
    const box = $("#messages");

    // Placeholder bubble for the streaming reply (mode=generate only;
    // regenerate replaces the existing last bubble once it re-renders).
    let placeholder = null;
    if (mode === "generate") {
      placeholder = document.createElement("div");
      placeholder.className = "msg-row assistant";
      placeholder.innerHTML = `<div class="msg-bubble"><span class="live-text"></span><span class="typing-dots"><span></span><span></span><span></span></span></div>`;
      box.appendChild(placeholder);
      box.scrollTop = box.scrollHeight;
    }

    const es = new EventSource(`/api/chats/${chatId}/${mode}`);
    let acc = "";
    es.onmessage = async (ev) => {
      const data = JSON.parse(ev.data);
      if (data.error) {
        es.close();
        if (placeholder) placeholder.remove();
        alert(data.error);
        resolve();
        return;
      }
      if (data.delta) {
        acc += data.delta;
        if (placeholder) {
          placeholder.querySelector(".live-text").textContent = acc;
          box.scrollTop = box.scrollHeight;
        }
      }
      if (data.done) {
        es.close();
        state.activeChat = await api(`/api/chats/${chatId}`);
        state.chats = await api("/api/chats");
        renderMessages();
        renderSidebar();
        resolve();
      }
    };
    es.onerror = () => {
      es.close();
      if (placeholder) placeholder.remove();
      resolve();
    };
  });
}

// ---------- Character modal ----------

function openCharacterModal(character) {
  const isNew = !character;
  const c = character || {
    id: null, name: "", description: "", personality: "", scenario: "",
    first_mes: "", mes_example: "", system_prompt: "", post_history_instructions: "",
    creator_notes: "", tags: [], character_book: [],
  };

  const root = $("#modal-root");
  root.innerHTML = `
    <div class="modal-backdrop">
      <div class="modal">
        <div class="modal-header">
          <span>${isNew ? "New Character" : "Edit Character"}</span>
          <button class="btn icon" id="modal-close">✕</button>
        </div>
        <div class="modal-body">
          <div class="field row">
            <div>
              <label>Name</label>
              <input type="text" id="f-name" value="${escapeHtml(c.name)}">
            </div>
            <div>
              <label>Tags (comma separated)</label>
              <input type="text" id="f-tags" value="${escapeHtml(c.tags.join(", "))}">
            </div>
          </div>
          <div class="field">
            <label>Description (appearance, background)</label>
            <textarea id="f-description">${escapeHtml(c.description)}</textarea>
          </div>
          <div class="field">
            <label>Personality</label>
            <textarea id="f-personality">${escapeHtml(c.personality)}</textarea>
          </div>
          <div class="field">
            <label>Scenario (current situation/setting)</label>
            <textarea id="f-scenario">${escapeHtml(c.scenario)}</textarea>
          </div>
          <div class="field">
            <label>First message (sent when a new chat starts)</label>
            <textarea id="f-first-mes">${escapeHtml(c.first_mes)}</textarea>
          </div>
          <div class="field">
            <label>Example dialogue (optional, for tone/style)</label>
            <textarea id="f-mes-example">${escapeHtml(c.mes_example)}</textarea>
          </div>
          <div class="field">
            <label>System prompt override (optional; leave blank for default roleplay instructions)</label>
            <textarea id="f-system-prompt">${escapeHtml(c.system_prompt)}</textarea>
          </div>
          <div class="field">
            <label>Post-history instructions (optional; injected right before each reply)</label>
            <textarea id="f-phi">${escapeHtml(c.post_history_instructions)}</textarea>
          </div>
          <div class="field">
            <label>Lorebook / world info</label>
            <div id="lore-entries"></div>
            <button class="btn small" id="btn-add-lore">+ Add entry</button>
          </div>
          ${!isNew ? `<div class="field">
            <label>Avatar</label>
            <input type="file" id="f-avatar" accept="image/*">
          </div>` : ""}
        </div>
        <div class="modal-footer">
          ${!isNew ? `<button class="btn danger" id="btn-delete-char" style="margin-right:auto">Delete</button>` : ""}
          <label class="btn" style="display:flex;align-items:center">
            Import card <input type="file" id="f-import" accept=".json,.png" style="display:none">
          </label>
          <button class="btn" id="modal-cancel">Cancel</button>
          <button class="btn primary" id="modal-save">${isNew ? "Create" : "Save"}</button>
        </div>
      </div>
    </div>`;

  let loreEntries = (c.character_book || []).map(e => ({ ...e }));
  renderLoreEntries();

  function renderLoreEntries() {
    $("#lore-entries").innerHTML = loreEntries.map((e, i) => `
      <div class="lore-entry" data-idx="${i}">
        <button class="btn small icon remove" data-idx="${i}">✕</button>
        <div class="field">
          <label>Trigger keys (comma separated)</label>
          <input type="text" class="lore-keys" value="${escapeHtml(e.keys.join(", "))}">
        </div>
        <div class="field">
          <label>Content injected when triggered</label>
          <textarea class="lore-content">${escapeHtml(e.content)}</textarea>
        </div>
      </div>`).join("");
  }

  $("#btn-add-lore").addEventListener("click", () => {
    loreEntries.push({ keys: [], content: "", enabled: true, case_sensitive: false });
    renderLoreEntries();
  });

  $("#lore-entries").addEventListener("click", (e) => {
    if (e.target.classList.contains("remove")) {
      loreEntries.splice(Number(e.target.dataset.idx), 1);
      renderLoreEntries();
    }
  });

  function collectLore() {
    return $$(".lore-entry").map(row => ({
      keys: $(".lore-keys", row).value.split(",").map(s => s.trim()).filter(Boolean),
      content: $(".lore-content", row).value,
      enabled: true,
      case_sensitive: false,
    }));
  }

  $("#modal-close").addEventListener("click", closeModal);
  $("#modal-cancel").addEventListener("click", closeModal);

  const importInput = $("#f-import");
  importInput.addEventListener("change", async () => {
    const file = importInput.files[0];
    if (!file) return;
    const fd = new FormData();
    fd.append("file", file);
    try {
      const imported = await api("/api/characters/import", { method: "POST", body: fd, headers: {} });
      closeModal();
      state.characters = await api("/api/characters");
      renderSidebar();
      openCharacterModal(imported);
    } catch (err) {
      alert("Import failed: " + err.message);
    }
  });

  if (!isNew) {
    $("#f-avatar").addEventListener("change", async () => {
      const file = $("#f-avatar").files[0];
      if (!file) return;
      const fd = new FormData();
      fd.append("file", file);
      const updated = await api(`/api/characters/${c.id}/avatar`, { method: "POST", body: fd, headers: {} });
      state.characters = state.characters.map(x => x.id === updated.id ? updated : x);
      renderSidebar();
    });
    $("#btn-delete-char").addEventListener("click", async () => {
      if (!confirm(`Delete "${c.name}" and all its chats' character reference? Chats themselves are kept but will show as Unknown.`)) return;
      await api(`/api/characters/${c.id}`, { method: "DELETE" });
      state.characters = await api("/api/characters");
      closeModal();
      renderSidebar();
    });
  }

  $("#modal-save").addEventListener("click", async () => {
    const payload = {
      id: c.id || undefined,
      name: $("#f-name").value.trim() || "Unnamed",
      description: $("#f-description").value,
      personality: $("#f-personality").value,
      scenario: $("#f-scenario").value,
      first_mes: $("#f-first-mes").value,
      alternate_greetings: c.alternate_greetings || [],
      mes_example: $("#f-mes-example").value,
      system_prompt: $("#f-system-prompt").value,
      post_history_instructions: $("#f-phi").value,
      creator_notes: c.creator_notes || "",
      tags: $("#f-tags").value.split(",").map(s => s.trim()).filter(Boolean),
      character_book: collectLore(),
    };
    if (isNew) {
      await api("/api/characters", { method: "POST", body: JSON.stringify(payload) });
    } else {
      await api(`/api/characters/${c.id}`, { method: "PUT", body: JSON.stringify(payload) });
    }
    state.characters = await api("/api/characters");
    closeModal();
    renderSidebar();
  });
}

function closeModal() { $("#modal-root").innerHTML = ""; }

// ---------- Persona modal ----------

function openPersonaModal() {
  const root = $("#modal-root");
  function render() {
    root.innerHTML = `
      <div class="modal-backdrop">
        <div class="modal">
          <div class="modal-header"><span>Manage Personas</span><button class="btn icon" id="modal-close">✕</button></div>
          <div class="modal-body">
            <div id="persona-items">
              ${state.personas.map(p => `
                <div class="lore-entry" data-id="${p.id}">
                  <div class="field row">
                    <div><label>Name</label><input type="text" class="p-name" value="${escapeHtml(p.name)}"></div>
                    <div><label>&nbsp;</label><button class="btn danger small p-delete" data-id="${p.id}">Delete</button></div>
                  </div>
                  <div class="field"><label>Description (who the user is)</label><textarea class="p-desc">${escapeHtml(p.description)}</textarea></div>
                  <button class="btn small p-save" data-id="${p.id}">Save</button>
                </div>`).join("")}
            </div>
            <button class="btn small" id="p-add">+ New persona</button>
          </div>
          <div class="modal-footer"><button class="btn" id="modal-cancel">Close</button></div>
        </div>
      </div>`;

    $("#modal-close").addEventListener("click", closeModal);
    $("#modal-cancel").addEventListener("click", closeModal);
    $("#p-add").addEventListener("click", async () => {
      const p = await api("/api/personas", { method: "POST", body: JSON.stringify({ name: "New Persona", description: "" }) });
      state.personas.push(p);
      render();
    });
    $$(".p-save").forEach(btn => btn.addEventListener("click", async () => {
      const row = btn.closest(".lore-entry");
      const id = row.dataset.id;
      const updated = await api(`/api/personas/${id}`, {
        method: "PUT",
        body: JSON.stringify({ name: $(".p-name", row).value, description: $(".p-desc", row).value }),
      });
      state.personas = state.personas.map(p => p.id === id ? updated : p);
      renderPersonaSelect();
    }));
    $$(".p-delete").forEach(btn => btn.addEventListener("click", async () => {
      if (state.personas.length <= 1) { alert("Keep at least one persona."); return; }
      await api(`/api/personas/${btn.dataset.id}`, { method: "DELETE" });
      state.personas = state.personas.filter(p => p.id !== btn.dataset.id);
      renderPersonaSelect();
      render();
    }));
  }
  render();
}

// ---------- Settings modal ----------

async function openSettingsModal() {
  const s = await api("/api/settings");
  const root = $("#modal-root");
  root.innerHTML = `
    <div class="modal-backdrop">
      <div class="modal">
        <div class="modal-header"><span>Settings</span><button class="btn icon" id="modal-close">✕</button></div>
        <div class="modal-body">
          <p class="tiny-note">This app never sends your chats anywhere by itself. It only talks to
            whatever model server you point it at below — by default that's Ollama running on
            your own machine.</p>

          <div class="field">
            <label>Model backend</label>
            <select id="s-provider">
              <option value="ollama" ${s.provider.provider === "ollama" ? "selected" : ""}>Ollama (local, recommended)</option>
              <option value="openai_compatible" ${s.provider.provider === "openai_compatible" ? "selected" : ""}>OpenAI-compatible server (LM Studio / llama.cpp / koboldcpp / vLLM / cloud API)</option>
            </select>
          </div>
          <div class="field">
            <label>Base URL</label>
            <input type="text" id="s-base-url" value="${escapeHtml(s.provider.base_url)}">
            <div class="hint">Ollama default: http://127.0.0.1:11434 — LM Studio default: http://127.0.0.1:1234</div>
          </div>
          <div class="field">
            <label>API key (optional — only sent to the Base URL above)</label>
            <input type="password" id="s-api-key" value="${escapeHtml(s.provider.api_key)}">
          </div>
          <div class="field row">
            <div>
              <label>Model</label>
              <select id="s-model"></select>
            </div>
            <div>
              <label>&nbsp;</label>
              <button class="btn small" id="s-refresh-models">Refresh list</button>
            </div>
          </div>

          <div class="field">
            <label>Temperature</label>
            <div class="range-row"><input type="range" id="s-temp" min="0" max="2" step="0.05" value="${s.generation.temperature}"><span class="val" id="s-temp-val">${s.generation.temperature}</span></div>
          </div>
          <div class="field">
            <label>Top P</label>
            <div class="range-row"><input type="range" id="s-topp" min="0" max="1" step="0.01" value="${s.generation.top_p}"><span class="val" id="s-topp-val">${s.generation.top_p}</span></div>
          </div>
          <div class="field">
            <label>Top K</label>
            <div class="range-row"><input type="range" id="s-topk" min="0" max="200" step="1" value="${s.generation.top_k}"><span class="val" id="s-topk-val">${s.generation.top_k}</span></div>
          </div>
          <div class="field">
            <label>Repeat penalty</label>
            <div class="range-row"><input type="range" id="s-reppen" min="1" max="2" step="0.01" value="${s.generation.repeat_penalty}"><span class="val" id="s-reppen-val">${s.generation.repeat_penalty}</span></div>
          </div>
          <div class="field row">
            <div><label>Max reply tokens</label><input type="number" id="s-maxtok" value="${s.generation.max_tokens}"></div>
            <div><label>Context length</label><input type="number" id="s-ctx" value="${s.generation.context_length}"></div>
          </div>
          <div class="field">
            <label><input type="checkbox" id="s-memory" ${s.memory_enabled ? "checked" : ""}> Summarize old messages into long-term memory once history gets long</label>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn" id="modal-cancel">Cancel</button>
          <button class="btn primary" id="modal-save">Save</button>
        </div>
      </div>
    </div>`;

  ["temp", "topp", "topk", "reppen"].forEach(key => {
    const input = $(`#s-${key}`);
    input.addEventListener("input", () => { $(`#s-${key}-val`).textContent = input.value; });
  });

  async function refreshModels() {
    const modelSelect = $("#s-model");
    modelSelect.innerHTML = `<option>Loading…</option>`;
    try {
      const tempSettings = {
        ...s,
        provider: {
          provider: $("#s-provider").value,
          base_url: $("#s-base-url").value,
          api_key: $("#s-api-key").value,
          model: s.provider.model,
        },
      };
      await api("/api/settings", { method: "PUT", body: JSON.stringify(tempSettings) });
      const { models } = await api("/api/settings/models");
      modelSelect.innerHTML = models.map(m => `<option value="${escapeHtml(m)}" ${m === s.provider.model ? "selected" : ""}>${escapeHtml(m)}</option>`).join("")
        || `<option value="">No models found</option>`;
    } catch (err) {
      modelSelect.innerHTML = `<option value="">Could not reach server</option>`;
    }
  }
  $("#s-refresh-models").addEventListener("click", refreshModels);
  refreshModels();

  $("#modal-close").addEventListener("click", closeModal);
  $("#modal-cancel").addEventListener("click", closeModal);
  $("#modal-save").addEventListener("click", async () => {
    const updated = {
      provider: {
        provider: $("#s-provider").value,
        base_url: $("#s-base-url").value,
        api_key: $("#s-api-key").value,
        model: $("#s-model").value,
      },
      generation: {
        temperature: parseFloat($("#s-temp").value),
        top_p: parseFloat($("#s-topp").value),
        top_k: parseInt($("#s-topk").value, 10),
        repeat_penalty: parseFloat($("#s-reppen").value),
        max_tokens: parseInt($("#s-maxtok").value, 10),
        context_length: parseInt($("#s-ctx").value, 10),
        stop: [],
      },
      memory_enabled: $("#s-memory").checked,
      memory_trigger_tokens: s.memory_trigger_tokens,
    };
    state.settings = await api("/api/settings", { method: "PUT", body: JSON.stringify(updated) });
    closeModal();
  });
}

loadAll().catch(err => {
  $("#messages").innerHTML = `<div class="empty-state"><h2>Could not load app</h2><p>${escapeHtml(err.message)}</p></div>`;
});
