# -*- coding: utf-8 -*-
"""
Brawlhalla Arabic Localization Studio (استوديو تعريب براول هالا)
An interactive local web tool to easily view, search, translate, and install all Brawlhalla texts.
Zero third-party pip dependencies required.
"""

import os
import sys
import json
import zlib
import struct
import time
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Set UTF-8 stdout
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GAME_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
sys.path.insert(0, SCRIPT_DIR)

from translation_rules import translate_string, MASTER_KEY_MAP
from build_arabic_language import build_arabic_database

ORIGINAL_BIN = os.path.join(GAME_DIR, 'languages', 'language.1.bin.original_backup')
if not os.path.exists(ORIGINAL_BIN):
    ORIGINAL_BIN = os.path.join(GAME_DIR, 'languages', 'language.1.bin')

USER_TRANS_FILE = os.path.join(SCRIPT_DIR, 'user_translations.json')

# In-memory storage
ALL_ENTRIES = [] # list of dicts: { id, key, orig, arabic, category, is_custom }
KEY_INDEX = {}
USER_CUSTOM = {}

def get_category(key):
    k = key.lower()
    if k.startswith('ui_') or k.startswith('lsm_') or k.startswith('tutorial_'):
        return 'ui'
    elif k.startswith('questtype_') or k.startswith('missiontype_') or k.startswith('guildmission_') or k.startswith('lesson'):
        return 'missions'
    elif any(k.startswith(p) for p in [
        'store', 'costume', 'weaponskin', 'avatar', 'color_', 'colorscheme', 'podium', 'skin_',
        'entitlement', 'taunt', 'moniker', 'emoji', 'spawnbot', 'promo', 'tile', 'traileffect', 'generated'
    ]):
        return 'store'
    elif k.startswith('herotype_'):
        return 'lore'
    elif any(k.startswith(p) for p in ['gamemode', 'playlist', 'levelset', 'scoring']):
        return 'modes'
    elif any(k.startswith(p) for p in ['helpfulhint', 'error_', 'cutscene_', 'itemtype_']):
        return 'settings'
    return 'other'

def load_data():
    global ALL_ENTRIES, KEY_INDEX, USER_CUSTOM
    print("Loading language data into memory...")
    if os.path.exists(USER_TRANS_FILE):
        try:
            with open(USER_TRANS_FILE, 'r', encoding='utf-8') as f:
                USER_CUSTOM = json.load(f)
        except Exception:
            USER_CUSTOM = {}
    else:
        USER_CUSTOM = {}

    with open(ORIGINAL_BIN, 'rb') as f:
        raw = zlib.decompress(f.read()[4:])
    count = struct.unpack('>I', raw[:4])[0]
    idx = 4
    ALL_ENTRIES = []
    KEY_INDEX = {}

    for i in range(count):
        klen = struct.unpack('>H', raw[idx:idx+2])[0]; idx += 2
        key = raw[idx:idx+klen].decode('utf-8', errors='replace'); idx += klen
        vlen = struct.unpack('>H', raw[idx:idx+2])[0]; idx += 2
        val = raw[idx:idx+vlen].decode('utf-8', errors='replace'); idx += vlen

        is_custom = key in USER_CUSTOM
        if is_custom:
            ar_val = USER_CUSTOM[key]
        else:
            ar_val = translate_string(val, key)

        has_ar = any('\u0600' <= c <= '\u06ff' for c in ar_val)
        if val == "":
            display_ar = ""
            is_done = True
        else:
            is_done = (has_ar or (key in MASTER_KEY_MAP and ar_val != ""))
            display_ar = ar_val if is_done else ""

        entry = {
            "id": i,
            "key": key,
            "orig": val,
            "arabic": display_ar,
            "category": get_category(key),
            "is_custom": is_custom,
            "is_done": is_done
        }
        ALL_ENTRIES.append(entry)
        KEY_INDEX[key] = entry

    print(f"Loaded {len(ALL_ENTRIES)} entries.")

