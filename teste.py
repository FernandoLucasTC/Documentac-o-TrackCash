import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="Documentação · Canais Marketplace",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    :root {
        --bg: #0f0f18; --surface: #16161f; --card: #1c1c28;
        --border: #252535; --text: #dde1f0; --muted: #6868a0;
        --accent: #E85D04; --accent-dim: rgba(232,93,4,0.13);
        --green: #22c55e; --amber: #f59e0b; --red: #ef4444;
    }
    body, [data-testid="stAppViewContainer"] { background: var(--bg) !important; color: var(--text); }
    [data-testid="stMainBlockContainer"] { padding: 36px 28px 60px; }

    .app-header { display:flex; align-items:center; gap:16px; margin-bottom:32px; padding-bottom:24px; border-bottom:1px solid var(--border); }
    .logo-icon { width:46px; height:46px; flex-shrink:0; background:linear-gradient(135deg,#E85D04 0%,#ff6b35 100%); border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:22px; color:#fff; box-shadow:0 4px 20px rgba(232,93,4,0.35); }
    .main-title { font-size:24px; font-weight:700; color:#f0f0ff; letter-spacing:-0.4px; }
    .subtitle { font-size:11px; color:var(--muted); margin-top:3px; letter-spacing:0.13em; text-transform:uppercase; }

    .stat-card { background:var(--card); border:1px solid var(--border); border-radius:10px; padding:16px; text-align:center; }
    .stat-value { font-size:28px; font-weight:800; color:var(--accent); line-height:1; margin-bottom:6px; }
    .stat-label { font-size:11px; color:var(--muted); text-transform:uppercase; letter-spacing:0.08em; }

    .progress-section { background:var(--surface); border:1px solid var(--border); border-radius:10px; padding:18px 22px; margin:22px 0 28px; }
    .progress-label { font-size:13px; color:#b0b0d0; margin-bottom:12px; font-weight:500; display:flex; justify-content:space-between; }
    .progress-label span:last-child { color:var(--accent); font-weight:700; }
    .progress-bar-wrap { height:7px; background:var(--border); border-radius:99px; overflow:hidden; }
    .progress-bar-fill { height:100%; background:linear-gradient(90deg,#E85D04 0%,#ff8c42 100%); border-radius:99px; box-shadow:0 0 10px rgba(232,93,4,0.45); }

    .cat-progress-wrap { background:var(--surface); border:1px solid var(--border); border-radius:10px; padding:14px 18px; margin-bottom:24px; display:flex; align-items:center; gap:18px; }
    .cat-progress-text { font-size:12px; color:var(--muted); white-space:nowrap; }
    .cat-progress-bar-wrap { flex:1; height:5px; background:var(--border); border-radius:99px; overflow:hidden; }
    .cat-progress-bar-fill { height:100%; background:linear-gradient(90deg,#E85D04,#ff8c42); border-radius:99px; }
    .cat-progress-pct { font-size:13px; font-weight:700; color:var(--accent); white-space:nowrap; }

    .counter-badge { text-align:center; padding:0 14px; color:var(--accent); font-weight:700; font-size:14px; background:var(--surface); border:1px solid var(--border); border-radius:8px; display:flex; align-items:center; white-space:nowrap; min-width:64px; justify-content:center; }
    .counter-badge.done { color:var(--green); border-color:rgba(34,197,94,0.3); background:rgba(34,197,94,0.06); }

    .expanded-card { background:var(--surface); border:1px solid var(--border); border-left:3px solid var(--accent); border-radius:10px; padding:18px 22px; margin-bottom:10px; }
    .section-title { font-size:10px; font-weight:700; color:var(--accent); text-transform:uppercase; letter-spacing:0.14em; margin-top:18px; margin-bottom:8px; display:flex; align-items:center; gap:8px; }
    .section-title:first-child { margin-top:0; }
    .section-title::before { content:''; width:3px; height:12px; background:var(--accent); border-radius:2px; }

    [data-testid="stCheckbox"] { background:var(--card); border:1px solid var(--border); border-radius:6px; padding:8px 12px !important; margin-bottom:5px !important; transition:all 0.15s; }
    [data-testid="stCheckbox"]:hover { border-color:rgba(232,93,4,0.4); background:rgba(232,93,4,0.04); }
    [data-testid="stCheckbox"] label { font-size:13px !important; color:#c8c8e8 !important; font-weight:400 !important; }
    [data-testid="stCheckbox"]:has(input:checked) { background:rgba(34,197,94,0.06); border-color:rgba(34,197,94,0.28); }
    [data-testid="stCheckbox"]:has(input:checked) label { color:#86efac !important; }

    [data-testid="stButton"] > button { background:var(--card) !important; border:1px solid var(--border) !important; color:#c8c8e8 !important; font-size:14px !important; font-weight:500 !important; border-radius:8px !important; padding:10px 16px !important; transition:all 0.18s !important; }
    [data-testid="stButton"] > button:hover { border-color:var(--accent) !important; color:var(--accent) !important; background:var(--accent-dim) !important; }

    [data-testid="stTextInput"] input { background:var(--card) !important; border:1px solid var(--border) !important; color:var(--text) !important; border-radius:8px !important; }
    [data-testid="stTextInput"] input:focus { border-color:var(--accent) !important; }

    [data-testid="stExpander"] { background:var(--surface) !important; border:1px dashed var(--border) !important; border-radius:10px !important; }
    [data-testid="stExpander"] summary { color:var(--muted) !important; font-size:13px !important; }

    .group-label { display:flex; align-items:center; gap:10px; font-size:11px; letter-spacing:0.15em; text-transform:uppercase; color:var(--muted); margin-bottom:12px; margin-top:28px; padding-bottom:10px; border-bottom:1px solid var(--border); }
    .dot { width:7px; height:7px; border-radius:50%; flex-shrink:0; }
    .dot-red   { background:#ef4444; box-shadow:0 0 7px rgba(239,68,68,0.7); }
    .dot-amber { background:#f59e0b; box-shadow:0 0 7px rgba(245,158,11,0.7); }
    .dot-gray  { background:#555570; }

    .empty-state { text-align:center; padding:60px 20px; color:var(--muted); border:1px dashed var(--border); border-radius:12px; }
    .empty-icon { font-size:40px; margin-bottom:14px; opacity:0.5; }
    .empty-title { font-size:16px; font-weight:600; color:#8080b0; margin-bottom:8px; }
    .empty-sub { font-size:13px; }

    hr { border:none; border-top:1px solid var(--border) !important; margin:32px 0 !important; }
    [data-testid="stDownloadButton"] > button { background:var(--surface) !important; border:1px solid var(--border) !important; color:#c8c8e8 !important; font-size:13px !important; border-radius:8px !important; }
    [data-testid="stDownloadButton"] > button:hover { border-color:var(--green) !important; color:var(--green) !important; }

    /* Remove linha vazia abaixo dos botões de canal */
    [data-testid="stHorizontalBlock"] { gap: 8px; }
</style>
""", unsafe_allow_html=True)

# ─── Conexão Supabase ─────────────────────────────────────────────────────────

@st.cache_resource
def get_supabase():
    try:
        from supabase import create_client
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Erro ao conectar ao Supabase: {e}")
        return None

supabase = get_supabase()

# ─── Persistência via Supabase ────────────────────────────────────────────────

def load_progress():
    if supabase is None:
        return {}
    try:
        res = supabase.table("checklist").select("*").execute()
        progress = {}
        for row in res.data:
            k = f"{row['categoria']}|{row['canal']}|{row['secao']}|{row['item']}"
            progress[k] = row["concluido"]
        return progress
    except Exception as e:
        st.warning(f"Erro ao carregar progresso: {e}")
        return {}

def save_check(cat, channel, section, item, value):
    if supabase is None:
        return
    try:
        supabase.table("checklist").upsert({
            "categoria": cat,
            "canal": channel,
            "secao": section,
            "item": item,
            "concluido": value,
            "updated_at": datetime.now().isoformat()
        }, on_conflict="categoria,canal,secao,item").execute()
    except Exception as e:
        st.warning(f"Erro ao salvar: {e}")

def clear_progress_db():
    if supabase is None:
        return
    try:
        supabase.table("checklist").delete().neq("id", 0).execute()
    except Exception as e:
        st.warning(f"Erro ao limpar progresso: {e}")

def load_structure():
    if supabase is None:
        return None
    try:
        res = supabase.table("estrutura").select("*").eq("id", 1).execute()
        if res.data:
            return json.loads(res.data[0]["data"])
        return None
    except Exception:
        return None

def save_structure(data):
    if supabase is None:
        return
    try:
        supabase.table("estrutura").upsert({
            "id": 1,
            "data": json.dumps(data, ensure_ascii=False),
            "updated_at": datetime.now().isoformat()
        }, on_conflict="id").execute()
    except Exception as e:
        st.warning(f"Erro ao salvar estrutura: {e}")

# ─── Estrutura padrão ─────────────────────────────────────────────────────────

DEFAULT_STRUCTURE = {
    "Ponto B": {
        "channels": {
            "Mercado Livre": {"priority": "alta", "sections": {"Suporte Track": ["API Pedido","API Repasse","Integracao","Validacao","Regras de negocio"], "Cliente": ["Integracao","Configuracao","Regras de negocio"], "Video": ["Local para postar os videos apenas"]}},
            "Omie":          {"priority": "alta", "sections": {"Suporte Track": ["Configuracao","Integracao","Validacao","Regras de negocio"], "Cliente": ["Configuracao","Integracao","Regras de negocio"], "Video": ["Local para postar os videos apenas"]}},
            "Shopee":        {"priority": "alta", "sections": {"Suporte Track": ["Integracao","Configuracao","Regras de negocio"], "Cliente": ["Integracao","Configuracao","Regras de negocio"], "Video": ["Local para postar os videos apenas"]}},
            "Magazine Luiza":{"priority": "alta", "sections": {"Suporte Track": ["Integracao","Configuracao","Regras de negocio","Subir repasse"], "Cliente": ["Integracao","Configuracao","Subir repasse","Regras de negocio"], "Video": ["Local para postar os videos apenas"]}},
            "Amazon":        {"priority": "media","sections": {"Suporte Track": ["Configuracao","Regras de negocio","Subir pedidos","Subir repasse"], "Cliente": ["Subir pedidos","Subir repasse","Configuracao","Regras de negocio"], "Video": ["Local para postar os videos apenas"]}},
            "Via Varejo":    {"priority": "media","sections": {"Suporte Track": ["Integracao","Configuracao","Subir repasse","Regras de negocio"], "Cliente": ["Integracao","Configuracao","Subir repasse","Regras de negocio"], "Video": ["Local para postar os videos apenas"]}},
            "Leroy Merlin":  {"priority": "media","sections": {"Suporte Track": ["Integracao","Configuracao","Regras de negocio","Validacao"], "Cliente": ["Integracao","Configuracao","Regras de negocio"], "Video": ["Local para postar os videos apenas"]}},
            "Carrefour":     {"priority": "media","sections": {"Suporte Track": ["Integracao","Configuracao","Regras de negocio","Validacao"], "Cliente": ["Integracao","Configuracao","Regras de negocio"], "Video": ["Local para postar os videos apenas"]}},
            "Madeira":       {"priority": "baixa","sections": {"Suporte Track": ["Subir pedidos","Subir repasse","Configuracao","Validacao","Regras de negocio"], "Cliente": ["Subir pedidos","Subir repasse","Configuracao","Regras de negocio"], "Video": []}},
            "Netshoes":      {"priority": "baixa","sections": {"Suporte Track": ["Integracao","Configuracao","Validacao","Regras de negocio"], "Cliente": ["Integracao","Configuracao","Regras de negocio"], "Video": ["Local para postar os videos apenas"]}},
            "Tiktok":        {"priority": "baixa","sections": {"Suporte Track": ["Integracao","Configuracao","Validacao","Regras de negocio"], "Cliente": ["Integracao","Configuracao","Regras de negocio"], "Video": ["Local para postar os videos apenas"]}},
            "B2W":           {"priority": "baixa","sections": {"Suporte Track": ["Integracao","Configuracao","Validacao","Regras de negocio"], "Cliente": ["Integracao","Configuracao","Regras de negocio"], "Video": ["Local para postar os videos apenas"]}}
        }
    },
    "Ponto A": {"channels": {}},
    "Meios de Pagamento": {"channels": {}}
}

# ─── Init session state ───────────────────────────────────────────────────────

if "progress" not in st.session_state:
    st.session_state.progress = load_progress()

if "structure" not in st.session_state:
    saved = load_structure()
    st.session_state.structure = saved if saved else DEFAULT_STRUCTURE

if "active_category" not in st.session_state:
    st.session_state.active_category = "Ponto B"

if "expanded_channel" not in st.session_state:
    st.session_state.expanded_channel = {}

# ─── Helpers ──────────────────────────────────────────────────────────────────

CATEGORIES = ["Ponto B", "Ponto A", "Meios de Pagamento"]
CAT_ICONS  = {"Ponto B": "🔵", "Ponto A": "🟠", "Meios de Pagamento": "💳"}
PRIORITY_ORDER = {"alta": 1, "media": 2, "baixa": 3}

def item_key(cat, channel, section, item):
    return f"{cat}|{channel}|{section}|{item}"

def is_done(cat, channel, section, item):
    return st.session_state.progress.get(item_key(cat, channel, section, item), False)

def set_done(cat, channel, section, item, value):
    k = item_key(cat, channel, section, item)
    st.session_state.progress[k] = value
    save_check(cat, channel, section, item, value)

def count_channel(cat, ch_name):
    ch_data = st.session_state.structure[cat]["channels"].get(ch_name, {})
    total = completed = 0
    for sec, items in ch_data.get("sections", {}).items():
        for item in items:
            total += 1
            if is_done(cat, ch_name, sec, item):
                completed += 1
    return completed, total

def count_category(cat):
    total = completed = 0
    for ch in st.session_state.structure[cat]["channels"]:
        c, t = count_channel(cat, ch)
        completed += c; total += t
    return completed, total

def count_all():
    total = completed = 0
    for cat in CATEGORIES:
        c, t = count_category(cat)
        completed += c; total += t
    return completed, total

def persist_structure():
    save_structure(st.session_state.structure)

# ─── Header ───────────────────────────────────────────────────────────────────

st.markdown("""
<div class='app-header'>
    <div class='logo-icon'>&#x25a4;</div>
    <div>
        <div class='main-title'>Documentacao de Canais</div>
        <div class='subtitle'>Marketplace Integration Roadmap</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Stats globais ────────────────────────────────────────────────────────────

g_done, g_total = count_all()
g_pct = int((g_done / g_total) * 100) if g_total > 0 else 0
total_channels = sum(len(st.session_state.structure[c]["channels"]) for c in CATEGORIES)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"<div class='stat-card'><div class='stat-value'>{g_done}</div><div class='stat-label'>Concluidos</div></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='stat-card'><div class='stat-value'>{g_total - g_done}</div><div class='stat-label'>Pendentes</div></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='stat-card'><div class='stat-value'>{g_pct}%</div><div class='stat-label'>Progresso Geral</div></div>", unsafe_allow_html=True)
with c4:
    st.markdown(f"<div class='stat-card'><div class='stat-value'>{total_channels}</div><div class='stat-label'>Canais Totais</div></div>", unsafe_allow_html=True)

st.markdown(f"""
<div class='progress-section'>
    <div class='progress-label'>
        <span>{g_done} de {g_total} itens concluidos</span>
        <span>{g_pct}%</span>
    </div>
    <div class='progress-bar-wrap'>
        <div class='progress-bar-fill' style='width:{g_pct}%'></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Category tab buttons ─────────────────────────────────────────────────────

t1, t2, t3 = st.columns(3)
for col, cat in zip([t1, t2, t3], CATEGORIES):
    c_done, c_total = count_category(cat)
    n_ch = len(st.session_state.structure[cat]["channels"])
    active_marker = "▶ " if st.session_state.active_category == cat else ""
    label = f"{active_marker}{CAT_ICONS[cat]} {cat}  [{n_ch} canais · {c_done}/{c_total}]"
    with col:
        if st.button(label, key=f"tab_{cat}", use_container_width=True):
            st.session_state.active_category = cat
            st.rerun()

st.markdown("<hr style='margin:14px 0 22px!important'>", unsafe_allow_html=True)

# ─── Categoria ativa ──────────────────────────────────────────────────────────

active_cat = st.session_state.active_category
cat_channels = st.session_state.structure[active_cat]["channels"]

# Mini progress da categoria
c_done, c_total = count_category(active_cat)
c_pct = int((c_done / c_total) * 100) if c_total > 0 else 0
st.markdown(f"""
<div class='cat-progress-wrap'>
    <span class='cat-progress-text'>{CAT_ICONS[active_cat]} {active_cat}</span>
    <div class='cat-progress-bar-wrap'>
        <div class='cat-progress-bar-fill' style='width:{c_pct}%'></div>
    </div>
    <span class='cat-progress-pct'>{c_done}/{c_total} &nbsp;·&nbsp; {c_pct}%</span>
</div>
""", unsafe_allow_html=True)

# ─── Formulário: adicionar canal ─────────────────────────────────────────────

with st.expander("➕  Adicionar novo canal / assunto principal"):
    nc1, nc2 = st.columns([3, 1])
    with nc1:
        new_ch_name = st.text_input("Nome do canal", key=f"nch_{active_cat}", placeholder="Ex: Shopee, Mercado Pago...")
    with nc2:
        new_prio = st.selectbox("Prioridade", ["alta", "media", "baixa"], key=f"nprio_{active_cat}")
    st.markdown("<div style='font-size:12px;color:#6868a0;margin:6px 0 10px'>Secoes padrao (voce pode adicionar ou renomear depois):</div>", unsafe_allow_html=True)
    s1c, s2c, s3c = st.columns(3)
    with s1c:
        sec1 = st.text_input("Secao 1", key=f"s1_{active_cat}", value="Suporte Track")
    with s2c:
        sec2 = st.text_input("Secao 2", key=f"s2_{active_cat}", value="Cliente")
    with s3c:
        sec3 = st.text_input("Secao 3 (opcional)", key=f"s3_{active_cat}", value="Video")

    if st.button("✓  Criar Canal", key=f"create_{active_cat}", use_container_width=True):
        name = new_ch_name.strip()
        if not name:
            st.warning("Digite o nome do canal.")
        elif name in cat_channels:
            st.warning("Ja existe um canal com esse nome nesta categoria.")
        else:
            sections = {}
            for sn in [sec1, sec2, sec3]:
                if sn.strip():
                    sections[sn.strip()] = []
            st.session_state.structure[active_cat]["channels"][name] = {"priority": new_prio, "sections": sections}
            persist_structure()
            st.success(f"Canal '{name}' criado!")
            st.rerun()

# ─── Estado vazio ─────────────────────────────────────────────────────────────

if not cat_channels:
    st.markdown(f"""
    <div class='empty-state'>
        <div class='empty-icon'>{CAT_ICONS[active_cat]}</div>
        <div class='empty-title'>Nenhum canal em {active_cat}</div>
        <div class='empty-sub'>Use o formulario acima para adicionar o primeiro canal desta categoria.</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─── Lista de canais ──────────────────────────────────────────────────────────

sorted_channels = sorted(cat_channels.items(), key=lambda x: PRIORITY_ORDER.get(x[1].get("priority","baixa"), 9))
current_priority = None

for ch_name, ch_data in sorted_channels:
    priority = ch_data.get("priority", "baixa")

    if priority != current_priority:
        current_priority = priority
        dot_cls = "dot-red" if priority == "alta" else "dot-amber" if priority == "media" else "dot-gray"
        p_label = {"alta": "Prioridade Alta", "media": "Prioridade Media", "baixa": "Prioridade Baixa"}.get(priority, priority)
        st.markdown(f'<div class="group-label"><span class="dot {dot_cls}"></span> {p_label}</div>', unsafe_allow_html=True)

    ch_done, ch_total = count_channel(active_cat, ch_name)
    ch_complete = ch_done == ch_total and ch_total > 0
    exp_key = f"{active_cat}|{ch_name}"

    col_btn, col_badge = st.columns([5, 1], gap="small")
    with col_btn:
        btn_lbl = f"✓  {ch_name}" if ch_complete else ch_name
        if st.button(btn_lbl, key=f"exp_{active_cat}_{ch_name}", use_container_width=True):
            st.session_state.expanded_channel[exp_key] = not st.session_state.expanded_channel.get(exp_key, False)
            st.rerun()
    with col_badge:
        bc = "done" if ch_complete else ""
        st.markdown(f"<div class='counter-badge {bc}'>{ch_done}/{ch_total}</div>", unsafe_allow_html=True)

    # Painel expandido
    if st.session_state.expanded_channel.get(exp_key, False):
        with st.container():
            st.markdown("<div class='expanded-card'>", unsafe_allow_html=True)
            sections = ch_data.get("sections", {})

            for sec_name, items in sections.items():
                st.markdown(f'<div class="section-title">{sec_name}</div>', unsafe_allow_html=True)

                if not items:
                    st.markdown("<div style='font-size:12px;color:#6868a0;padding:4px 0 8px'>Nenhum item ainda. Adicione abaixo.</div>", unsafe_allow_html=True)

                for item in items:
                    current_val = is_done(active_cat, ch_name, sec_name, item)
                    wk = f"cb__{active_cat}__{ch_name}__{sec_name}__{item}"
                    if wk not in st.session_state:
                        st.session_state[wk] = current_val
                    new_val = st.checkbox(item, key=wk)
                    if new_val != current_val:
                        set_done(active_cat, ch_name, sec_name, item, new_val)
                        st.rerun()

                # Adicionar item ao checklist
                ai_col1, ai_col2 = st.columns([4, 1], gap="small")
                with ai_col1:
                    ni = st.text_input("", key=f"ni_{active_cat}_{ch_name}_{sec_name}", placeholder=f"Novo item em '{sec_name}'...", label_visibility="collapsed")
                with ai_col2:
                    if st.button("+ Add", key=f"additem_{active_cat}_{ch_name}_{sec_name}", use_container_width=True):
                        if ni.strip():
                            if ni.strip() not in st.session_state.structure[active_cat]["channels"][ch_name]["sections"][sec_name]:
                                st.session_state.structure[active_cat]["channels"][ch_name]["sections"][sec_name].append(ni.strip())
                                persist_structure()
                                st.rerun()
                            else:
                                st.warning("Item ja existe nessa secao.")
                        else:
                            st.warning("Digite o nome do item.")

            # Adicionar nova secao
            st.markdown("<hr style='margin:16px 0 12px!important'>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:11px;color:#6868a0;text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px'>Adicionar nova secao</div>", unsafe_allow_html=True)
            ns1, ns2 = st.columns([4, 1], gap="small")
            with ns1:
                new_sec = st.text_input("", key=f"newsec_{active_cat}_{ch_name}", placeholder="Nome da nova secao...", label_visibility="collapsed")
            with ns2:
                if st.button("+ Secao", key=f"addsec_{active_cat}_{ch_name}", use_container_width=True):
                    if new_sec.strip():
                        if new_sec.strip() not in sections:
                            st.session_state.structure[active_cat]["channels"][ch_name]["sections"][new_sec.strip()] = []
                            persist_structure()
                            st.rerun()
                        else:
                            st.warning("Essa secao ja existe.")
                    else:
                        st.warning("Digite o nome da secao.")

            # Excluir canal
            st.markdown("<hr style='margin:12px 0!important'>", unsafe_allow_html=True)
            del_key = f"delconfirm_{active_cat}_{ch_name}"
            if st.session_state.get(del_key):
                st.markdown(f"<div style='font-size:13px;color:#ef4444;margin-bottom:8px'>Confirmar exclusao de <b>{ch_name}</b>? Esta acao e irreversivel.</div>", unsafe_allow_html=True)
                dc1, dc2 = st.columns(2)
                with dc1:
                    if st.button("Sim, excluir", key=f"delyes_{active_cat}_{ch_name}", use_container_width=True):
                        del st.session_state.structure[active_cat]["channels"][ch_name]
                        persist_structure()
                        st.session_state.expanded_channel.pop(exp_key, None)
                        st.rerun()
                with dc2:
                    if st.button("Cancelar", key=f"delno_{active_cat}_{ch_name}", use_container_width=True):
                        st.session_state[del_key] = False
                        st.rerun()
            else:
                if st.button(f"Excluir canal '{ch_name}'", key=f"delch_{active_cat}_{ch_name}", use_container_width=True):
                    st.session_state[del_key] = True
                    st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────

st.markdown("---")

f1, f2, f3 = st.columns(3)

with f1:
    rows = ["Categoria,Canal,Secao,Item,Status"]
    for cat in CATEGORIES:
        for ch, chd in st.session_state.structure[cat]["channels"].items():
            for sec, items in chd.get("sections", {}).items():
                for it in items:
                    status = "Feito" if is_done(cat, ch, sec, it) else "Pendente"
                    rows.append(f"{cat},{ch},{sec},{it},{status}")
    st.download_button(
        label="Exportar progresso (CSV)",
        data="\n".join(rows),
        file_name=f"doc-channels-{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )

with f2:
    if st.button("Limpar progresso (checkboxes)", use_container_width=True, key="clrprog"):
        if st.session_state.get("confirm_clrprog"):
            clear_progress_db()
            st.session_state.progress = {}
            for k in list(st.session_state.keys()):
                if k.startswith("cb__"):
                    del st.session_state[k]
            st.session_state.confirm_clrprog = False
            st.rerun()
        else:
            st.session_state.confirm_clrprog = True
            st.warning("Clique novamente para confirmar. Os canais serao mantidos.")

with f3:
    if st.button("Reset completo (canais + progresso)", use_container_width=True, key="clrall"):
        if st.session_state.get("confirm_clrall"):
            clear_progress_db()
            st.session_state.progress = {}
            st.session_state.structure = DEFAULT_STRUCTURE
            persist_structure()
            for k in list(st.session_state.keys()):
                if k.startswith("cb__"):
                    del st.session_state[k]
            st.session_state.confirm_clrall = False
            st.rerun()
        else:
            st.session_state.confirm_clrall = True
            st.warning("Clique novamente para confirmar o reset total.")
