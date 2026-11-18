/**
 * PageSage AI Book Assistant - Frontend Application
 */

document.addEventListener('DOMContentLoaded', () => {
    // State
    const state = {
        conversation: [],
        spoilerShield: true,
        apiKey: localStorage.getItem('pagesage_gemini_key') || '',
        preferences: JSON.parse(localStorage.getItem('pagesage_preferences') || '{"genres":[],"authors":""}'),
        bookshelf: JSON.parse(localStorage.getItem('pagesage_bookshelf') || '{"want":[],"reading":[],"finished":[]}'),
        activeShelfTab: 'want',
        theme: localStorage.getItem('pagesage_theme') || 'dark',
        isGenerating: false
    };

    // DOM Elements
    const chatContainer = document.getElementById('chatContainer');
    const messagesList = document.getElementById('messagesList');
    const welcomeScreen = document.getElementById('welcomeScreen');
    const typingIndicator = document.getElementById('typingIndicator');
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const sendBtn = document.getElementById('sendBtn');
    
    const sidebar = document.getElementById('sidebar');
    const toggleSidebarBtn = document.getElementById('toggleSidebarBtn');
    const closeSidebarBtn = document.getElementById('closeSidebarBtn');
    const newChatBtn = document.getElementById('newChatBtn');
    
    const spoilerShieldToggle = document.getElementById('spoilerShieldToggle');
    const spoilerShieldText = document.getElementById('spoilerShieldText');
    const inputSpoilerBtn = document.getElementById('inputSpoilerBtn');
    const shieldActiveHint = document.getElementById('shieldActiveHint');
    
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const themeIcon = document.getElementById('themeIcon');
    
    const openSettingsBtn = document.getElementById('openSettingsBtn');
    const closeSettingsModalBtn = document.getElementById('closeSettingsModalBtn');
    const settingsModal = document.getElementById('settingsModal');
    const saveSettingsBtn = document.getElementById('saveSettingsBtn');
    const resetSettingsBtn = document.getElementById('resetSettingsBtn');
    const geminiApiKeyInput = document.getElementById('geminiApiKeyInput');
    const toggleApiKeyVisibility = document.getElementById('toggleApiKeyVisibility');
    const apiKeyEyeIcon = document.getElementById('apiKeyEyeIcon');
    const favAuthorsInput = document.getElementById('favAuthorsInput');
    const genreChipsSelector = document.getElementById('genreChipsSelector');
    
    const currentEngineLabel = document.getElementById('currentEngineLabel');
    const headerStatusText = document.getElementById('headerStatusText');
    
    const bookshelfList = document.getElementById('bookshelfList');
    const wantCount = document.getElementById('wantCount');
    const readingCount = document.getElementById('readingCount');
    const finishedCount = document.getElementById('finishedCount');
    const exportBookshelfBtn = document.getElementById('exportBookshelfBtn');
    
    const bookModal = document.getElementById('bookModal');
    const closeBookModalBtn = document.getElementById('closeBookModalBtn');
    const bookModalTitle = document.getElementById('bookModalTitle');
    const bookModalContent = document.getElementById('bookModalContent');

    // ==========================================
    // Initialization
    // ==========================================
    initTheme();
    initSettings();
    initEngineBadge();
    renderBookshelf();
    setupEventListeners();
    refreshIcons();

    // Auto-fill starter sample bookshelf if completely empty
    if (!state.bookshelf.want.length && !state.bookshelf.reading.length && !state.bookshelf.finished.length) {
        state.bookshelf.want.push({
            id: "project-hail-mary",
            title: "Project Hail Mary",
            author: "Andy Weir",
            year: 2021,
            genre: "Science Fiction",
            rating: 4.8,
            cover_url: "https://covers.openlibrary.org/b/id/10522956-M.jpg"
        });
        saveBookshelf();
        renderBookshelf();
    }

    function refreshIcons() {
        if (window.lucide) {
            window.lucide.createIcons();
        }
    }

    // ==========================================
    // Theme Management
    // ==========================================
    function initTheme() {
        document.documentElement.setAttribute('data-theme', state.theme);
        updateThemeIcon();
    }

    function toggleTheme() {
        state.theme = state.theme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', state.theme);
        localStorage.setItem('pagesage_theme', state.theme);
        updateThemeIcon();
    }

    function updateThemeIcon() {
        if (themeIcon) {
            themeIcon.setAttribute('data-lucide', state.theme === 'dark' ? 'sun' : 'moon');
            refreshIcons();
        }
    }

    // ==========================================
    // Settings & Engine Badge
    // ==========================================
    function initSettings() {
        if (geminiApiKeyInput) geminiApiKeyInput.value = state.apiKey;
        if (favAuthorsInput) favAuthorsInput.value = state.preferences.authors || '';
        
        // Highlight selected genre pills
        if (genreChipsSelector) {
            const selectedGenres = new Set(state.preferences.genres || []);
            genreChipsSelector.querySelectorAll('.genre-pill').forEach(pill => {
                if (selectedGenres.has(pill.dataset.genre)) {
                    pill.classList.add('selected');
                }
            });
        }
    }

    function initEngineBadge() {
        if (state.apiKey) {
            currentEngineLabel.textContent = "Gemini 2.5 Flash";
            headerStatusText.textContent = "Connected to Gemini Cloud AI";
        } else {
            currentEngineLabel.textContent = "PageSage Literary Core";
            headerStatusText.textContent = "Offline Literary Engine Active";
        }
    }

    // ==========================================
    // Spoiler Shield Management
    // ==========================================
    function setSpoilerShield(enabled) {
        state.spoilerShield = enabled;
        spoilerShieldToggle.checked = enabled;
        spoilerShieldText.textContent = enabled ? 'Spoiler Shield ON' : 'Spoiler Shield OFF';
        shieldActiveHint.textContent = enabled ? '🛡️ Spoiler Shield Active' : '⚡ Spoilers Allowed';
        inputSpoilerBtn.classList.toggle('active', enabled);
    }

    // ==========================================
    // Chat & Message Handling
    // ==========================================
    async function sendMessage(text) {
        const query = (text || messageInput.value).trim();
        if (!query || state.isGenerating) return;

        // Hide welcome screen
        if (welcomeScreen) welcomeScreen.style.display = 'none';

        // Clear input and reset height
        messageInput.value = '';
        messageInput.style.height = 'auto';

        // Add user message to UI & history
        appendMessage('user', query);
        state.conversation.push({ role: 'user', content: query });

        // Show typing indicator
        state.isGenerating = true;
        typingIndicator.style.display = 'flex';
        sendBtn.disabled = true;
        chatContainer.scrollTop = chatContainer.scrollHeight;

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: query,
                    conversation_history: state.conversation.slice(-8),
                    api_key: state.apiKey,
                    spoiler_shield: state.spoilerShield,
                    preferences: state.preferences
                })
            });

            const data = await response.json();
            typingIndicator.style.display = 'none';

            if (data.error) {
                appendMessage('assistant', `⚠️ **Error**: ${data.error}\n\n*${data.details || 'Please check your connection and try again.'}*`);
            } else {
                appendMessage('assistant', data.text, data.book_cards, data.engine, data.model, data.notice);
                state.conversation.push({ role: 'assistant', content: data.text });
            }
        } catch (err) {
            typingIndicator.style.display = 'none';
            appendMessage('assistant', `⚠️ **Network Exception**: Unable to contact PageSage server.\n\n*${err.message}*`);
        } finally {
            state.isGenerating = false;
            sendBtn.disabled = false;
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    }

    function appendMessage(role, content, bookCards = [], engine = null, model = null, notice = null) {
        const row = document.createElement('div');
        row.className = `message-row ${role}`;

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = role === 'user' 
            ? '<i data-lucide="user"></i>' 
            : '<i data-lucide="sparkles"></i>';

        const contentWrapper = document.createElement('div');
        contentWrapper.className = 'message-content';

        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';

        if (role === 'assistant') {
            let renderedHtml = marked.parse(content || '');
            if (notice) {
                renderedHtml = `<div style="font-size: 0.8rem; color: var(--accent); margin-bottom: 0.75rem; padding: 0.4rem 0.6rem; background: var(--accent-dim); border-radius: 6px;">ℹ️ ${notice}</div>` + renderedHtml;
            }
            bubble.innerHTML = renderedHtml;

            // Render Book Cards if present
            if (bookCards && bookCards.length > 0) {
                const grid = document.createElement('div');
                grid.className = 'book-cards-grid';
                
                bookCards.forEach(book => {
                    const card = createBookCardElement(book);
                    grid.appendChild(card);
                });
                bubble.appendChild(grid);
            }
        } else {
            bubble.textContent = content;
        }

        contentWrapper.appendChild(bubble);

        // Action bar for assistant messages
        if (role === 'assistant') {
            const metaBar = document.createElement('div');
            metaBar.className = 'message-actions';
            
            if (model) {
                const engineTag = document.createElement('span');
                engineTag.className = 'message-engine-tag';
                engineTag.textContent = model;
                metaBar.appendChild(engineTag);
            }

            const copyBtn = document.createElement('button');
            copyBtn.className = 'icon-btn text-btn';
            copyBtn.innerHTML = '<i data-lucide="copy" class="icon-sm"></i> Copy';
            copyBtn.title = 'Copy response text';
            copyBtn.onclick = () => {
                navigator.clipboard.writeText(content);
                copyBtn.innerHTML = '<i data-lucide="check" class="icon-sm"></i> Copied!';
                setTimeout(() => {
                    copyBtn.innerHTML = '<i data-lucide="copy" class="icon-sm"></i> Copy';
                    refreshIcons();
                }, 2000);
            };
            metaBar.appendChild(copyBtn);

            contentWrapper.appendChild(metaBar);
        }

        if (role === 'user') {
            row.appendChild(contentWrapper);
            row.appendChild(avatar);
        } else {
            row.appendChild(avatar);
            row.appendChild(contentWrapper);
        }

        messagesList.appendChild(row);
        refreshIcons();
    }

    function createBookCardElement(book) {
        const card = document.createElement('div');
        card.className = 'book-card';

        const coverImg = document.createElement('img');
        coverImg.className = 'book-card-cover';
        coverImg.src = book.cover_url || 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?auto=format&fit=crop&q=80&w=120';
        coverImg.alt = book.title;
        coverImg.onerror = () => {
            coverImg.src = 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?auto=format&fit=crop&q=80&w=120';
        };

        const details = document.createElement('div');
        details.className = 'book-card-details';

        const title = document.createElement('div');
        title.className = 'book-card-title';
        title.textContent = book.title;
        title.title = book.title;

        const author = document.createElement('div');
        author.className = 'book-card-author';
        author.textContent = book.author ? `by ${book.author}` : '';

        const meta = document.createElement('div');
        meta.className = 'book-card-meta';
        meta.innerHTML = `<span>⭐ ${book.rating || '4.5'}</span> <span>•</span> <span>${book.genre || 'Literature'}</span>`;

        const btnRow = document.createElement('div');
        btnRow.style.display = 'flex';
        btnRow.style.gap = '6px';

        const addBtn = document.createElement('button');
        addBtn.className = 'book-card-btn';
        addBtn.innerHTML = '<i data-lucide="plus" style="width: 12px; height: 12px;"></i> Add';
        addBtn.onclick = (e) => {
            e.stopPropagation();
            addToBookshelf(book, 'want');
            addBtn.innerHTML = '<i data-lucide="check" style="width: 12px; height: 12px;"></i> Saved';
            setTimeout(() => {
                addBtn.innerHTML = '<i data-lucide="plus" style="width: 12px; height: 12px;"></i> Add';
                refreshIcons();
            }, 1800);
        };

        const detailsBtn = document.createElement('button');
        detailsBtn.className = 'book-card-btn';
        detailsBtn.style.backgroundColor = 'transparent';
        detailsBtn.innerHTML = '<i data-lucide="info" style="width: 12px; height: 12px;"></i> Details';
        detailsBtn.onclick = () => openBookModal(book);

        btnRow.appendChild(addBtn);
        btnRow.appendChild(detailsBtn);

        details.appendChild(title);
        details.appendChild(author);
        details.appendChild(meta);
        details.appendChild(btnRow);

        card.appendChild(coverImg);
        card.appendChild(details);

        return card;
    }

    // ==========================================
    // Bookshelf Manager
    // ==========================================
    function addToBookshelf(book, shelf = 'want') {
        const item = {
            id: book.id || book.title.toLowerCase().replace(/[^a-z0-9]/g, '-'),
            title: book.title,
            author: book.author || 'Unknown',
            cover_url: book.cover_url || '',
            rating: book.rating || 4.5,
            genre: book.genre || 'Fiction',
            year: book.year || '',
            description: book.description || '',
            themes: book.themes || [],
            discussion_questions: book.discussion_questions || [],
            read_alikes: book.read_alikes || []
        };

        // Remove from other shelves first
        ['want', 'reading', 'finished'].forEach(s => {
            state.bookshelf[s] = state.bookshelf[s].filter(b => b.id !== item.id);
        });

        state.bookshelf[shelf].unshift(item);
        saveBookshelf();
        renderBookshelf();
    }

    function removeFromBookshelf(bookId) {
        ['want', 'reading', 'finished'].forEach(s => {
            state.bookshelf[s] = state.bookshelf[s].filter(b => b.id !== bookId);
        });
        saveBookshelf();
        renderBookshelf();
    }

    function moveBookshelfItem(bookId, targetShelf) {
        let found = null;
        ['want', 'reading', 'finished'].forEach(s => {
            const idx = state.bookshelf[s].findIndex(b => b.id === bookId);
            if (idx !== -1) {
                found = state.bookshelf[s].splice(idx, 1)[0];
            }
        });
        if (found) {
            state.bookshelf[targetShelf].unshift(found);
            saveBookshelf();
            renderBookshelf();
        }
    }

    function saveBookshelf() {
        localStorage.setItem('pagesage_bookshelf', JSON.stringify(state.bookshelf));
    }

    function renderBookshelf() {
        wantCount.textContent = state.bookshelf.want.length;
        readingCount.textContent = state.bookshelf.reading.length;
        finishedCount.textContent = state.bookshelf.finished.length;

        bookshelfList.innerHTML = '';
        const currentList = state.bookshelf[state.activeShelfTab] || [];

        if (currentList.length === 0) {
            const empty = document.createElement('div');
            empty.className = 'empty-shelf-notice';
            empty.innerHTML = `No books in your <strong>${state.activeShelfTab}</strong> shelf yet. Tap "+ Add" on recommendations to save books here!`;
            bookshelfList.appendChild(empty);
            return;
        }

        currentList.forEach(book => {
            const item = document.createElement('div');
            item.className = 'shelf-item';

            const cover = document.createElement('img');
            cover.className = 'shelf-item-cover';
            cover.src = book.cover_url || 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?auto=format&fit=crop&q=80&w=120';
            cover.alt = book.title;

            const info = document.createElement('div');
            info.className = 'shelf-item-info';
            info.innerHTML = `
                <div class="shelf-item-title" title="${book.title}">${book.title}</div>
                <div class="shelf-item-author">${book.author}</div>
            `;
            info.style.cursor = 'pointer';
            info.onclick = () => openBookModal(book);

            const actions = document.createElement('div');
            actions.className = 'shelf-item-actions';

            // Shelf cycler
            const cycleBtn = document.createElement('button');
            cycleBtn.className = 'shelf-action-btn';
            cycleBtn.title = 'Move shelf';
            cycleBtn.innerHTML = '<i data-lucide="arrow-right-left" style="width: 14px; height: 14px;"></i>';
            cycleBtn.onclick = (e) => {
                e.stopPropagation();
                const nextShelf = state.activeShelfTab === 'want' ? 'reading' : (state.activeShelfTab === 'reading' ? 'finished' : 'want');
                moveBookshelfItem(book.id, nextShelf);
            };

            const delBtn = document.createElement('button');
            delBtn.className = 'shelf-action-btn';
            delBtn.title = 'Remove';
            delBtn.innerHTML = '<i data-lucide="trash-2" style="width: 14px; height: 14px;"></i>';
            delBtn.onclick = (e) => {
                e.stopPropagation();
                removeFromBookshelf(book.id);
            };

            actions.appendChild(cycleBtn);
            actions.appendChild(delBtn);

            item.appendChild(cover);
            item.appendChild(info);
            item.appendChild(actions);

            bookshelfList.appendChild(item);
        });

        refreshIcons();
    }

    function exportBookshelfToMarkdown() {
        let md = `# 📚 My PageSage Literary Bookshelf\n*Exported on ${new Date().toLocaleDateString()}*\n\n`;
        
        ['want', 'reading', 'finished'].forEach(shelf => {
            const title = shelf === 'want' ? 'Want to Read' : (shelf === 'reading' ? 'Currently Reading' : 'Finished Reading');
            md += `## ${title} (${state.bookshelf[shelf].length})\n`;
            if (state.bookshelf[shelf].length === 0) {
                md += `*None*\n\n`;
            } else {
                state.bookshelf[shelf].forEach(b => {
                    md += `- **${b.title}** by ${b.author} (${b.year || 'N/A'}) - ⭐ ${b.rating || '4.5'}/5.0\n`;
                });
                md += `\n`;
            }
        });

        const blob = new Blob([md], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `my-reading-bookshelf-${new Date().toISOString().slice(0,10)}.md`;
        a.click();
        URL.revokeObjectURL(url);
    }

    // ==========================================
    // Book Details Modal
    // ==========================================
    function openBookModal(book) {
        bookModalTitle.textContent = book.title;
        
        let questionsHtml = '';
        if (book.discussion_questions && book.discussion_questions.length > 0) {
            questionsHtml = `
                <div style="margin-top: 1rem;">
                    <h4 style="font-family: var(--font-serif); margin-bottom: 0.5rem; color: var(--accent);">👥 Discussion Questions:</h4>
                    <ol style="margin-left: 1.25rem; font-size: 0.85rem; color: var(--text-secondary);">
                        ${book.discussion_questions.map(q => `<li style="margin-bottom: 0.25rem;">${q}</li>`).join('')}
                    </ol>
                </div>
            `;
        }

        let readAlikesHtml = '';
        if (book.read_alikes && book.read_alikes.length > 0) {
            readAlikesHtml = `
                <div style="margin-top: 1rem;">
                    <h4 style="font-family: var(--font-serif); margin-bottom: 0.5rem; color: var(--accent);">🔍 If You Liked This:</h4>
                    <p style="font-size: 0.85rem; color: var(--text-secondary);">${book.read_alikes.join(' • ')}</p>
                </div>
            `;
        }

        bookModalContent.innerHTML = `
            <div style="display: flex; gap: 1.25rem; align-items: flex-start;">
                <img src="${book.cover_url || 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?auto=format&fit=crop&q=80&w=120'}" 
                     style="width: 100px; height: 150px; border-radius: 8px; object-fit: cover; box-shadow: var(--shadow-md);">
                <div>
                    <h3 style="font-family: var(--font-serif); font-size: 1.2rem; color: var(--text-primary);">${book.title}</h3>
                    <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 0.5rem;">by <strong>${book.author}</strong> (${book.year || 'N/A'})</p>
                    <p style="font-size: 0.85rem; color: var(--accent); margin-bottom: 0.75rem;">⭐ ${book.rating || '4.5'}/5.0 | ${book.genre || 'Literature'}</p>
                    <div style="display: flex; gap: 0.5rem;">
                        <button class="primary-btn" id="modalAddWantBtn" style="font-size: 0.75rem; padding: 0.4rem 0.8rem;">+ Want to Read</button>
                        <button class="secondary-btn" id="modalAskAI" style="font-size: 0.75rem; padding: 0.4rem 0.8rem;">✨ Ask PageSage</button>
                    </div>
                </div>
            </div>
            
            <div style="margin-top: 1.25rem; font-size: 0.9rem; line-height: 1.6; color: var(--text-primary);">
                <h4 style="font-family: var(--font-serif); margin-bottom: 0.35rem; color: var(--accent);">Overview</h4>
                <p>${book.description || 'A remarkable work of literature with rich themes and compelling character arcs.'}</p>
            </div>

            ${questionsHtml}
            ${readAlikesHtml}
        `;

        bookModal.classList.add('active');

        // Modal Action listeners
        document.getElementById('modalAddWantBtn').onclick = () => {
            addToBookshelf(book, 'want');
            bookModal.classList.remove('active');
        };

        document.getElementById('modalAskAI').onclick = () => {
            bookModal.classList.remove('active');
            sendMessage(`Tell me more about "${book.title}" by ${book.author}, including its themes, tone, and who would enjoy it.`);
        };
    }

    // ==========================================
    // Event Listeners Setup
    // ==========================================
    function setupEventListeners() {
        // Chat Form Submit
        chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            sendMessage();
        });

        // Input Keyboard shortcuts
        messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        // Auto-expand textarea
        messageInput.addEventListener('input', () => {
            messageInput.style.height = 'auto';
            messageInput.style.height = `${Math.min(messageInput.scrollHeight, 160)}px`;
        });

        // Spoiler Shield Toggles
        spoilerShieldToggle.addEventListener('change', (e) => {
            setSpoilerShield(e.target.checked);
        });

        inputSpoilerBtn.addEventListener('click', () => {
            setSpoilerShield(!state.spoilerShield);
        });

        // Theme Toggle
        themeToggleBtn.addEventListener('click', toggleTheme);

        // Sidebar Toggles
        toggleSidebarBtn.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
        });

        closeSidebarBtn.addEventListener('click', () => {
            sidebar.classList.add('collapsed');
        });

        newChatBtn.addEventListener('click', () => {
            state.conversation = [];
            messagesList.innerHTML = '';
            if (welcomeScreen) welcomeScreen.style.display = 'block';
            headerStatusText.textContent = 'New literary session started';
        });

        // Bookshelf Tabs
        document.querySelectorAll('.shelf-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                document.querySelectorAll('.shelf-tab').forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                state.activeShelfTab = tab.dataset.tab;
                renderBookshelf();
            });
        });

        exportBookshelfBtn.addEventListener('click', exportBookshelfToMarkdown);

        // Quick Prompt Chips (Sidebar & Welcome Screen)
        document.querySelectorAll('.prompt-chip, .starter-card').forEach(card => {
            card.addEventListener('click', () => {
                const prompt = card.dataset.prompt;
                if (prompt) {
                    sendMessage(prompt);
                }
            });
        });

        // Settings Modal
        openSettingsBtn.addEventListener('click', () => {
            settingsModal.classList.add('active');
        });

        closeSettingsModalBtn.addEventListener('click', () => {
            settingsModal.classList.remove('active');
        });

        settingsModal.addEventListener('click', (e) => {
            if (e.target === settingsModal) {
                settingsModal.classList.remove('active');
            }
        });

        toggleApiKeyVisibility.addEventListener('click', () => {
            const isPassword = geminiApiKeyInput.type === 'password';
            geminiApiKeyInput.type = isPassword ? 'text' : 'password';
            apiKeyEyeIcon.setAttribute('data-lucide', isPassword ? 'eye-off' : 'eye');
            refreshIcons();
        });

        // Genre pill selector
        genreChipsSelector.querySelectorAll('.genre-pill').forEach(pill => {
            pill.addEventListener('click', () => {
                pill.classList.toggle('selected');
            });
        });

        saveSettingsBtn.addEventListener('click', () => {
            state.apiKey = geminiApiKeyInput.value.trim();
            localStorage.setItem('pagesage_gemini_key', state.apiKey);

            const selectedGenres = Array.from(genreChipsSelector.querySelectorAll('.genre-pill.selected'))
                .map(p => p.dataset.genre);
            state.preferences.genres = selectedGenres;
            state.preferences.authors = favAuthorsInput.value.trim();
            localStorage.setItem('pagesage_preferences', JSON.stringify(state.preferences));

            initEngineBadge();
            settingsModal.classList.remove('active');
        });

        resetSettingsBtn.addEventListener('click', () => {
            geminiApiKeyInput.value = '';
            favAuthorsInput.value = '';
            genreChipsSelector.querySelectorAll('.genre-pill').forEach(p => p.classList.remove('selected'));
        });

        // Book Modal Close
        closeBookModalBtn.addEventListener('click', () => {
            bookModal.classList.remove('active');
        });

        bookModal.addEventListener('click', (e) => {
            if (e.target === bookModal) {
                bookModal.classList.remove('active');
            }
        });
    }
});
