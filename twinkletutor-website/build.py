"""Build the Twinkle Tutor site into docs/ (served by GitHub Pages). Run: python3 build.py"""
import re
from html import escape as e
from pathlib import Path
from urllib.parse import quote

from data import EXAMS, FEATURED_STATES, GRADES, REGIONS, STATES, SUBJECTS

ROOT = Path(__file__).parent / "docs"
B = "/us"
CUR = f"{B}/us-curriculum"
TP = f"{B}/test-prep"
EMAIL = "hello@twinkletutor.com"
SITE = "https://twinkletutor.com"
DOMAIN = "twinkletutor.com"
# Where the free trial and contact forms send submissions, e.g. a Formspree URL
# like "https://formspree.io/f/abcdwxyz". Leave empty to use Netlify Forms.
FORM_ENDPOINT = ""
STATE = {s[0]: s for s in STATES}

CARET = '<svg class="caret" viewBox="0 0 10 10" aria-hidden="true"><path d="M1 3l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'
MARK = '<svg class="logo-mark" viewBox="0 0 24 24" aria-hidden="true"><path d="M11 3c.9 5.6 3 7.7 8.6 8.6-5.6.9-7.7 3-8.6 8.6-.9-5.6-3-7.7-8.6-8.6C8 10.700 10.100 8.600 11 3z" fill="#F5A524"/><path d="M19 2c.3 2 1 2.700 3 3-2 .3-2.700 1-3 3-.3-2-1-2.700-3-3 2-.3 2.700-1 3-3z" fill="#A597F5"/></svg>'
LOGO = f'<a class="logo" href="{B}" aria-label="Twinkle Tutor home">{MARK}<span>Twinkle<b>Tutor</b></span></a>'


def a(href, text, cls=None):
    c = f' class="{cls}"' if cls else ""
    return f'<a{c} href="{href}">{e(text)}</a>'


def header():
    states = "".join(a(f"{CUR}/{s}", STATE[s][1]) for s in FEATURED_STATES[:8])
    grades = "".join(a(f"{CUR}/{g[0]}", g[1]) for g in GRADES)
    subjects = "".join(a(f"{CUR}/{s[0]}", f"{s[1]} Tutor") for s in SUBJECTS)
    exams = "".join(a(f"{TP}/{x[0]}", x[1]) for x in EXAMS)
    return f"""<div class="topbar"><div class="container">
  <span>Online tutoring for US students · Kindergarten to 12th Grade</span>
  <span><a href="mailto:{EMAIL}">{EMAIL}</a></span>
</div></div>
<header class="site-header"><div class="container nav">
  {LOGO}
  <ul class="menu">
    <li><button type="button">Curriculum {CARET}</button>
      <div class="dropdown wide">
        <div><h5>Overview</h5>{a(CUR, "US Curriculum & Standards")}<h5>States</h5>{states}{a(f"{CUR}/states", "All 50 states + DC →")}</div>
        <div><h5>Grade levels</h5>{grades}</div>
      </div></li>
    <li><button type="button">Subjects {CARET}</button><div class="dropdown">{subjects}</div></li>
    <li><button type="button">Test Prep {CARET}</button><div class="dropdown">{exams}</div></li>
    <li>{a(f"{B}/pricing", "Pricing")}</li>
    <li>{a(f"{B}/about", "About")}</li>
    <li>{a(f"{B}/contact-us", "Contact")}</li>
  </ul>
  <div class="nav-cta">
    <a class="btn btn-ghost btn-sm" href="{B}/contact-us">Talk to us</a>
    <a class="btn btn-accent btn-sm" href="{B}/free-trial">Free Trial</a>
    <button class="nav-toggle" type="button" aria-label="Menu"><svg width="22" height="22" viewBox="0 0 24 24"><path d="M3 6h18M3 12h18M3 18h18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>
  </div>
</div></header>"""


def footer():
    li = lambda h, t: f"<li>{a(h, t)}</li>"
    company = "".join(li(h, t) for h, t in [(B, "Home"), (CUR, "US Curriculum"), (f"{B}/pricing", "Pricing"), (f"{B}/about", "About Us"), (f"{B}/contact-us", "Contact Us"), (f"{B}/free-trial", "Free Trial")])
    subjects = "".join(li(f"{CUR}/{s[0]}", f"{s[1]} Tutor") for s in SUBJECTS)
    exams = "".join(li(f"{TP}/{x[0]}", x[1]) for x in EXAMS)
    states = "".join(li(f"{CUR}/{s}", STATE[s][1]) for s in FEATURED_STATES[:6])
    return f"""<footer class="site-footer"><div class="container">
  <div class="footer-grid">
    <div>
      {LOGO}
      <p>Live 1-on-1 online tutoring for K–12 students in all 50 states, aligned with Common Core and each state's standards.</p>
      <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
    <div><h4>Company</h4><ul>{company}</ul></div>
    <div><h4>Subjects</h4><ul>{subjects}</ul></div>
    <div><h4>Test Prep</h4><ul>{exams}</ul></div>
    <div><h4>States & Grades</h4><ul>{states}<li>{a(f"{CUR}/states", "All 50 states →")}</li><li>{a(f"{CUR}#grades", "All grade levels →")}</li></ul></div>
  </div>
  <div class="footer-bottom">
    <span>© <span data-year>2026</span> Twinkle Tutor</span>
    <ul><li>{a(f"{B}/privacy", "Privacy Policy")}</li><li>{a(f"{B}/refund", "Refund Policy")}</li><li>{a(f"{B}/terms-and-conditions", "Terms & Conditions")}</li></ul>
  </div>
</div></footer>"""