HTML_PAGE = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Brawlhalla Arabic Studio | استوديو تعريب براول هالا</title>
    <style>
        :root {
            --bg-dark: #0a0e17;
            --bg-card: #131a29;
            --bg-card-hover: #1a2336;
            --bg-input: #080c14;
            --primary: #00d2ff;
            --primary-glow: rgba(0, 210, 255, 0.35);
            --accent-gold: #ffb800;
            --accent-gold-glow: rgba(255, 184, 0, 0.4);
            --accent-green: #00e676;
            --text-main: #f0f4f8;
            --text-muted: #8b9bb4;
            --border: #232f45;
            --border-active: #00d2ff;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Cairo, sans-serif; }
        body { background: var(--bg-dark); color: var(--text-main); min-height: 100vh; padding-bottom: 60px; }
        
        /* Top Navigation Header */
        header {
            background: linear-gradient(180deg, #162033 0%, #0d1422 100%);
            border-bottom: 1px solid var(--border);
            padding: 16px 32px;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
        }
        .brand { display: flex; align-items: center; gap: 14px; }
        .brand-icon {
            width: 44px; height: 44px; border-radius: 10px;
            background: linear-gradient(135deg, #00d2ff, #0077ff);
            display: flex; align-items: center; justify-content: center;
            font-size: 22px; font-weight: bold; color: #fff;
            box-shadow: 0 0 15px var(--primary-glow);
        }
        .brand-title h1 { font-size: 20px; font-weight: 800; color: #fff; letter-spacing: 0.5px; }
        .brand-title p { font-size: 12px; color: var(--text-muted); }
        
        .header-actions { display: flex; align-items: center; gap: 14px; }
        .btn-build {
            background: linear-gradient(135deg, #ffb800, #ff8c00);
            color: #000;
            font-weight: 800;
            font-size: 15px;
            padding: 12px 24px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            box-shadow: 0 0 18px var(--accent-gold-glow);
            transition: all 0.2s ease;
            display: flex; align-items: center; gap: 8px;
        }
        .btn-build:hover { transform: translateY(-2px); box-shadow: 0 0 25px rgba(255,184,0,0.7); }
        .btn-build:active { transform: translateY(0); }
        
        /* Main Container */
        .container { max-width: 1400px; margin: 0 auto; padding: 24px 24px; }
        
        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }
        .stat-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 18px 20px;
            display: flex;
            align-items: center;
            gap: 16px;
        }
        .stat-icon {
            width: 48px; height: 48px; border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-size: 24px; background: rgba(255,255,255,0.05);
        }
        .stat-info h3 { font-size: 24px; font-weight: 800; color: #fff; margin-bottom: 2px; }
        .stat-info p { font-size: 13px; color: var(--text-muted); }
        
        /* Filter & Search Toolbar */
        .toolbar {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 18px 20px;
            margin-bottom: 20px;
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
        }
        .search-box {
            flex: 1;
            min-width: 300px;
            position: relative;
        }
        .search-box input {
            width: 100%;
            background: var(--bg-input);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 12px 16px 12px 40px;
            color: #fff;
            font-size: 15px;
            outline: none;
            transition: border 0.2s;
        }
        .search-box input:focus { border-color: var(--primary); box-shadow: 0 0 10px var(--primary-glow); }
        .search-icon { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--text-muted); }
        
        .filter-group { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
        .filter-btn {
            background: var(--bg-input);
            border: 1px solid var(--border);
            color: var(--text-muted);
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }
        .filter-btn:hover { color: #fff; border-color: #3d5075; }
        .filter-btn.active {
            background: rgba(0, 210, 255, 0.15);
            border-color: var(--primary);
            color: var(--primary);
        }
        
        select.cat-select {
            background: var(--bg-input);
            border: 1px solid var(--border);
            color: #fff;
            padding: 9px 16px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 600;
            outline: none;
            cursor: pointer;
        }
        select.cat-select:focus { border-color: var(--primary); }
        
        /* Items List */
        .entries-list { display: flex; flex-direction: column; gap: 12px; margin-bottom: 24px; }
        .entry-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 16px 20px;
            display: grid;
            grid-template-columns: 280px 1fr 1.2fr auto;
            align-items: center;
            gap: 20px;
            transition: border-color 0.2s;
        }
        .entry-card:hover { border-color: #3b4d6d; background: var(--bg-card-hover); }
        
        .entry-key {
            font-family: 'Consolas', monospace;
            font-size: 13px;
            color: #79a8e0;
            word-break: break-all;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        .key-badge {
            display: inline-block;
            font-size: 10px;
            text-transform: uppercase;
            padding: 2px 6px;
            border-radius: 4px;
            background: rgba(255,255,255,0.06);
            color: var(--text-muted);
            width: fit-content;
        }
        
        .entry-orig {
            color: #c5d1e0;
            font-size: 14px;
            line-height: 1.4;
            background: rgba(0,0,0,0.25);
            padding: 10px 12px;
            border-radius: 6px;
            border: 1px solid rgba(255,255,255,0.03);
            word-break: break-word;
        }
        
        .entry-edit { display: flex; flex-direction: column; gap: 4px; position: relative; }
        .arabic-input {
            width: 100%;
            background: var(--bg-input);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 10px 14px;
            color: #fff;
            font-size: 15px;
            outline: none;
            direction: rtl;
            transition: border 0.2s;
        }
        .arabic-input:focus { border-color: var(--primary); box-shadow: 0 0 10px var(--primary-glow); }
        
        .char-counter {
            font-size: 11px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 4px;
            align-self: flex-start;
        }
        .char-safe { color: var(--accent-green); }
        .char-mid { color: var(--accent-gold); }
        .char-long { color: #ff5252; }
        
        .entry-actions { display: flex; align-items: center; gap: 8px; }
        .btn-save {
            background: #00d2ff;
            color: #000;
            font-weight: 700;
            font-size: 13px;
            padding: 9px 18px;
            border-radius: 6px;
            border: none;
            cursor: pointer;
            transition: all 0.2s;
            white-space: nowrap;
        }
        .btn-save:hover { background: #38e1ff; transform: scale(1.03); }
        .btn-save.saved { background: var(--accent-green); color: #000; }
        
        /* Pagination */
        .pagination {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            margin-top: 20px;
        }
        .page-btn {
            background: var(--bg-card);
            border: 1px solid var(--border);
            color: #fff;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s;
        }
        .page-btn:hover:not(:disabled) { border-color: var(--primary); color: var(--primary); }
        .page-btn:disabled { opacity: 0.3; cursor: not-allowed; }
        .page-info { font-size: 14px; color: var(--text-muted); }
        
        /* Modal Notification */
        .modal-overlay {
            position: fixed; inset: 0; background: rgba(0,0,0,0.8);
            display: none; align-items: center; justify-content: center; z-index: 1000;
        }
        .modal {
            background: var(--bg-card);
            border: 1px solid var(--accent-gold);
            box-shadow: 0 0 40px var(--accent-gold-glow);
            border-radius: 16px; padding: 32px; max-width: 500px; text-align: center;
        }
        .modal-icon { font-size: 48px; margin-bottom: 16px; }
        .modal h2 { font-size: 22px; color: #fff; margin-bottom: 10px; }
        .modal p { color: var(--text-muted); font-size: 14px; line-height: 1.5; margin-bottom: 24px; }
        .modal-btn {
            background: var(--accent-gold); color: #000; font-weight: 800; font-size: 15px;
            padding: 10px 30px; border-radius: 8px; border: none; cursor: pointer;
        }
        
        /* Loading spinner */
        .spinner {
            border: 3px solid rgba(255,255,255,0.1);
            border-top: 3px solid var(--accent-gold);
            border-radius: 50%; width: 20px; height: 20px;
            animation: spin 0.8s linear infinite; display: inline-block;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

        @media (max-width: 1024px) {
            .entry-card { grid-template-columns: 1fr; gap: 12px; }
            .entry-actions { justify-content: flex-end; }
        }
    </style>
</head>
<body>

    <header>
        <div class="brand">
            <div class="brand-icon">B</div>
            <div class="brand-title">
                <h1>Brawlhalla Arabic Studio</h1>
                <p>محرر واستوديو تعريب براول هالا التفاعلي</p>
            </div>
        </div>
        <div class="header-actions">
            <button class="btn-build" id="buildBtn" onclick="buildAndInstall()">
                <span>🚀 تطبيق التعريب في اللعبة فوراً</span>
            </button>
        </div>
    </header>

    <div class="container">
        <!-- Stats -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">📚</div>
                <div class="stat-info">
                    <h3 id="statTotal">--</h3>
                    <p>إجمالي نصوص اللعبة</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon" style="color: var(--accent-green);">✓</div>
                <div class="stat-info">
                    <h3 id="statTranslated" style="color: var(--accent-green);">--</h3>
                    <p>النصوص المعربة حالياً</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon" style="color: #ff5252;">⏳</div>
                <div class="stat-info">
                    <h3 id="statUntranslated" style="color: #ff5252;">--</h3>
                    <p>نصوص بانتظار التعريب</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon" style="color: var(--accent-gold);">🎯</div>
                <div class="stat-info">
                    <h3 id="statPercent" style="color: var(--accent-gold);">--%</h3>
                    <p>نسبة اكتمال التعريب</p>
                </div>
            </div>
        </div>

        <!-- Toolbar -->
        <div class="toolbar">
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="ابحث بالإنجليزية أو اسم المفتاح (Key)..." oninput="onSearchChange()">
                <span class="search-icon">🔍</span>
            </div>
            <div class="filter-group">
                <button class="filter-btn active" data-status="all" onclick="setFilter('status', 'all')">الكل</button>
                <button class="filter-btn" data-status="untranslated" onclick="setFilter('status', 'untranslated')">غير معرب</button>
                <button class="filter-btn" data-status="translated" onclick="setFilter('status', 'translated')">معرب</button>
                <button class="filter-btn" data-status="custom" onclick="setFilter('status', 'custom')">تعديلاتي الخاصة ✍️</button>
                
                <select class="cat-select" id="catSelect" onchange="setFilter('category', this.value)">
                    <option value="all">كل الأقسام</option>
                    <option value="ui">القوائم والواجهة (UI)</option>
                    <option value="missions">المهمات والتحديات</option>
                    <option value="store">المتجر والمظاهر والألقاب</option>
                    <option value="lore">الأساطير والقصص</option>
                    <option value="modes">أنماط اللعب والخرائط</option>
                    <option value="settings">التعليمات والإعدادات</option>
                    <option value="other">متنوع</option>
                </select>
            </div>
        </div>

        <!-- Entries List -->
        <div class="entries-list" id="entriesList">
            <!-- Dynamic Cards -->
        </div>

        <!-- Pagination -->
        <div class="pagination">
            <button class="page-btn" id="prevBtn" onclick="changePage(-1)">السابق</button>
            <span class="page-info" id="pageInfo">صفحة 1 من 1</span>
            <button class="page-btn" id="nextBtn" onclick="changePage(1)">التالي</button>
        </div>
    </div>

    <!-- Success Modal -->
    <div class="modal-overlay" id="modalOverlay">
        <div class="modal">
            <div class="modal-icon">🎉</div>
            <h2 id="modalTitle">تم تطبيق التعريب بنجاح!</h2>
            <p id="modalDesc">تم إنشاء ملف اللغة المعرب وتثبيته مباشرة في مجلد لعبة Brawlhalla.<br>يمكنك الآن فتح اللعبة للاستمتاع بتعديلاتك فوراً!</p>
            <button class="modal-btn" onclick="closeModal()">ممتاز، حسناً</button>
        </div>
    </div>

    <script>
        let currentStatus = 'all';
        let currentCategory = 'all';
        let currentSearch = '';
        let currentPage = 1;
        let totalPages = 1;
        let searchTimeout = null;

        const catNames = {
            'ui': 'القوائم والواجهة',
            'missions': 'المهمات والتحديات',
            'store': 'المتجر والمظاهر',
            'lore': 'الأساطير والقصص',
            'modes': 'أنماط اللعب',
            'settings': 'الإعدادات والتعليمات',
            'other': 'متنوع'
        };

        async function fetchStats() {
            try {
                const res = await fetch('/api/stats');
                const data = await res.json();
                document.getElementById('statTotal').innerText = data.total.toLocaleString();
                document.getElementById('statTranslated').innerText = data.translated.toLocaleString();
                document.getElementById('statUntranslated').innerText = data.untranslated.toLocaleString();
                document.getElementById('statPercent').innerText = data.percent + '%';
            } catch (err) {
                console.error(err);
            }
        }

        async function fetchEntries() {
            const listEl = document.getElementById('entriesList');
            listEl.innerHTML = '<div style="text-align: center; padding: 40px; color: var(--text-muted);"><div class="spinner"></div><p style="margin-top: 10px;">جارٍ تحميل النصوص...</p></div>';

            const query = new URLSearchParams({
                search: currentSearch,
                status: currentStatus,
                category: currentCategory,
                page: currentPage,
                limit: 40
            });

            try {
                const res = await fetch('/api/strings?' + query.toString());
                const data = await res.json();
                currentPage = data.page;
                totalPages = data.total_pages || 1;
                document.getElementById('pageInfo').innerText = `صفحة ${currentPage} من ${totalPages} (${data.total_matches.toLocaleString()} نصاً)`;
                document.getElementById('prevBtn').disabled = currentPage <= 1;
                document.getElementById('nextBtn').disabled = currentPage >= totalPages;

                if (data.items.length === 0) {
                    listEl.innerHTML = '<div style="text-align: center; padding: 60px; color: var(--text-muted);"><p style="font-size: 18px;">لم يتم العثور على أي نصوص تطابق البحث الحالي.</p></div>';
                    return;
                }

                listEl.innerHTML = '';
                data.items.forEach(item => {
                    const card = createEntryCard(item);
                    listEl.appendChild(card);
                });
            } catch (err) {
                listEl.innerHTML = '<div style="text-align: center; padding: 40px; color: #ff5252;">حدث خطأ أثناء تحميل البيانات.</div>';
            }
        }

        function createEntryCard(item) {
            const div = document.createElement('div');
            div.className = 'entry-card';
            div.id = 'card-' + item.key;

            const charCount = item.arabic.length;
            const counterClass = charCount <= 22 ? 'char-safe' : (charCount <= 45 ? 'char-mid' : 'char-long');
            const counterText = charCount <= 22 ? 'آمن (سطر واحد)' : (charCount <= 45 ? 'طول متوسط' : 'طويل (قد يلتف)');

            const catLabel = catNames[item.category] || 'عام';

            div.innerHTML = `
                <div class="entry-key">
                    <span class="key-badge">${catLabel}</span>
                    <span title="${item.key}">${item.key}</span>
                </div>
                <div class="entry-orig" title="النص الإنجليزي">${escapeHtml(item.orig)}</div>
                <div class="entry-edit">
                    <input type="text" class="arabic-input" id="input-${item.id}" value="${escapeHtml(item.arabic)}" 
                           placeholder="اكتب التعريب العربي هنا..." oninput="onInputCharChange(${item.id})"
                           onkeydown="if(event.key === 'Enter') saveItem('${item.key}', ${item.id})">
                    <div class="char-counter ${counterClass}" id="counter-${item.id}">
                        <span>${charCount} حرفاً</span> • <span>${counterText}</span>
                    </div>
                </div>
                <div class="entry-actions">
                    <button class="btn-save" id="btn-save-${item.id}" onclick="saveItem('${item.key}', ${item.id})">حفظ</button>
                </div>
            `;
            return div;
        }

        function onInputCharChange(id) {
            const input = document.getElementById('input-' + id);
            const counter = document.getElementById('counter-' + id);
            const len = input.value.length;
            const cClass = len <= 22 ? 'char-safe' : (len <= 45 ? 'char-mid' : 'char-long');
            const cText = len <= 22 ? 'آمن (سطر واحد)' : (len <= 45 ? 'طول متوسط' : 'طويل (قد يلتف)');
            counter.className = 'char-counter ' + cClass;
            counter.innerHTML = `<span>${len} حرفاً</span> • <span>${cText}</span>`;
        }

        async function saveItem(key, id) {
            const input = document.getElementById('input-' + id);
            const btn = document.getElementById('btn-save-' + id);
            const val = input.value.trim();

            btn.innerText = 'جارٍ الحفظ...';
            try {
                const res = await fetch('/api/save', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ key: key, arabic: val })
                });
                const data = await res.json();
                if (data.success) {
                    btn.innerText = '✓ تم الحفظ';
                    btn.classList.add('saved');
                    setTimeout(() => {
                        btn.innerText = 'حفظ';
                        btn.classList.remove('saved');
                    }, 1500);
                    fetchStats();
                }
            } catch (err) {
                btn.innerText = 'خطأ!';
            }
        }

        async function buildAndInstall() {
            const btn = document.getElementById('buildBtn');
            btn.disabled = true;
            btn.innerHTML = '<span class="spinner"></span> <span>جارٍ البناء والتثبيت...</span>';

            try {
                const res = await fetch('/api/build', { method: 'POST' });
                const data = await res.json();
                if (data.success) {
                    document.getElementById('modalTitle').innerText = 'تم تثبيت التعريب في اللعبة بنجاح! 🚀';
                    document.getElementById('modalDesc').innerHTML = `
                        تم تجهيز <b>${data.arabic_count.toLocaleString()}</b> مدخلاً عربياً، وتم تحديث ملف اللغة في مجلد اللعبة مباشرة.<br>
                        حجم الملف: <b>${(data.bytes / 1024).toFixed(1)} KB</b>.<br><br>
                        يمكنك الآن فتح Brawlhalla والاستمتاع بكلماتك المعربة فوراً!
                    `;
                    document.getElementById('modalOverlay').style.display = 'flex';
                } else {
                    alert('حدث خطأ أثناء البناء: ' + (data.error || 'غير معروف'));
                }
            } catch (err) {
                alert('فشل الاتصال بالخادم.');
            } finally {
                btn.disabled = false;
                btn.innerHTML = '<span>🚀 تطبيق التعريب في اللعبة فوراً</span>';
            }
        }

        function closeModal() {
            document.getElementById('modalOverlay').style.display = 'none';
        }

        function onSearchChange() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                currentSearch = document.getElementById('searchInput').value.trim();
                currentPage = 1;
                fetchEntries();
            }, 300);
        }

        function setFilter(type, value) {
            if (type === 'status') {
                currentStatus = value;
                document.querySelectorAll('.filter-btn').forEach(b => {
                    b.classList.toggle('active', b.dataset.status === value);
                });
            } else if (type === 'category') {
                currentCategory = value;
            }
            currentPage = 1;
            fetchEntries();
        }

        function changePage(delta) {
            currentPage += delta;
            fetchEntries();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        function escapeHtml(text) {
            if (!text) return '';
            return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
        }

        // Initial Load
        fetchStats();
        fetchEntries();
    </script>
</body>
</html>
"""

class StudioHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Silent logger for clean console
        pass

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == '/' or path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))

        elif path == '/api/stats':
            total = len(ALL_ENTRIES)
            translated = sum(1 for e in ALL_ENTRIES if e.get('is_done', False) or e['arabic'])
            untranslated = total - translated
            custom_count = len(USER_CUSTOM)
            pct = 100.0 if untranslated == 0 else round((translated / total) * 100, 1)
            
            resp = {
                "total": total,
                "translated": translated,
                "untranslated": untranslated,
                "custom_count": custom_count,
                "percent": pct
            }
            self.send_json(resp)

        elif path == '/api/strings':
            params = parse_qs(parsed.query)
            search = params.get('search', [''])[0].strip().lower()
            status = params.get('status', ['all'])[0]
            cat = params.get('category', ['all'])[0]
            page = int(params.get('page', [1])[0])
            limit = int(params.get('limit', [50])[0])

            filtered = ALL_ENTRIES

            # Status filter
            if status == 'translated':
                filtered = [e for e in filtered if e['arabic']]
            elif status == 'untranslated':
                filtered = [e for e in filtered if not e['arabic']]
            elif status == 'custom':
                filtered = [e for e in filtered if e['is_custom']]

            # Category filter
            if cat != 'all':
                filtered = [e for e in filtered if e['category'] == cat]

            # Search filter
            if search:
                filtered = [
                    e for e in filtered
                    if search in e['key'].lower() or search in e['orig'].lower() or search in e['arabic'].lower()
                ]

            total_matches = len(filtered)
            total_pages = max(1, (total_matches + limit - 1) // limit)
            page = min(max(1, page), total_pages)
            start = (page - 1) * limit
            items = filtered[start:start+limit]

            resp = {
                "items": items,
                "total_matches": total_matches,
                "page": page,
                "total_pages": total_pages
            }
            self.send_json(resp)

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == '/api/save':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode('utf-8')
            try:
                data = json.loads(body)
                key = data.get('key')
                ar_text = data.get('arabic', '').strip()

                if key in KEY_INDEX:
                    USER_CUSTOM[key] = ar_text
                    # Save user_translations.json
                    with open(USER_TRANS_FILE, 'w', encoding='utf-8') as f:
                        json.dump(USER_CUSTOM, f, ensure_ascii=False, indent=2)

                    # Update in-memory entry
                    entry = KEY_INDEX[key]
                    entry['arabic'] = ar_text
                    entry['is_custom'] = True
                    MASTER_KEY_MAP[key] = ar_text

                self.send_json({"success": True})
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)

        elif path == '/api/build':
            try:
                out_bin = os.path.join(SCRIPT_DIR, 'language.1.arabic.bin')
                game_target = os.path.join(GAME_DIR, 'languages', 'language.1.bin')
                
                print("[Studio] Building Arabic database...")
                build_arabic_database(ORIGINAL_BIN, out_bin)

                import shutil
                shutil.copy2(out_bin, game_target)
                bytes_size = os.path.getsize(game_target)

                # Count Arabic entries
                ar_count = sum(1 for e in ALL_ENTRIES if e['arabic'])

                self.send_json({
                    "success": True,
                    "bytes": bytes_size,
                    "arabic_count": ar_count
                })
            except Exception as e:
                print(f"[Studio Build Error]: {e}")
                self.send_json({"success": False, "error": str(e)}, status=500)
        else:
            self.send_response(404)
            self.end_headers()

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

def run_server(port=8085):
    load_data()
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, StudioHandler)
    url = f"http://127.0.0.1:{port}"
    print("=" * 65)
    print("  استوديو تعريب براول هالا جاهز ويعمل الآن!")
    print(f"  افتح المتصفح على: {url}")
    print("=" * 65)
    try:
        webbrowser.open(url)
    except Exception:
        pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nتم إيقاف الاستوديو.")

if __name__ == '__main__':
    port = 8085
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    run_server(port)
