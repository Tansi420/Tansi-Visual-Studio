"""Tema 'web 2000': CSS global, cabecera, paneles y widgets HTML reutilizables."""
import html as _html

import streamlit as st

from config import BPM_BASE, BPM_MAX, BPM_MIN

A = "/app/static/ui"      # GIFs generados con tools/make_assets.py

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Pixelify+Sans:wght@500;700&family=Silkscreen:wght@400;700&family=VT323&display=swap');
:root{--lime:#39ff14;--lime2:#b8ffb0;--pink:#ff5fd2;--lilac:#d68bff;--violet:#7a2cff;--ink:#05020c}
.stApp{
  background:
    radial-gradient(ellipse at 15% 10%, rgba(90,20,200,.38), transparent 55%),
    radial-gradient(ellipse at 85% 60%, rgba(20,40,200,.28), transparent 55%),
    linear-gradient(rgba(14,4,30,.66), rgba(5,2,12,.78)),
    url(__A__/bg.jpg) center/cover fixed #05020c;
  cursor:url(__A__/cursor.png) 2 2, auto;
}
.stApp, .stApp p, .stApp label, .stApp li, .stApp input, .stApp textarea,
.stApp button, .stApp [data-testid="stMarkdownContainer"], .stApp [data-testid="stCaptionContainer"]{
  font-family:'VT323','DotGothic16',monospace !important;
}
.stApp p, .stApp label, .stApp li{font-size:1.35rem;line-height:1.1;color:var(--lime2)}
[data-testid="stCaptionContainer"]{background:rgba(0,0,0,.62);padding:2px 10px;display:inline-block;border-left:3px solid var(--pink)}
[data-testid="stCaptionContainer"] p{color:var(--lilac);font-size:1.2rem}
a{color:var(--pink) !important}
a:hover{color:#fff !important;text-shadow:0 0 8px var(--pink)}
header[data-testid="stHeader"]{background:transparent}
[data-testid="stToolbar"], [data-testid="stDecoration"], footer{visibility:hidden}
.block-container{padding-top:1.2rem;max-width:1150px}
*{scrollbar-width:thin;scrollbar-color:var(--violet) #0a0014}
::-webkit-scrollbar{width:12px;height:12px}
::-webkit-scrollbar-track{background:#0a0014;border:1px solid var(--lime)}
::-webkit-scrollbar-thumb{background:var(--pink);border:2px outset #ffc2ee}
img.px{image-rendering:pixelated}

/* ---- cabecera ---- */
.tvs-head{position:relative;display:flex;align-items:center;justify-content:center;gap:18px;
  padding:14px 8px 6px;flex-wrap:wrap;text-align:center}
.tvs-row{display:flex;align-items:center;justify-content:center;gap:16px;width:100%}
.tvs-head .eye{height:54px}
.tvs-title{position:relative;font-family:'Pixelify Sans',monospace !important;font-weight:700;
  font-size:clamp(22px,4.6vw,56px);line-height:1;white-space:nowrap;color:#d9ff7a;letter-spacing:2px;
  text-shadow:0 0 6px #7cff3a,0 0 20px #1fa81f,4px 4px 0 #3b0a6b;animation:wob 3s ease-in-out infinite}
.tvs-title::before,.tvs-title::after{content:attr(data-text);position:absolute;left:0;top:0;width:100%;
  text-shadow:none;pointer-events:none}
.tvs-title::before{opacity:0;color:#00f0ff;clip-path:inset(0 0 58% 0);animation:gl1 2.6s infinite steps(1)}
.tvs-title::after{opacity:0;color:#ff2fd0;clip-path:inset(58% 0 0 0);animation:gl2 3.3s infinite steps(1)}
@keyframes gl1{0%,90%{opacity:0}91%{opacity:1;transform:translate(-5px,1px)}94%{opacity:1;transform:translate(4px,-1px)}96%,100%{opacity:0}}
@keyframes gl2{0%,86%{opacity:0}87%{opacity:1;transform:translate(5px,0)}90%{opacity:1;transform:translate(-4px,1px)}92%,100%{opacity:0}}
@keyframes wob{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}
.tvs-sub{width:auto;background:rgba(0,0,0,.65);padding:2px 12px;border:1px solid #ff5fd2;font-family:'Silkscreen',monospace !important;font-size:13px;letter-spacing:3px;
  color:var(--pink);text-shadow:0 0 8px var(--pink);animation:blink 1.6s steps(1) infinite}
@keyframes blink{50%{opacity:.25}}
.page-tag{display:inline-block;font-family:'Silkscreen',monospace !important;font-size:14px;color:#05020c;
  background:linear-gradient(var(--lime2),#2f9e2f);border:2px outset #b6ff6a;border-radius:14px;padding:2px 14px;margin:6px 0 2px}
.hazard{height:16px;margin:8px 0;background:url(__A__/hazard.gif) repeat-x;image-rendering:pixelated;
  border-top:2px solid #000;border-bottom:2px solid #000}
.ticker{overflow:hidden;white-space:nowrap;border:2px solid var(--lime);background:#000;margin:6px 0 14px;
  box-shadow:0 0 10px rgba(57,255,20,.45)}
.ticker span{display:inline-block;padding-left:100%;font-size:22px;color:var(--pink);animation:tick 34s linear infinite}
@keyframes tick{to{transform:translateX(-100%)}}
.chev{text-align:center;letter-spacing:4px;color:var(--lime);font-family:'Silkscreen',monospace !important;
  font-size:12px;margin:10px 0;text-shadow:0 0 6px var(--lime);animation:blink 2.2s steps(1) infinite}
.spark{position:absolute;width:24px;height:24px;image-rendering:pixelated}

/* ---- paneles ---- */
[data-testid="stVerticalBlockBorderWrapper"]{
  border:2px solid var(--lime) !important;border-radius:0 !important;
  background:rgba(0,10,0,.74) repeating-linear-gradient(0deg,rgba(57,255,20,.07) 0 1px,transparent 1px 14px),
             repeating-linear-gradient(90deg,rgba(57,255,20,.07) 0 1px,transparent 1px 14px) !important;
  box-shadow:0 0 14px rgba(57,255,20,.35), inset 0 0 22px rgba(122,44,255,.25)}
.ptitle{font-family:'Silkscreen',monospace !important;font-weight:700;font-size:19px;color:var(--lilac);
  text-shadow:0 0 8px var(--violet),2px 2px 0 #1a0033;border-bottom:2px dotted var(--lime);
  padding-bottom:4px;margin:0 0 10px;letter-spacing:1px}
.ptitle::before{content:'»» ';color:var(--lime)}
.stApp h1,.stApp h2,.stApp h3{font-family:'Silkscreen',monospace !important;color:var(--lilac)}

/* ---- botones ---- */
[data-testid="stButton"] button,[data-testid="stFormSubmitButton"] button,.stButton button{
  width:100%;font-family:'Silkscreen',monospace !important;font-size:13px;letter-spacing:1px;
  background:linear-gradient(#caff7a,#2f9e2f 55%,#1d6a1d) !important;color:#04210a !important;
  border:3px outset #b6ff6a !important;border-radius:20px !important;
  box-shadow:0 0 8px rgba(57,255,20,.6),inset 0 0 6px rgba(255,255,255,.4);text-shadow:1px 1px 0 #9f9;
  transition:transform .08s steps(2),filter .1s}
[data-testid="stButton"] button p,[data-testid="stFormSubmitButton"] button p{
  font-family:'Silkscreen',monospace !important;font-size:13px;color:#04210a !important;margin:0}
[data-testid="stButton"] button:hover,[data-testid="stFormSubmitButton"] button:hover{
  filter:hue-rotate(75deg) brightness(1.15);transform:translateY(-2px) scale(1.04);animation:shake .3s steps(2) infinite}
[data-testid="stButton"] button:active{border-style:inset !important;transform:translateY(2px)}
@keyframes shake{0%{transform:translate(-1px,-2px) scale(1.04)}50%{transform:translate(1px,-2px) scale(1.04)}}
[data-testid="stButton"] button[kind="primary"],[data-testid="stBaseButton-primary"]{
  background:linear-gradient(#ffb3ec,#ff2fd0 55%,#8a0f78) !important;color:#fff !important;
  border:3px inset #ffc2ee !important;text-shadow:1px 1px 0 #400;
  box-shadow:0 0 14px #ff2fd0,inset 0 0 8px rgba(255,255,255,.5);animation:pulse 1.1s steps(2) infinite}
[data-testid="stButton"] button[kind="primary"] p,[data-testid="stBaseButton-primary"] p{color:#fff !important}
@keyframes pulse{50%{box-shadow:0 0 24px #ff2fd0,inset 0 0 8px rgba(255,255,255,.5)}}

/* ---- inputs ---- */
[data-baseweb="input"],[data-baseweb="base-input"],[data-baseweb="textarea"]{
  background:#000 !important;border-radius:0 !important;border-color:var(--lime) !important}
[data-baseweb="input"] input{color:#7cff3a !important;font-size:1.4rem}
[data-testid="stForm"]{border:2px dashed var(--violet) !important;border-radius:0 !important;background:rgba(10,0,30,.6)}
[data-testid="stAudioInput"]{border:2px solid var(--violet);background:#0a0014;border-radius:0}
[data-testid="stSlider"] [role="slider"]{background:var(--pink) !important;border-radius:0 !important;
  box-shadow:0 0 8px var(--pink);border:2px solid #fff}
[data-testid="stAlert"]{background:#14002b !important;border:2px dashed var(--pink) !important;border-radius:0 !important}
[data-testid="stAlert"] p{color:#ffd1f5}
iframe{border:3px ridge var(--lime) !important;box-shadow:0 0 18px rgba(57,255,20,.45),0 0 40px rgba(122,44,255,.35);background:#000}

/* ---- barra lateral ---- */
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0c0020,#050010 60%,#001a0a);border-right:3px double var(--lime)}
[data-testid="stSidebarNav"] a,[data-testid="stSidebarNavLink"]{
  font-family:'Silkscreen',monospace !important;background:linear-gradient(#caff7a,#2f9e2f 60%,#1d6a1d) !important;
  border:2px outset #b6ff6a;border-radius:20px;margin:6px 0;box-shadow:0 0 8px rgba(57,255,20,.5);justify-content:center}
[data-testid="stSidebarNav"] a span,[data-testid="stSidebarNavLink"] span,[data-testid="stSidebarNavLink"] p{
  color:#04210a !important;font-family:'Silkscreen',monospace !important;font-size:13px !important}
[data-testid="stSidebarNav"] a:hover,[data-testid="stSidebarNavLink"]:hover{filter:hue-rotate(75deg);animation:shake .3s steps(2) infinite}
[data-testid="stSidebarNav"] a[aria-current="page"],[data-testid="stSidebarNavLink"][aria-current="page"]{
  background:linear-gradient(#ffb3ec,#ff2fd0 55%,#8a0f78) !important;border-color:#ffc2ee}
[data-testid="stSidebarNav"] a[aria-current="page"] span,[data-testid="stSidebarNavLink"][aria-current="page"] span,
[data-testid="stSidebarNavLink"][aria-current="page"] p{color:#fff !important}
.side{text-align:center}
.side img{display:block;margin:6px auto}
.side .cap{font-family:'Silkscreen',monospace !important;font-size:10px;color:var(--lilac);letter-spacing:1px}
.counter{display:inline-block;background:#000;border:2px inset #555;color:#ff2e3b;font-size:24px;letter-spacing:4px;padding:0 8px;
  text-shadow:0 0 6px #f00}

/* ---- lecturas en vivo y terminal ---- */
.lcd-row{display:flex;flex-wrap:wrap;gap:10px;align-items:stretch;margin:4px 0 10px}
.lcd{flex:1 1 90px;background:#000;border:2px inset #555;padding:4px 8px;text-align:center}
.lcd small{display:block;font-family:'Silkscreen',monospace !important;font-size:10px;color:var(--lilac)}
.lcd b{font-family:'Pixelify Sans',monospace !important;font-size:32px;color:#7cff3a;text-shadow:0 0 8px #39ff14}
.bar{flex:2 1 170px;background:#000;border:2px inset #555;padding:4px 8px}
.bar small{display:block;font-family:'Silkscreen',monospace !important;font-size:10px;color:var(--lilac);margin-bottom:4px}
.bar div{height:14px;background:#0a1a0a;border:1px solid #145214}
.bar i{display:block;height:100%;background:repeating-linear-gradient(90deg,#39ff14 0 6px,transparent 6px 8px)}
.bar.p i{background:repeating-linear-gradient(90deg,#ff5fd2 0 6px,transparent 6px 8px)}
.flag{flex:1 1 90px;display:flex;align-items:center;justify-content:center;font-family:'Silkscreen',monospace !important;
  font-size:11px;border:2px solid #333;color:#444;background:#000}
.flag.on{color:#fff;border-color:var(--pink);background:#3a0030;text-shadow:0 0 8px var(--pink);animation:blink .9s steps(1) infinite}
.pill{display:inline-block;font-family:'Silkscreen',monospace !important;font-size:11px;padding:2px 10px;border:2px solid;margin-bottom:6px}
.pill.ok{color:var(--lime);border-color:var(--lime);text-shadow:0 0 6px var(--lime)}
.pill.no{color:#ffb000;border-color:#ffb000;animation:blink 1s steps(1) infinite}
.term{background:#000;border:2px inset #444;padding:8px 10px;font-size:1.25rem;line-height:1.05;color:#7cff3a;
  max-height:230px;overflow:auto;text-shadow:0 0 4px rgba(57,255,20,.7)}
.term .t{color:#8a8aa8}.term .o{color:var(--pink)}
.term::after{content:'_';animation:blink .8s steps(1) infinite}
.tips li{font-size:1.25rem}

/* ---- decoraciones (GIFs) ---- */
.strip{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:16px;margin:14px 0}
.strip img,.side-gifs img{max-height:104px;width:auto;image-rendering:pixelated}
.deco{filter:drop-shadow(0 0 6px rgba(57,255,20,.65));transition:transform .1s steps(2)}
.deco.fr{border:3px ridge #d68bff;box-shadow:0 0 12px rgba(122,44,255,.8);filter:none;background:#000}
.deco:hover{animation:shake .3s steps(2) infinite;filter:hue-rotate(90deg) drop-shadow(0 0 8px #ff5fd2)}
.side-gifs{display:flex;flex-direction:column;align-items:center;gap:12px;margin:10px 0}
.side-gifs img{max-width:150px}
#rail, #rail-left{position:fixed;top:0;width:160px;height:100vh;overflow:hidden;z-index:1;pointer-events:none;
  border-left:3px double var(--lime);border-right:3px double var(--lime);background:linear-gradient(90deg,rgba(5,2,12,.72),rgba(20,0,40,.72))}
#rail{right:14px}
#rail-left{left:14px}
#rail .track, #rail-left .track{display:flex;flex-direction:column;align-items:center;gap:18px;padding:14px 0}
#rail .track{animation:railscroll 70s linear infinite}
#rail-left .track{animation:railscroll-rev 70s linear infinite}
#rail img, #rail-left img{max-width:128px;height:auto;image-rendering:pixelated}
@keyframes railscroll{from{transform:translateY(0)}to{transform:translateY(-50%)}}
@keyframes railscroll-rev{from{transform:translateY(-50%)}to{transform:translateY(0)}}
@media (max-width:1280px){#rail, #rail-left{display:none}}
@media (min-width:1281px){.block-container{padding-left:200px !important;padding-right:200px !important}}
.padrow{display:flex;flex-wrap:wrap;gap:8px;margin:2px 0 10px}
.padi{display:flex;align-items:center;gap:6px;padding:3px 10px;border:2px solid #333;background:#000;
  font-family:'Silkscreen',monospace !important;font-size:11px;color:#777;opacity:.45;filter:grayscale(1)}
.padi.on{opacity:1;filter:none;color:#fff;border-color:var(--pink);box-shadow:0 0 12px var(--pink);background:#3a0030}
.padi img{image-rendering:pixelated}
/* iconos animados en los pads (botonmusica = audio, botonvideo = visual) */
[class*="st-key-pad_audio_"] button,[class*="st-key-pad_video_"] button{display:flex;align-items:center;justify-content:center;gap:6px}
[class*="st-key-pad_audio_"] button::before{content:'';width:36px;height:31px;flex:none;
  background:url(__A__/deco/botonmusica.gif) center/contain no-repeat;image-rendering:pixelated}
[class*="st-key-pad_video_"] button::before{content:'';width:25px;height:25px;flex:none;
  background:url(__A__/deco/botonvideo.gif) center/contain no-repeat;image-rendering:pixelated}
@media (prefers-reduced-motion:reduce){*{animation:none !important}}
"""

TICKER = ("♥ bienvenid@ a la guarida visual de tansi ♥ &nbsp;&nbsp; ~*~ 4 audios · 4 visuales · 140 bpm ~*~ &nbsp;&nbsp; "
          "mejor visto en chrome o edge &nbsp;&nbsp; ★ gira los faders, aprieta los pads, habla con la máquina ★ &nbsp;&nbsp; "
          "bajo construcción para siempre &nbsp;&nbsp;")


# --- reparto de los 25 GIFs decorativos (static/ui/deco/<nombre>.gif) ---
RAIL = ["speaker_eq", "dj", "lips", "speaker_tall", "ear_blow", "speaker_chrome", "speaker_sky", "speaker_black"]
RAIL_LEFT = list(reversed(RAIL))
SIDE = ["music_girl", "junglist", "ear_small", "speaker_mini"]
HEAD = ("eye_round", "red_eye")
STRIP_B = ["boombox", "notes_bar", "eyes_strip", "eye_bars", "eye_arrows", "eye_gray"]
STRIP_C = ["blue_eye", "split_eye", "eye_thai", "leaves", "flower_eye"]
FRAMED = {"speaker_mini", "eyes_strip", "lips", "speaker_sky", "ear_blow", "eye_arrows", "blue_eye", "split_eye",
          "junglist", "speaker_black", "eye_thai", "eye_gray"}      # GIFs sin transparencia -> marco tipo polaroid


def _gif(name: str, extra: str = "", i: int = 0) -> str:
    cls = "px deco fr" if name in FRAMED else "px deco"
    return f'<img class="{cls}" src="{A}/deco/{name}.gif" style="transform:rotate({(i % 5 - 2) * 1.6}deg);{extra}">'


def strip(names: list):
    st.markdown('<div class="strip">' + "".join(_gif(n, i=i) for i, n in enumerate(names)) + "</div>", unsafe_allow_html=True)


def _rail_html() -> str:
    items_right = "".join(f'<img src="{A}/deco/{n}.gif">' for n in RAIL)
    items_left = "".join(f'<img src="{A}/deco/{n}.gif">' for n in RAIL_LEFT)
    return (
        f'<div id="rail"><div class="track">{items_right}{items_right}</div></div>'
        f'<div id="rail-left"><div class="track">{items_left}{items_left}</div></div>'
    )


def inject_theme():
    st.markdown(f"<style>{CSS.replace('__A__', A)}</style>" + _rail_html(), unsafe_allow_html=True)


def sidebar_decor():
    gifs = "".join(_gif(n, i=i) for i, n in enumerate(SIDE))
    st.markdown(
        '<div class="side"><div class="cap">~ TANSI VJ v0.3 ~</div>'
        f'<div class="side-gifs">{gifs}</div>'
        f'<img class="px" src="{A}/btn_tansi.gif"><img class="px" src="{A}/btn_wokwi.gif">'
        f'<img class="px" src="{A}/btn_mqtt.gif"><img class="px" src="{A}/btn_music.gif">'
        f'<img class="px" src="{A}/btn_vj.gif"><img class="px" src="{A}/btn_chrome.gif">'
        '<div class="cap">VISITANTES</div><div class="counter">001337</div>'
        f'<div class="cap" style="margin-top:8px"><img class="px" src="{A}/heart.gif" style="display:inline;width:18px;margin:0"> '
        'hecho con wokwi + mqtt</div></div>', unsafe_allow_html=True)


def header(page_tag: str):
    sp = lambda x, y, d: f'<img class="spark" src="{A}/sparkle.gif" style="left:{x}%;top:{y}px;animation:blink {d}s steps(1) infinite">'
    st.markdown(
        '<div class="tvs-head">' + sp(4, 8, 1.7) + sp(93, 20, 2.3) + sp(18, 70, 1.3) + sp(80, 76, 2.9)
        + f'<div class="tvs-row">{_gif(HEAD[0], "height:60px;", 1)}'
        '<div class="tvs-title" data-text="Tansi Visual Studio">Tansi Visual Studio</div>'
        f'{_gif(HEAD[1], "height:60px;")}</div>'
        '<div class="tvs-sub">~*~ interfaces multimodales · vj lab ~*~</div>'
        f'<div><span class="page-tag">{_html.escape(page_tag)}</span></div></div>'
        '<div class="hazard"></div>'
        f'<div class="ticker"><span>{TICKER}</span></div>', unsafe_allow_html=True)


def ptitle(text: str):
    st.markdown(f'<div class="ptitle">{_html.escape(text)}</div>', unsafe_allow_html=True)


def chevrons():
    st.markdown('<div class="chev">» » » » » » » » » » » » » » » » » » » » » » » »</div>', unsafe_allow_html=True)


def footer():
    strip(STRIP_C)
    st.markdown(
        '<div class="hazard"></div><div class="side">'
        f'<img class="px" src="{A}/btn_chrome.gif" style="display:inline"> <img class="px" src="{A}/btn_mqtt.gif" style="display:inline"> '
        f'<img class="px" src="{A}/btn_wokwi.gif" style="display:inline"> <img class="px" src="{A}/btn_vj.gif" style="display:inline">'
        '<div class="cap" style="margin-top:6px">© 2026 tansi visual studio · todos los derechos reservados al vacío</div></div>',
        unsafe_allow_html=True)


def status_html(connected: bool, s: dict) -> str:
    vol = s["volumen"]
    bpm_pct = round((s["bpm"] - BPM_MIN) * 100 / (BPM_MAX - BPM_MIN))
    pill = '<span class="pill ok">● BROKER CONECTADO</span>' if connected else '<span class="pill no">○ CONECTANDO AL BROKER…</span>'
    pads = '<div class="padrow">' + "".join(
        f'<div class="padi{" on" if s["audio"] == i else ""}"><img src="{A}/deco/botonmusica.gif">A{i}</div>' for i in range(1, 5)
    ) + "".join(
        f'<div class="padi{" on" if s["video"] == i else ""}"><img src="{A}/deco/botonvideo.gif">V{i}</div>' for i in range(1, 5)
    ) + "</div>"
    return (pill + pads + '<div class="lcd-row">'
            f'<div class="lcd"><small>AUDIO</small><b>A{s["audio"]}</b></div>'
            f'<div class="lcd"><small>VISUAL</small><b>V{s["video"]}</b></div>'
            f'<div class="bar"><small>VOLUMEN {vol}%</small><div><i style="width:{vol}%"></i></div></div>'
            f'<div class="bar p"><small>BPM {s["bpm"]} · {s["bpm"] / BPM_BASE:.2f}x</small><div><i style="width:{bpm_pct}%"></i></div></div>'
            f'<div class="flag{" on" if s["invierte"] else ""}">INVERTIDO</div>'
            f'<div class="flag{" on" if s["silencio"] else ""}">SILENCIO</div></div>')


def log_html(rows: list) -> str:
    if not rows:
        return '<div class="term"><span class="t">// esperando señales del universo…</span></div>'
    lines = [f'<span class="t">[{_html.escape(r["Hora"])}]</span> <span class="o">{_html.escape(r["Origen"])}</span> '
             f'{_html.escape(r["Evento"])}' for r in rows]
    return '<div class="term">' + "<br>".join(lines) + "</div>"