FORM_ATTRS = f' action="{FORM_ENDPOINT}" data-endpoint="{FORM_ENDPOINT}"' if FORM_ENDPOINT else ""


def page(path, title, desc, body):
    url = f"{B}/{path}".rstrip("/")
    html = f"""<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{url}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>

{header()}
<main>
{body}
</main>

{footer()}
<script src="/assets/main.js"></script>
</body>
</html>
"""
    out = ROOT / "us" / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)


# ---------- shared blocks ----------

def crumbs(*items):
    parts = [a(B, "Home")]
    for item in items:
        parts.append(a(*item) if isinstance(item, tuple) else f"<span>{e(item)}</span>")
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span aria-hidden="true">/</span>'.join(parts) + "</nav>"


def hero(eyebrow, h1, lead, ctas=None, points=None, crumb="", aside="", compact=True):
    ctas = ctas if ctas is not None else [(f"{B}/free-trial", "Book a free trial"), (f"{B}/pricing", "See pricing")]
    cta = ""
    if ctas:
        cta = '<div class="hero-ctas">' + "".join(a(h, t, "btn btn-primary" if i == 0 else "btn btn-ghost") for i, (h, t) in enumerate(ctas)) + "</div>"
    pts = '<ul class="hero-points">' + "".join(f"<li>{e(p)}</li>" for p in points) + "</ul>" if points else ""
    return f"""<section class="hero{' compact' if compact and not aside else ''}"><div class="container hero-grid">
  <div>
    {crumb}
    <span class="eyebrow">{e(eyebrow)}</span>
    <h1>{h1}</h1>
    <p class="lead">{e(lead)}</p>
    {cta}
    {pts}
  </div>
  {aside}
</div></section>"""


def lesson_card(title="Today's lesson", sub="7th Grade Math · Pre-Algebra"):
    return f"""<div class="hero-card">
  <h3>{e(title)}</h3><div class="sub">{e(sub)}</div>
  <div class="lesson-mock">
    <div class="lesson-row"><span class="avatar">EM</span><div><b>Emily · Your tutor</b><small>M.Ed. Mathematics · Background-checked ✓</small></div></div>
    <div class="lesson-row"><span class="avatar">✓</span><div style="flex:1"><b>Learning goal</b><small>Solve two-step linear equations</small><div class="progress" style="margin-top:8px"><i style="width:72%"></i></div></div></div>
    <div class="lesson-row"><span class="avatar">→</span><div><b>Lesson notes sent to parent</b><small>Strengths, next steps & homework</small></div></div>
  </div>
</div>"""


def section(inner, alt=False, extra="", attrs=""):
    return f'<section class="section{" alt" if alt else ""}{extra}"{attrs}><div class="container">{inner}</div></section>'


def head(h2, kicker="", p="", center=False):
    k = f"<span class=kicker>{e(kicker)}</span>" if kicker else ""
    pp = f"<p>{e(p)}</p>" if p else ""
    return f'<div class="section-head{" center" if center else ""}">{k}<h2>{e(h2)}</h2>{pp}</div>'


def card(href, title, p, more="", tile="", tag=""):
    t = f'<div class="tile {tile[1]}">{e(tile[0])}</div>' if tile else ""
    tg = f'<span class="tag">{e(tag)}</span>' if tag else ""
    m = f'<span class="more">{e(more)}</span>' if more else ""
    return f'<a class="card" href="{href}">{t}{tg}<h3>{e(title)}</h3><p>{e(p)}</p>{m}</a>'


def subject_cards():
    return '<div class="grid g3">' + "".join(card(f"{CUR}/{s[0]}", f"{s[1]} Tutor", s[4], f"Explore {s[1]} →", (s[2], s[3])) for s in SUBJECTS) + "</div>"


def exam_cards(slugs=None):
    xs = [x for x in EXAMS if not slugs or x[0] in slugs]
    return '<div class="grid g4">' + "".join(card(f"{TP}/{x[0]}", x[1], x[2], "Learn more →", tag=x[3]) for x in xs) + "</div>"


def grade_chips():
    return '<div class="chip-list">' + "".join(a(f"{CUR}/{g[0]}", g[1], "chip") for g in GRADES) + "</div>"


def state_chips(states=STATES):
    return '<div class="chip-list">' + "".join(a(f"{CUR}/{s[0]}", s[1], "chip") for s in states) + "</div>"


def state_cards(slugs):
    return '<div class="grid g2">' + "".join(
        card(f"{CUR}/{s}", STATE[s][1], f"{STATE[s][4]} · {STATE[s][5].split(' (')[0]}", f"{STATE[s][2]} tutoring →", (STATE[s][2], "t-blue"))
        for s in slugs) + "</div>"


STEPS = [("Book a free trial", "Tell us about your child, their grade and goals. It takes 2 minutes."),
         ("Get matched", "We pair your child with a background-checked tutor who knows your state's standards."),
         ("Learn 1-on-1 online", "Live lessons on an interactive whiteboard, at times that suit your family."),
         ("Track progress", "Lesson notes after every session and regular progress reports for parents.")]


def steps():
    return '<div class="grid g4 steps">' + "".join(f'<div class="card step"><h3>{e(h)}</h3><p>{e(p)}</p></div>' for h, p in STEPS) + "</div>"


def faq(items):
    return '<div class="faq">' + "".join(f"<details><summary>{e(q)}</summary><p>{e(ans)}</p></details>" for q, ans in items) + "</div>"


