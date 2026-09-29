"""Build the static research-note pages and the Insights index for atuliwale.com.

Run: python3 tools/insights/build.py  (content lives in posts_a/b/c.py and evidence.py)

Head, header, bottom CTA and footer are lifted from the existing blog.html so the
new pages share the site's navigation and assets exactly.
"""
import hashlib, html, re, sys, os
sys.path.insert(0, os.path.dirname(__file__))

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'website')

def c(*ns):
    """Numbered citation link(s) to the sources list."""
    return ''.join(f'<sup><a href="#s{n}" aria-label="Source {n}">[{n}]</a></sup>' for n in ns)

def bars(title, rows, caption, unit='', max_value=None, reveal=True):
    """Horizontal bar chart. rows: (label, value, display, highlight)."""
    mx = max_value or max(r[1] for r in rows)
    items = ''.join(
        f'<li class="ins-bar{" ins-bar--hi" if hi else ""}"><span class="ins-bar-label">{html.escape(lbl)}</span>'
        f'<span class="ins-bar-track"><span class="ins-bar-fill" style="--w:{max(1.5, v / mx * 100):.1f}%"></span></span>'
        f'<span class="ins-bar-val">{disp}</span></li>'
        for lbl, v, disp, hi in rows)
    dr = ' data-reveal' if reveal else ''
    return (f'<figure class="ins-chart"{dr}><p class="rd-label">Figure</p><p class="ins-chart-title">{title}</p>'
            f'<ul class="ins-bars" role="list">{items}</ul><figcaption>{caption}</figcaption></figure>')

def table(head, rows, caption, num_cols=()):
    th = ''.join(f'<th scope="col"{" class=num" if i in num_cols else ""}>{h}</th>' for i, h in enumerate(head))
    body = ''.join('<tr>' + ''.join(f'<td{" class=num" if i in num_cols else ""}>{v}</td>' for i, v in enumerate(r)) + '</tr>' for r in rows)
    return (f'<div class="ins-table-wrap" data-reveal><table class="ins-table"><caption>{caption}</caption>'
            f'<thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>')

def pull(text):
    return f'<blockquote class="ins-pull" data-reveal><p>{text}</p></blockquote>'

def callout(label, *paras):
    ps = ''.join(f'<p>{p}</p>' for p in paras)
    return f'<aside class="ins-callout" data-reveal><p class="rd-label">{label}</p>{ps}</aside>'

def checklist(items):
    return '<ol class="ins-check">' + ''.join(f'<li><span>{i}</span></li>' for i in items) + '</ol>'

# ---------------------------------------------------------------- page chrome
TEMPLATE = os.path.join(os.path.dirname(__file__), 'blog_template.html')

def chrome():
    if not os.path.exists(TEMPLATE):  # keep the original React-rendered page as the chrome source
        open(TEMPLATE, 'w').write(open(f'{SITE}/blog.html').read())
    s = open(TEMPLATE).read()
    head = s[:s.find('</head>')]
    head = re.sub(r'<script type="module"[^>]*></script>', '', head)
    body = s[s.find('<body'):]
    pre_main = body[body.find('<a class="skip"'):body.find('<main')]
    post = body[body.find('</main>') + 7:]
    cta = post[:post.find('<footer')]
    footer = post[post.find('<footer'):post.find('</footer>') + 9]
    return head, pre_main, cta, footer

def vhash(rel):
    return hashlib.sha256(open(f'{SITE}/{rel}', 'rb').read()).hexdigest()[:12]

def set_head(head, title, desc, url):
    t = html.escape(title, quote=True); d = html.escape(desc, quote=True)
    head = re.sub(r'<title>.*?</title>', f'<title>{t} — Atul Iwale</title>', head, flags=re.S)
    for prop in ('og:title', 'twitter:title'):
        head = re.sub(rf'(<meta (?:property|name)="{prop}" content=")[^"]*', rf'\g<1>{t}', head)
    for prop in ('description', 'og:description', 'twitter:description'):
        head = re.sub(rf'(<meta (?:property|name)="{prop}" content=")[^"]*', rf'\g<1>{d}', head)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*', rf'\g<1>https://atuliwale.com/{url}', head)
    head = re.sub(r'(<link rel="canonical" href=")[^"]*', rf'\g<1>https://atuliwale.com/{url}', head)
    # refresh every local asset version from the files on disk (the template may be older)
    head = re.sub(r'(/((?:assets|react)/[^"?]+))\?v=[0-9a-f]+', lambda m: f'{m.group(1)}?v={vhash(m.group(2))}', head)
    extra = (f'<link rel="stylesheet" href="/assets/redesign/insight.css?v={vhash("assets/redesign/insight.css")}">'
             f'<script defer src="/assets/redesign/home.js?v={vhash("assets/redesign/home.js")}"></script>'
             f'<script defer src="/assets/redesign/insight.js?v={vhash("assets/redesign/insight.js")}"></script>')
    return head + extra