def table(rows, head_row=None):
    th = "<thead><tr>" + "".join(f"<th>{e(c)}</th>" for c in head_row) + "</tr></thead>" if head_row else ""
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) if head_row else \
        "".join(f"<tr><th style='width:40%'>{e(k)}</th><td>{e(v)}</td></tr>" for k, v in rows)
    return f'<div class="table-wrap"><table>{th}<tbody>{body}</tbody></table></div>'


def cta(h="Try a free 1-on-1 lesson"):
    return f"""<section class="section tight"><div class="container"><div class="cta-band">
  <div><h2>{e(h)}</h2><p>Meet your tutor, get a personalized learning plan and see the difference — no payment details needed.</p></div>
  <div class="actions"><a class="btn btn-accent" href="{B}/free-trial">Book free trial</a><a class="btn btn-white" href="{B}/contact-us">Ask a question</a></div>
</div></div></section>"""


MAIN_FAQ = [
    ("How does online tutoring work?", "Lessons are live and 1-on-1 over video, with an interactive whiteboard. Your child needs a laptop or tablet with a camera and a stable internet connection."),
    ("Who are your tutors?", "Every tutor has a college degree and a background check, and is interviewed and trained before teaching. Many are certified teachers or subject specialists."),
    ("Do you follow my state's standards?", "Yes. Tutors follow Common Core or your state's own standards (such as TEKS in Texas, B.E.S.T. in Florida or the Virginia SOLs), plus your child's class syllabus."),
    ("Is the free trial really free?", "Yes. The first session is free, with no obligation and no payment details needed."),
    ("Which time zones do you cover?", "All of them. We schedule lessons in your local time, from Eastern to Hawaii–Aleutian."),
    ("What if we need to cancel a session?", "You can reschedule or cancel at no charge with at least 24 hours' notice. See our Refund Policy for details."),
]


# ---------- pages ----------

SEAL_TEXT = "FREE TRIAL · 1-ON-1 · LIVE · ALL 50 STATES · "


def studio_hero():
    seal = f"""<div class="seal" aria-hidden="true"><svg viewBox="0 0 160 160">
      <defs><path id="sealPath" d="M80,80 m-58,0 a58,58 0 1,1 116,0 a58,58 0 1,1 -116,0"/></defs>
      <path d="M80 6 l6 6 8-3 4 7 9-1 2 8 8 1 0 8 8 3-2 8 7 5-4 7 5 6-6 6 3 8-7 4 1 8-8 2-1 9-8 0-3 8-8-2-5 7-7-4-6 5-6-5-7 4-5-7-8 2-3-8-8 0-1-9-8-2 1-8-7-4 3-8-6-6 5-6-4-7 7-5-2-8 8-3 0-8 8-1 2-8 9 1 4-7 8 3z" fill="#fff" stroke="currentColor" stroke-width="1.2"/>
      <circle cx="80" cy="80" r="44" fill="none" stroke="currentColor" stroke-width="1"/>
      <text font-size="13" font-weight="800" letter-spacing="3" fill="currentColor"><textPath href="#sealPath">{SEAL_TEXT}</textPath></text>
      <circle cx="80" cy="80" r="26" fill="none" stroke="#16152b" stroke-width="3"/>
      <path d="M58 74c14 2 30 2 44 0M58 86c14-2 30-2 44 0M80 54c-10 14-10 38 0 52M80 54c10 14 10 38 0 52" fill="none" stroke="#16152b" stroke-width="2.4"/>
    </svg></div>"""
    return f"""<section class="studio"><div class="container studio-grid">
  <div>
    <div class="studio-mark">{MARK}</div>
    <div class="studio-name"><b>Twinkle Tutor</b><span class="select-badge"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 1.5 9.8 5.6l4.4.4-3.3 2.9 1 4.3L8 10.9l-3.9 2.3 1-4.3L1.8 6l4.4-.4z" fill="currentColor"/></svg>USA · K–12</span></div>
    <h1>Online Tutoring · Math, English, Science, SAT &amp; ACT<span class="dot">.</span></h1>
    <ul class="studio-meta"><li>Kindergarten–12th Grade</li><li>All 50 states + DC</li><li>Live 1-on-1</li></ul>
    <div class="studio-ctas">
      <a class="btn btn-primary" href="{B}/free-trial">Book a free trial</a>
      <a class="btn btn-ghost" href="{B}/pricing">See pricing</a>
      <a class="btn btn-icon" href="{CUR}/states" aria-label="Find your state"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg></a>
    </div>
  </div>
  <div class="bento">
    {seal}
    <div class="b-stats"><div><b>1-on-1</b><small>Live lessons with<br>expert tutors</small></div><div><b>K–12</b><small>Every grade<br>— all 50 states + DC</small></div></div>
    <a class="b-tile b-violet" href="{CUR}" style="text-decoration:none"><span class="top">Standards-aligned</span><b>Common Core</b><small>TEKS · B.E.S.T. · SOL</small></a>
    <a class="b-tile b-light" href="{TP}/sat" style="text-decoration:none;color:inherit"><b>SAT · ACT</b><small>+ AP &amp; state tests</small></a>
    <div class="b-device" aria-hidden="true"><div class="laptop"><div class="screen"><div class="ui">
      <div class="bar"><span>TWINKLE TUTOR</span><span>Lessons · Progress · Messages</span></div>
      <h6>Hello, Marcus!</h6>
      <div class="row"><i></i>Your SAT practice test is scored</div>
      <div class="promo">Next lesson: Algebra 2 · Thu 4:30 PM ET with Emily</div>
      <div class="row"><i style="background:#a597f5"></i>Upcoming: AP Calculus review</div>
      <div class="row"><i style="background:#f5a524"></i>Lesson notes sent to parent</div>
    </div></div><div class="base"></div></div></div>
    <div class="b-quote"><p>Your first 60-minute lesson is free. Meet your tutor and get a personalized learning plan, with no payment details needed.</p><a class="more" href="{B}/free-trial">Book a free lesson →</a></div>
  </div>
</div></section>"""


def home():
    body = studio_hero()
    body += '<section class="section tight"><div class="container"><div class="stats">' + "".join(
        f"<div class=stat><b>{b}</b><span>{s}</span></div>" for b, s in
        [("1-on-1", "Live online lessons"), ("K–12", "Every grade level"), ("50 + DC", "States covered"), ("100%", "Background-checked tutors")]) + "</div></div></section>"
    body += section(head("Expert tutors in every core subject", "Subjects", "Specialist tutors matched to your child's grade, state and learning style.") + subject_cards(), alt=True)
    body += section(head("How it works", "Simple process", "Getting started takes minutes, and your first lesson is free.", center=True) + steps())
    body += section(head("Test prep that builds real confidence", "Test prep", "From state tests and the SHSAT to the SAT, ACT and AP exams — structured plans with plenty of practice.") + exam_cards(), alt=True)
    body += section(f"""<div class="split">
      <div><span class="kicker">Standards-aligned</span><h2>Taught to your state's standards</h2>
        <p class="lead">Most states use Common Core-based standards, and some write their own, like TEKS in Texas, Florida's B.E.S.T. and Virginia's SOLs. Our tutors know the standards and the annual test for your state.</p>
        <a class="btn btn-primary mt" href="{CUR}/states">Find your state</a></div>
      <div>{state_cards(FEATURED_STATES[:6])}</div></div>""")
    body += section(head("Tutoring for every grade level", "Kindergarten to 12th Grade", "Choose a grade to see what we cover in Math, English and Science.") + grade_chips(), alt=True)
    body += section(head("Frequently asked questions", "FAQ", center=True) + faq(MAIN_FAQ), alt=True)
    body += cta()
    page("", "Online Tutoring USA | K–12, SAT & ACT | Twinkle Tutor",
         "Live 1-on-1 online tutoring for US students, K–12. Math, English, Science, state tests, SAT, ACT & AP, aligned with your state's standards. Book a free trial.", body)


def curriculum():
    body = hero("US Curriculum & Standards", "Tutoring aligned with US standards",
                "The US has no national curriculum. Each state sets its own standards, and most are based on Common Core and NGSS. Our tutors follow your state's standards and your child's class syllabus.",
                crumb=crumbs("US Curriculum"))
    body += section(head("How the US curriculum works", "Overview") + f"""<div class="split"><div>
      <p>Each state sets its own learning standards, and local school districts choose the curriculum and textbooks. Many states use the <b>Common Core State Standards</b> for Math and English Language Arts, and many use the <b>Next Generation Science Standards (NGSS)</b> or a version of them. Others, like Texas, Florida, Virginia and Indiana, use standards they wrote themselves.</p>
      <ul class="checklist"><li>Grade-level standards from Kindergarten to 12th Grade</li><li>Annual state tests in Grades 3–8 and once in high school</li><li>High school credits, End-of-Course exams and AP/IB courses</li></ul>
      </div><div class="panel"><h3>Subjects we tutor</h3><div class="chip-list">{''.join(a(f"{CUR}/{s[0]}", s[1], "chip") for s in SUBJECTS)}</div>
      <p class="muted mt">Math, English Language Arts and Science, including high school and AP Physics, Chemistry and Biology.</p></div></div>""")
    body += section(head("The main standards frameworks", "Frameworks") + table([
        ("Common Core State Standards (CCSS)", "Math & ELA, K–12", "Most states, often renamed or revised locally"),
        ("Next Generation Science Standards (NGSS)", "Science, K–12", "Adopted or adapted by most states"),
        ("Texas Essential Knowledge and Skills (TEKS)", "All subjects", "Texas"),
        ("Florida B.E.S.T. Standards", "Math & ELA", "Florida"),
        ("Virginia Standards of Learning (SOL)", "All subjects", "Virginia"),
        ("AP Course Frameworks", "College-level courses", "Nationwide (College Board)"),
    ], ["Framework", "Covers", "Used in"]), alt=True)
    body += section(head("Browse by grade level", "Grade levels", "See what's covered at each stage, and how we help.") + grade_chips(), attrs=" id=grades")
    body += section(head("Browse by state", "States", "Each state has its own standards and tests.") + state_chips() + f'<p class="mt">{a(f"{CUR}/states", "Compare standards & tests for all 50 states →", "more")}</p>', alt=True)
    body += cta()
    page("us-curriculum", "US Curriculum & State Standards Tutoring | Twinkle Tutor",
         "Online tutoring aligned with Common Core, NGSS and each state's standards, from TEKS to Florida B.E.S.T. and the Virginia SOLs, for Kindergarten to 12th Grade.", body)