def words(htmltext):
    return len(re.sub(r'<[^>]+>', ' ', htmltext).split())

# ---------------------------------------------------------------- article
def article(p, allposts):
    head, pre_main, cta, footer = chrome()
    body_html = ''.join(sec[2] for sec in p['sections'])
    minutes = max(4, round((words(body_html) + words(''.join(p['takeaways']))) / 220))
    p['minutes'] = minutes
    keys = ''.join(
        f'<div class="ins-key" data-reveal><dt>{k[0]}</dt><dd>{k[1]}{c(k[2]) if k[2] else ""}</dd></div>' for k in p['keys'])
    toc = ''.join(f'<li><a href="#{sid}">{html.escape(t)}</a></li>' for sid, t, _ in p['sections']) + \
          '<li><a href="#sources">Sources</a></li>'
    secs = ''.join(
        f'<h2 id="{sid}"><span class="ins-h2-no">{i:02d}</span>{t}</h2>{b}' for i, (sid, t, b) in enumerate(p['sections'], 1))
    take = ''.join(f'<li>{t}</li>' for t in p['takeaways'])
    a = p['applied']
    applied = (f'<section class="ins-applied" data-reveal aria-label="From my work"><p class="rd-label">From my work</p>'
               f'<h3>{a["title"]}</h3>' + ''.join(f'<p>{x}</p>' for x in a['text']) +
               f'<a class="ins-link" href="{a["href"]}"{" target=_blank rel=noopener" if a["href"].startswith("http") else ""}>{a["label"]} <span class="ins-arrow" aria-hidden="true">→</span></a></section>')
    srcs = ''.join(f'<li id="s{i}"><span>{s}</span></li>' for i, s in enumerate(p['sources'], 1))
    nxt = ''.join(
        f'<a href="/{q["slug"]}.html"><span class="rd-label">{q["topic"]}</span><strong>{q["title"]}</strong></a>'
        for q in (next(x for x in allposts if x['slug'] == s) for s in p['next']))
    date_label = p['date_label']
    main = f'''<main id="main" class="ins">
<article>
<header class="ins-hero rd-wrap">
<a class="ins-link ins-link--back" href="/blog.html"><span class="ins-arrow" aria-hidden="true">←</span> All insights</a>
<p class="rd-label ins-kicker">{p["topic"]} <span>×</span> Research note</p>
<h1 class="ins-title">{p["title"]}</h1>
<p class="ins-dek">{p["dek"]}</p>
<ul class="ins-meta"><li>{minutes} min read</li><li>{len(p["sources"])} sources</li><li><time datetime="{p["date"]}">{date_label}</time></li><li>Atul Iwale</li></ul>
</header>
<div class="rd-wrap"><dl class="ins-keys">{keys}</dl></div>
<div class="ins-body rd-wrap">
<nav class="ins-toc" aria-label="On this page"><p class="rd-label">On this page</p><ol>{toc}</ol></nav>
<div class="ins-prose">
<section class="ins-takeaways" aria-label="Key takeaways"><p class="rd-label">Key takeaways</p><ul>{take}</ul></section>
{secs}
{applied}
<h2 id="sources"><span class="ins-h2-no">Notes</span>Sources</h2>
<ol class="ins-sources">{srcs}</ol>
<p class="ins-note">Figures are quoted from the sources above as published; where a source reports a range or a survey estimate, it is described that way. Results from my own projects say whether they use real public data or synthetic data.</p>
</div>
</div>
<nav class="ins-next rd-wrap" aria-label="Keep reading"><p class="rd-label">Keep reading</p><div class="ins-next-grid">{nxt}</div></nav>
</article>
</main>'''
    ld = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"Article",'
          f'"headline":{json_str(p["title"])},"description":{json_str(p["dek"])},"datePublished":"{p["date"]}",'
          '"author":{"@type":"Person","name":"Atul Iwale","url":"https://atuliwale.com/"},'
          f'"mainEntityOfPage":"https://atuliwale.com/{p["slug"]}.html"}}</script>')
    h = set_head(head, re.sub(r'<[^>]+>', '', p['title']), p['meta'], f'{p["slug"]}.html')
    pre = pre_main.replace(' aria-current="page"', '')
    pre = pre.replace('<a href="/blog.html">Insights</a>', '<a href="/blog.html" aria-current="page">Insights</a>')
    pre = pre.replace('<a href="/blog.html"><span class="menu-number">04</span>', '<a href="/blog.html" aria-current="page"><span class="menu-number">04</span>')
    foot = footer
    return (f'{h}{ld}</head><body id="top" class="writing inner-page rd-page">{pre}{main}{cta}{foot}</body></html>')

def json_str(s):
    import json
    return json.dumps(re.sub(r'<[^>]+>', '', s))