def states_index():
    body = hero("All 50 states + DC", "Online tutoring in every US state",
                "Find your state's learning standards and annual test. Every tutor is matched to the standards your child is taught at school.",
                crumb=crumbs((CUR, "US Curriculum"), "States"))
    for i, r in enumerate(REGIONS):
        rows = [(a(f"{CUR}/{s[0]}", s[1]) + f" <span class='muted'>({s[2]})</span>", e(s[4]), e(s[5])) for s in STATES if s[3] == r]
        body += section(head(f"{r}", "Region") + table(rows, ["State", "Learning standards", "State test"]), alt=i % 2 == 1)
    body += section('<p class="muted">Standards and test names change from time to time. Check your state department of education for the latest details, and tell us your district when you book so we can match your class syllabus.</p>')
    body += cta()
    page("us-curriculum/states", "Tutoring by State: Standards & Tests | Twinkle Tutor",
         "Learning standards and state tests for all 50 US states and DC, from STAAR and CAASPP to FAST, Regents and PSSA. Online tutoring matched to your state.", body)


def state_page(s):
    slug, name, abbr, region, standards, test = s
    special = {
        "new-york": ["shsat", "state-tests", "sat", "ap-exams"],
    }.get(slug, ["state-tests", "sat", "act", "ap-exams"])
    body = hero(f"{abbr} · State standards", f"Online tutoring in {e(name)}",
                f"Live 1-on-1 tutoring for {name} students from Kindergarten to 12th Grade, aligned with the {standards} and the {test.split(' (')[0]}.",
                points=[f"{abbr} standards-aligned", f"{test.split(' (')[0]} prep", "Flexible after-school times"],
                crumb=crumbs((CUR, "US Curriculum"), (f"{CUR}/states", "States"), name))
    body += section(head(f"How schooling works in {name}", "Curriculum") + f"""<div class="split"><div>
      <p class="lead">{e(name)} students learn to the {e(standards)}. Students in Grades 3–8 and in high school take the {e(test)}.</p>
      <p>Our {e(name)} tutors know the standards, the question types and the testing calendar, so lessons support classwork, homework and tests.</p></div>
      <div>{table([("Learning standards", standards), ("State test", test), ("Region", region), ("Grades", "Kindergarten to 12th Grade"), ("College admissions", "SAT, ACT, AP")])}</div></div>""")
    body += section(head(f"Subjects for {name} students", "Subjects") + subject_cards(), alt=True)
    body += section(head(f"Test prep for {name} students", "Test prep") + exam_cards(special))
    body += section(head("Browse by grade", "Grades") + grade_chips(), alt=True)
    others = [x for x in STATES if x[3] == region and x[0] != slug]
    body += section(head(f"Other {region} states", "Nearby") + state_chips(others))
    body += cta(f"Try a free lesson with a {name} tutor")
    page(f"us-curriculum/{slug}", f"Online Tutoring in {name} ({abbr}) | Twinkle Tutor",
         f"Live 1-on-1 online tutoring for {name} students, K–12, aligned with {abbr} standards and state tests, plus SAT & ACT prep. Book a free trial.", body)


def grade_page(g):
    slug, label, stage, ages, note, maths, ela, sci = g
    subj = {s[1]: s for s in SUBJECTS}
    cols = [("Math", "π", "t-blue", maths, "online-math-tutor"), ("English", "Aa", "t-pink", ela, "online-english-tutor"), ("Science", "Sc", "t-green", sci, "online-science-tutor")]
    cards = "".join(f'<div class="card"><div class="tile {t}">{i}</div><h3>{n}</h3><ul>' + "".join(f"<li>{e(x)}</li>" for x in items) + f'</ul>{a(f"{CUR}/{u}", f"{n} tutoring →", "more")}</div>' for n, i, t, items, u in cols)
    idx = GRADES.index(g)
    if idx <= 2:
        tests = []
    elif idx <= 8:
        tests = ["state-tests", "isee", "ssat"] + (["shsat"] if idx == 8 else [])
    elif idx == 9:
        tests = ["state-tests", "psat", "ap-exams"]
    else:
        tests = ["sat", "act", "psat", "ap-exams"] if idx < 12 else ["sat", "act", "ap-exams", "state-tests"]
    body = hero(f"{stage} · Ages {ages}", f"{e(label)} online tutoring",
                f"What {label} students learn in Math, English and Science, and how a 1-on-1 tutor can help them stay ahead.",
                ctas=[(f"{B}/free-trial", f"Free {label} trial"), (f"{B}/pricing", "See pricing")], points=[note],
                crumb=crumbs((CUR, "US Curriculum"), label))
    body += section(head(f"Key focus areas in {label}", "Curriculum", "Aligned with Common Core, NGSS and your state's standards.") + f'<div class="grid g3">{cards}</div>', alt=True)
    if tests:
        body += section(head(f"Tests in {label}", "Test prep") + exam_cards(tests))
    body += section(head("Other grades", "Grade levels") + grade_chips(), alt=not tests)
    body += cta()
    page(f"us-curriculum/{slug}", f"{label} Online Tutoring | Twinkle Tutor",
         f"Live 1-on-1 {label} tutoring in Math, English and Science, aligned with Common Core and your state's standards. Book a free trial.", body)


def subject_page(s):
    slug, name, icon, tile, blurb, standards, bands, strands = s
    body = hero(f"Online {name} Tutor", f"Online {e(name)} tutoring, K–12",
                f"Our {name.lower()} tutors follow the {standards}. We find the gaps, rebuild the foundations, then stretch students with problem-solving and reasoning.",
                ctas=[(f"{B}/free-trial?subject={quote(name)}", f"Free {name} trial"), (f"{B}/pricing", "See pricing")],
                points=["Specialist tutors", "Standards-aligned", "Lesson notes for parents"],
                crumb=crumbs((CUR, "US Curriculum"), f"{name} Tutor"),
                aside=lesson_card(f"{name} lesson", blurb), compact=False)
    body += section(head(f"What our {name} tutors cover", "Topics", "Lessons follow your child's class — or target the gaps that matter most.") +
                    '<div class="grid g3">' + "".join(f'<div class="card"><h3>{e(t)}</h3><ul>' + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul></div>" for t, items in bands) + "</div>", alt=True)
    approach = [("Diagnose", "A short assessment shows exactly where your child is and where the gaps are."),
                ("Plan", "A personalized plan mapped to their grade and state standards."),
                ("Teach & practice", "Clear explanations, worked examples and guided practice in every lesson."),
                ("Review", "Regular check-ins and reports so you can see progress.")]
    body += section(f"""<div class="split"><div>
        <h2>Our approach to {e(name)}</h2>
        <p class="lead">Every session is 1-on-1, so your tutor can move at your child's pace and focus on what will make the biggest difference.</p>
        <h3 class="mt">Key domains</h3><div class="chip-list">{''.join(f'<span class="chip">{e(x)}</span>' for x in strands)}</div>
      </div><div class="grid g2 steps">{''.join(f'<div class="card step"><h3>{e(h)}</h3><p>{e(p)}</p></div>' for h, p in approach)}</div></div>""")
    body += section(head("By grade level") + f'<p class="muted">Pick a grade to see {name} focus areas:</p>' + grade_chips(), alt=True)
    body += cta(f"Try a free {name} lesson")
    page(f"us-curriculum/{slug}", f"Online {name} Tutor | K–12, AP & SAT/ACT | Twinkle Tutor",
         f"Live 1-on-1 online {name.lower()} tutoring for US students, Kindergarten to 12th Grade. Aligned with Common Core/NGSS and state standards. Book a free trial.", body)


def exam_page(x):
    slug, name, full, tag, grades, overview, fmt, checklist = x
    aside = f"""<div class="hero-card"><h3>{e(name)}</h3><div class="sub">{e(full)}</div>
                  <ul class="checklist">{''.join(f'<li>{e(c)}</li>' for c in checklist)}</ul>
                  <a class="btn btn-primary" style="width:100%" href="{B}/free-trial?exam={quote(name)}">Get a free diagnostic</a></div>"""
    body = hero(f"Test prep · {grades} · {tag}", f"{e(name)} prep &amp; tutoring",
                f"Expert {name} tutors who know the format, the question types and the strategies that raise scores.",
                ctas=[(f"{B}/free-trial?exam={quote(name)}", f"Start {name} prep"), (f"{B}/pricing", "Test Prep plan")],
                crumb=crumbs("Test Prep", name), aside=aside, compact=False)
    body += section(head(f"About the {name}", "Overview") + f'<div class="prose" style="margin:0;max-width:820px"><p class="lead">{e(overview)}</p></div>')
    body += section(head("What's tested", "Format") + '<div class="grid g4">' + "".join(f'<div class="card"><h3>{e(h)}</h3><p>{e(p)}</p></div>' for h, p in fmt) + "</div>", alt=True)
    plan = ["Diagnostic & target score", "Weekly skill-building sessions", "Timed practice & review", "Final mock test & test-day plan"]
    body += section(head(f"Our {name} prep plan", "How we help", "A structured program that builds skills first, then speed and test-day confidence.") +
                    '<div class="grid g4 steps">' + "".join(f'<div class="card step"><h3>{e(p)}</h3></div>' for p in plan) + "</div>")
    if slug == "state-tests":
        rows = [(a(f"{CUR}/{s[0]}", s[1]), e(s[5])) for s in STATES]
        body += section(head("State tests by state", "All 50 states + DC") + table(rows, ["State", "Annual test"]), alt=True)
    body += section(head("Other test prep", "More exams") + exam_cards([y[0] for y in EXAMS if y[0] != slug]), alt=slug != "state-tests")
    body += cta(f"Start {name} prep with a free lesson")
    page(f"test-prep/{slug}", f"{name} Prep & Tutoring Online | Twinkle Tutor",
         f"1-on-1 online {name} tutoring with a diagnostic, a personalized plan and full-length practice. Book a free trial.", body)


PLANS = [
    ("Flex", "Pay as you go, one session at a time.", 59, 54, ["1 x 60-min session per week", "Matched, background-checked tutor", "Lesson notes after every session", "Reschedule with 24h notice"], False),
    ("Progress", "Our most popular plan for steady improvement.", 52, 47, ["2 x 60-min sessions per week", "Personalized learning plan", "Monthly progress report", "Homework & test help", "Priority tutor matching"], True),
    ("Test Prep", "For state tests, SHSAT, SAT, ACT & AP goals.", 49, 44, ["3+ sessions per week", "Full-length practice tests", "Test strategy coaching", "Biweekly parent check-ins", "Summer & break intensives"], False),
]


def pricing():
    plans = ""
    for n, note, w, t, items, feat in PLANS:
        plans += f"""<div class="plan{' featured' if feat else ''}">
      {'<span class="badge">Most popular</span>' if feat else ''}
      <h3>{n}</h3><p class="note">{e(note)}</p>
      <div class="price">$<span data-weekly="{w}" data-term="{t}">{w}</span><small data-unit>/session</small></div>
      <p class="note">60-minute 1-on-1 session · USD</p>
      <ul class="checklist">{''.join(f'<li>{e(i)}</li>' for i in items)}</ul>
      <a class="{'btn btn-primary' if feat else 'btn btn-ghost'}" href="{B}/free-trial?plan={quote(n)}">{'Choose' if feat else 'Start with'} {n}</a></div>"""
    body = hero("Simple, transparent pricing", "Pricing that fits your family",
                "No long-term contracts and no sign-up fees. Start with a free trial lesson, and choose a plan only if it's the right fit.",
                ctas=[], crumb=crumbs("Pricing"))
    body += f"""<section class="section" style="padding-top:20px"><div class="container center">
      <div class="toggle" data-billing data-term-unit="/session, paid per semester"><button class="on" data-mode="weekly" type="button">Pay as you go</button><button data-mode="term" type="button">Pay per semester (save ~9%)</button></div>
      <div style="text-align:left"><div class="plans">{plans}</div></div></div></section>"""
    body += section(head("Compare plans", center=True) + table([
        ("1-on-1 live lessons", "✓", "✓", "✓"), ("Lesson notes", "✓", "✓", "✓"), ("Personalized learning plan", "—", "✓", "✓"),
        ("Progress reports", "—", "Monthly", "Biweekly"), ("Practice tests & scoring", "—", "—", "✓"), ("Sessions per week", "1", "2", "3+")],
        ["Feature", "Flex", "Progress", "Test Prep"]), alt=True)
    body += section(head("Pricing FAQs", center=True) + faq([
        ("Is there a sign-up fee?", "No. You only pay for sessions."),
        ("Can I switch plans?", "Yes, you can switch plans at any time."),
        ("What does 'pay per semester' mean?", "You prepay a semester of sessions at a lower rate per session. Unused sessions are covered by our Refund Policy."),
        ("Do you offer sibling discounts?", "Yes. Contact us for family pricing for two or more students."),
        ("Can I use an HSA, 529 or ESA?", "Some states' education savings accounts and scholarship programs cover tutoring. Contact us and we'll help with the paperwork.")]))
    body += cta()
    page("pricing", "Online Tutoring Prices (USD) | Twinkle Tutor",
         "Simple pricing for 1-on-1 online tutoring in the US. Pay as you go or per semester, with no contracts. Free trial lesson.", body)


GRADE_OPTS = "".join(f"<option>{g[1]}</option>" for g in GRADES)
STATE_OPTS = "".join(f"<option>{s[1]}</option>" for s in STATES)


def free_trial():
    subj_opts = "".join(f'<option value="{s[1]}">{s[1]}</option>' for s in SUBJECTS) + "".join(f'<option value="{x[1]}">{x[1]} prep</option>' for x in EXAMS)
    form = f"""<form class="form panel" name="free-trial-us" method="POST"{FORM_ATTRS} data-netlify="true" netlify-honeypot="bot-field" data-demo-form novalidate id="trial"><input type="hidden" name="form-name" value="free-trial-us"><p hidden><label>Leave empty <input name="bot-field"></label></p>
      <div class="form-success">🎉 You're booked in! We'll call or email within one business day to match your tutor and confirm a time.</div>
      <div class="form-fields form">
        <h3 style="margin:0">Book your free lesson</h3>
        <div class="row"><div><label for="t-parent">Parent / guardian name</label><input id="t-parent" name="parent" required autocomplete="name"></div>
          <div><label for="t-student">Student's first name</label><input id="t-student" name="student" required></div></div>
        <div class="row"><div><label for="t-email">Email</label><input id="t-email" name="email" type="email" required autocomplete="email"></div>
          <div><label for="t-phone">Phone</label><input id="t-phone" name="phone" type="tel" required autocomplete="tel"></div></div>
        <div class="row"><div><label for="t-year">Grade</label><select id="t-year" name="grade" required><option value="">Select…</option>{GRADE_OPTS}</select></div>
          <div><label for="t-state">State</label><select id="t-state" name="state" required><option value="">Select…</option>{STATE_OPTS}</select></div></div>
        <div><label for="trial-subject">Subject or test</label><select id="trial-subject" name="subject" required><option value="">Select…</option>{subj_opts}</select></div>
        <div><label for="t-goal">What would you like help with? (optional)</label><textarea id="t-goal" name="goal" placeholder="e.g. building confidence with fractions, raising an SAT score…"></textarea></div>
        <label class="check"><input type="checkbox" required> I agree to the <a href="{B}/terms-and-conditions">Terms</a> and <a href="{B}/privacy">Privacy Policy</a>.</label>
        <button class="btn btn-primary" type="submit">Book my free trial</button>
        <p class="muted" style="font-size:.85rem;margin:0">No payment details required.</p>
      </div></form>"""
    body = hero("Free trial lesson", "Try a free 1-on-1 lesson",
                "Meet a specialist tutor, get a personalized learning plan and try our online classroom, free and with no obligation.",
                ctas=[], points=["60-minute lesson", "Personalized learning plan", "No payment details needed"],
                crumb=crumbs("Free Trial"), aside=form, compact=False)
    body += section(head("What happens next", center=True) + steps(), alt=True)
    page("free-trial", "Book a Free Online Tutoring Lesson | Twinkle Tutor",
         "Book a free 60-minute 1-on-1 online tutoring lesson for any K–12 student in the US. No payment details needed.", body)


def contact():
    form = f"""<form class="form panel" name="contact-us" method="POST"{FORM_ATTRS} data-netlify="true" netlify-honeypot="bot-field" data-demo-form novalidate><input type="hidden" name="form-name" value="contact-us"><p hidden><label>Leave empty <input name="bot-field"></label></p>
      <div class="form-success">Thanks! We'll get back to you within one business day.</div>
      <div class="form-fields form">
        <h3 style="margin:0">Send us a message</h3>
        <div class="row"><div><label for="c-name">Name</label><input id="c-name" name="name" required autocomplete="name"></div>
          <div><label for="c-email">Email</label><input id="c-email" name="email" type="email" required autocomplete="email"></div></div>
        <div><label for="c-state">State</label><select id="c-state" name="state"><option value="">Select…</option>{STATE_OPTS}</select></div>
        <div><label for="c-msg">Message</label><textarea id="c-msg" name="message" required></textarea></div>
        <button class="btn btn-primary" type="submit">Send message</button>
      </div></form>"""
    body = hero("Contact us", "We're here to help",
                f"Questions about tutoring, pricing or your state's standards? Email {EMAIL} or send us a message.",
                ctas=[], points=["Mon–Fri 9am–8pm ET", "Sat 10am–4pm ET", "Reply within 1 business day"],
                crumb=crumbs("Contact"), aside=form, compact=False)
    body += section(head("Common questions", center=True) + faq(MAIN_FAQ), alt=True)
    page("contact-us", "Contact Us | Twinkle Tutor", "Contact Twinkle Tutor about online tutoring for US students. Email us or send a message.", body)


def about():
    body = hero("About Twinkle Tutor", "Great tutoring, wherever you live",
                "We match US students with expert tutors for live, 1-on-1 lessons online. Every lesson is personal, aligned with the student's standards and focused on real progress.",
                crumb=crumbs("About"))
    body += section(head("What we believe", "Our values") + '<div class="grid g3">' + "".join(
        f'<div class="card"><h3>{e(h)}</h3><p>{e(p)}</p></div>' for h, p in [
            ("1-on-1 works", "Personal attention is the fastest way to close gaps and build confidence."),
            ("Standards matter", "Lessons line up with your state's standards and your child's class, so the gains carry over to report cards and tests."),
            ("Parents in the loop", "Lesson notes after every session and regular progress reports.")]) + "</div>", alt=True)
    body += section(head("Our tutors", "Quality") + '<ul class="checklist">' + "".join(f"<li>{e(x)}</li>" for x in [
        "College degree, with many certified teachers and subject specialists", "Criminal background check before teaching",
        "Interviewed, trained and observed", "Specialists in state tests, SAT/ACT and AP"]) + "</ul>")
    body += cta()
    page("about", "About Us | Twinkle Tutor", "Twinkle Tutor provides live 1-on-1 online tutoring for K–12 students in all 50 US states.", body)


def legal(slug, title, paras):
    body = hero("Legal", e(title), f"Last updated October 2026.", ctas=[], crumb=crumbs(title))
    body += section('<div class="prose">' + "".join(f"<h3>{e(h)}</h3><p>{e(p)}</p>" for h, p in paras) + "</div>")
    page(slug, f"{title} | Twinkle Tutor", f"{title} for Twinkle Tutor's US online tutoring services.", body)


def extras():
    """404 page, sitemap and robots.txt for the live site."""
    body = hero("Page not found", "We couldn't find that page", "The link may be old or mistyped. Try the home page, or find your state.",
                ctas=[(B, "Go to the home page"), (f"{CUR}/states", "Find your state")])
    page("404", "Page Not Found | Twinkle Tutor", "This page could not be found.", body)
    tmp = ROOT / "us" / "404" / "index.html"
    html = re.sub(r'<link rel="canonical"[^>]*>', '<meta name="robots" content="noindex">', tmp.read_text())
    (ROOT / "404.html").write_text(html)
    tmp.unlink()
    tmp.parent.rmdir()
    urls = sorted(f"{SITE}/" + str(f.parent.relative_to(ROOT)) for f in (ROOT / "us").rglob("index.html"))
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
                                      "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    (ROOT / "CNAME").write_text(DOMAIN + "\n")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")


def build():
    home(); curriculum(); states_index()
    for s in STATES: state_page(s)
    for g in GRADES: grade_page(g)
    for s in SUBJECTS: subject_page(s)
    for x in EXAMS: exam_page(x)
    pricing(); free_trial(); contact(); about()
    legal("privacy", "Privacy Policy", [
        ("What we collect", "Contact details you give us, information about the student's grade and goals, and lesson records."),
        ("How we use it", "To match tutors, run lessons, send progress updates and improve our service. We never sell personal information."),
        ("Children's privacy", "We collect student information only with a parent or guardian's consent, in line with COPPA."),
        ("Your choices", "You can ask us to see, correct or delete your data at any time by emailing " + EMAIL + ".")])
    legal("refund", "Refund Policy", [
        ("Cancellations", "Sessions canceled with at least 24 hours' notice can be rescheduled or refunded."),
        ("Semester plans", "Unused prepaid sessions are refunded pro rata, minus the discount applied."),
        ("Satisfaction", "If a lesson doesn't meet your expectations, tell us within 7 days and we'll make it right.")])
    legal("terms-and-conditions", "Terms & Conditions", [
        ("Services", "Twinkle Tutor provides live online tutoring sessions under the plan you choose."),
        ("Payments", "Prices are in US dollars. Sales tax is added where it applies."),
        ("Conduct", "Students and tutors must behave respectfully. Sessions may be recorded for quality and safety."),
        ("Changes", "We may update these terms and will tell you about any material changes.")])
    (ROOT / "index.html").write_text('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=/us"><link rel="canonical" href="/us"><a href="/us">Continue</a>')
    extras()
    print(len(list((ROOT / "us").rglob("index.html"))), "pages built")


if __name__ == "__main__":
    build()