# ---------------------------------------------------------------- index
EXISTING = [
    dict(slug='insight-erp-adoption', topic='Digital adoption', topics='adoption', title='Why ERP adoption fails on site — and what to do differently',
         blurb='The gap between configured systems and everyday site workflows, including training and user adoption.', kind='Field note'),
    dict(slug='insight-procurement-data', topic='Procurement', topics='commercial', title='Turning procurement data into project intelligence',
         blurb='Connecting purchase orders, supplier records and material requirements to practical project decisions.', kind='Field note'),
    dict(slug='insight-aec-ai', topic='AI & automation', topics='ai', title='Where AI genuinely helps in AEC operations — and where it’s still hype',
         blurb='Useful AEC applications for AI, the information they depend on and where human judgment remains essential.', kind='Field note'),
]
FILTERS = [('all', 'All'), ('controls', 'Cost & controls'), ('data', 'Data & productivity'), ('safety', 'Safety'),
           ('ai', 'AI & automation'), ('commercial', 'Commercial'), ('adoption', 'Adoption')]

def index(posts):
    head, pre_main, cta, footer = chrome()
    feat = posts[0]
    cards = []
    for p in posts:
        cards.append(f'''<a class="ins-card" href="/{p["slug"]}.html" data-topics="{p["topics"]}" data-reveal>
<span class="rd-label">{p["topic"]} · Research note</span><h2>{p["title"]}</h2><p>{p["blurb"]}</p>
<span class="ins-card-meta"><span>{p["minutes"]} min · {len(p["sources"])} sources</span><span class="ins-arrow" aria-hidden="true">→</span></span></a>''')
    for e in EXISTING:
        cards.append(f'''<a class="ins-card" href="/{e["slug"]}.html" data-topics="{e["topics"]}" data-reveal>
<span class="rd-label">{e["topic"]} · {e["kind"]}</span><h2>{e["title"]}</h2><p>{e["blurb"]}</p>
<span class="ins-card-meta"><span>Short read</span><span class="ins-arrow" aria-hidden="true">→</span></span></a>''')
    filt = ''.join(f'<button type="button" data-topic="{k}" aria-pressed="{"true" if k == "all" else "false"}">{v}</button>' for k, v in FILTERS)
    total = len(posts) + len(EXISTING)
    main = f'''<main id="main" class="ins">
<header class="ins-index-hero rd-wrap">
<p class="rd-label ins-kicker">Insights <span>×</span> Research notes</p>
<h1 class="ins-title">What the evidence says about building better.</h1>
<p class="ins-dek">Research notes on construction cost, safety, data and AI: what published studies and public data actually show, what it means on a project, and where I have tested the idea in my own work. Every figure is linked to its source.</p>
<ul class="ins-meta"><li>{len(posts)} research notes</li><li>{len(EXISTING)} field notes</li><li>{sum(len(p["sources"]) for p in posts)} cited sources</li></ul>
</header>
<section class="rd-wrap" aria-label="Featured note">
<a class="ins-feature" href="/{feat["slug"]}.html" data-reveal>
<div><p class="rd-label" style="color:var(--sage)!important">Featured · {feat["topic"]}</p><h2 class="ins-title">{feat["title"]}</h2><p>{feat["blurb"]}</p>
<span class="ins-link">Read the note <span class="ins-arrow" aria-hidden="true">→</span></span></div>
<div class="ins-feature-stat"><b>{feat["feature_stat"][0]}</b><span>{feat["feature_stat"][1]}</span></div></a>
</section>
<section class="rd-wrap" aria-labelledby="all-notes">
<div class="ins-sub"><div><p class="rd-label">Library</p><h2 id="all-notes">All notes</h2></div><p><span data-ins-count>{total} notes</span> · filter by topic</p></div>
<div class="ins-filters" role="group" aria-label="Filter notes by topic" style="margin-top:22px">{filt}</div>
<div class="ins-grid">{"".join(cards)}</div>
</section>
</main>'''
    h = set_head(head, 'Insights & research notes', 'Research notes on construction cost, safety, data and AI, with every figure linked to its source.', 'blog.html')
    return f'{h}</head><body id="top" class="writing inner-page rd-page">{pre_main}{main}<div style="height:clamp(56px,6vw,96px)"></div>{cta}{footer}</body></html>'

if __name__ == '__main__':
    from posts_a import POSTS as A
    from posts_b import POSTS as B
    from posts_c import POSTS as C
    posts = A + B + C
    from evidence import EVIDENCE
    for p in posts:  # insert the evidence grading just before the practical checklist
        if not any(sid == 'evidence' for sid, _, _ in p['sections']):
            p['sections'].insert(len(p['sections']) - 1, ('evidence', 'How strong is the evidence?', EVIDENCE[p['slug']]))
    for p in posts:
        out = article(p, posts)
        open(f'{SITE}/{p["slug"]}.html', 'w').write(out)
        print(p['slug'], p['minutes'], 'min', words(''.join(s[2] for s in p['sections'])), 'words', len(p['sources']), 'sources')
    open(f'{SITE}/blog.html', 'w').write(index(posts))
    print('blog.html written')
