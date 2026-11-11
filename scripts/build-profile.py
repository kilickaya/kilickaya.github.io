#!/usr/bin/env python3
"""Generate crawler-readable profile exports from the visible HTML. Standard library only.

Run after editing site content; use --check to detect stale generated output.
"""
import argparse
import calendar
import html
import json
import re
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://kilickaya.github.io/'
BEGIN = '<!-- Generated research metadata: scripts/build-profile.py -->'
END = '<!-- End generated research metadata -->'
TOPICS = [
    ('Autonomous vision', r'autonomous vision'),
    ('Data curation', r'curate their own data'),
    ('Self-supervised visual representation learning', r'self-supervised visual representation learning'),
    ('Continual learning', r'continual'),
    ('Efficient adaptation', r'adapt(?:ing)? efficiently'),
    ('Multimodal and vision-language learning', r'multimodal|vision-language'),
    ('Applied computer vision', r'applied AI|applied computer vision'),
]
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}


def clean(value):
    return re.sub(r'\s+', ' ', value).strip()


@dataclass
class Node:
    tag: str
    attrs: dict = field(default_factory=dict)
    children: list = field(default_factory=list)

    def text(self):
        return clean(''.join(c.text() if isinstance(c, Node) else c for c in self.children))

    def own_text(self):
        return clean(''.join(c for c in self.children if isinstance(c, str)))

    def all(self, tag=None, cls=None, id=None):
        found = []
        for child in self.children:
            if not isinstance(child, Node):
                continue
            if ((tag is None or child.tag == tag)
                    and (cls is None or cls in child.attrs.get('class', '').split())
                    and (id is None or child.attrs.get('id') == id)):
                found.append(child)
            found.extend(child.all(tag, cls, id))
        return found

    def first(self, tag=None, cls=None, id=None):
        matches = self.all(tag, cls, id)
        if not matches:
            raise ValueError(f'Missing HTML content: {tag=}, {cls=}, {id=}')
        return matches[0]


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.root = Node('document')
        self.stack = [self.root]
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        node = Node(tag, dict(attrs))
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def links(node):
    return [{'label': a.text(), 'url': urljoin(BASE, a.attrs['href'])} for a in node.all('a')]


def dates(label):
    months = {name.lower(): f'{i:02d}' for i, name in enumerate(calendar.month_name) if name}
    months.update({name.lower(): f'{i:02d}' for i, name in enumerate(calendar.month_abbr) if name})
    pattern = r'(?:(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+)?((?:19|20)\d{2})'
    found = re.findall(pattern, label, re.I)
    values = [year + ('-' + months[month.lower()] if month else '') for month, year in found]
    return values[0] if values else None, values[1] if len(values) > 1 else None


def read_profile(doc):
    bio = doc.first(id='bio')
    education = bio.first(cls='bio-education')
    supervisor = links(education)[-1]
    qualification = re.search(r'I completed my (.*?) at the (.*?)’s', education.text())
    if not qualification:
        raise ValueError('Update the education parser for the revised bio wording.')
    career = []
    for record in doc.first(id='experience').all('li', cls='career-row'):
        heading = record.first('h3')
        date_label = record.first(cls='career-date').text()
        start, end = dates(date_label)
        role = next(p.text() for p in record.all('p') if not p.attrs.get('class'))
        title, _, focus = role.partition(' · ')
        locations = heading.all('span')
        career.append({
            'organization': heading.own_text(),
            'roleTitle': title,
            'researchFocus': focus or None,
            'location': locations[0].text() if locations else None,
            'dateLabel': date_label,
            'startDate': start,
            'endDate': end,
            'current': 'present' in date_label.lower(),
            'links': links(record),
            'sourceURL': BASE + '#experience',
        })
    current = [r for r in career if r['current']]
    if len(current) != 1:
        raise ValueError('Exactly one current role is required.')

    papers = []
    for article in doc.first(id='research').all('article', cls='research-paper'):
        venue = article.first(cls='venue').text()
        image = article.first('img')
        papers.append({
            'id': article.attrs['id'],
            'title': article.first('h3').text(),
            'authors': [] if article.attrs.get('data-authors-complete') == 'false' else [a.strip() for a in article.first(cls='authors').text().split(',')],
            **({'authorNote': article.first(cls='authors').text()} if article.attrs.get('data-authors-complete') == 'false' else {}),
            'venue': venue,
            'year': int(re.search(r'\d{4}', venue)[0]),
            'description': article.first(cls='description').text(),
            'links': links(article.first(cls='text-links')),
            'illustrationURL': urljoin(BASE, image.attrs['src']),
            'sourceURL': BASE + '#' + article.attrs['id'],
        })

    news = []
    for item in doc.first(id='news').first(cls='news-list').all('li'):
        news.append({'date': item.first('time').attrs['datetime'],
                     'text': item.first('p').text(), 'links': links(item)})
    earlier = []
    for item in doc.first(id='earlier-news').all('li'):
        label = item.first(cls='news-date').text()
        month, year = label.split('/')
        earlier.append({'date': f'{year}-{month}', 'text': links(item)[0]['label'], 'links': links(item)})

    patents = []
    for record in doc.first(id='patents').all('article', cls='patent'):
        source = links(record.first(cls='patent-citation'))[0]
        patents.append({'title': record.first('h3').text(),
                        'authors': [a.strip() for a in record.first(cls='authors').text().split(',')],
                        'originalCitationLabel': source['label'], 'url': source['url']})
    people = []
    for record in doc.first(id='supervision').all('article', cls='person'):
        heading = record.first('h3')
        person, project = links(heading)[0], links(record.first('p'))[0]
        people.append({'name': person['label'], 'profileURL': person['url'],
                       'degreeAndInstitution': heading.own_text().strip('()'),
                       'period': record.first(cls='person-date').text(),
                       'project': project['label'], 'projectURL': project['url']})
    return {
        'name': doc.first('h1').text(),
        'identity': doc.first(cls='brand').first('span').text(),
        'researchGoal': bio.first(cls='intro-lead').text(),
        'researchOverview': doc.first(id='research').first(cls='section-heading').first('p').text(),
        'researchTopics': [name for name, pattern in TOPICS if re.search(pattern, bio.text() + ' ' + doc.first(id='research').first(cls='section-heading').text() + ' ' + doc.first(id='experience').text(), re.I)],
        'url': BASE,
        'imageURL': urljoin(BASE, bio.first('img').attrs['src']),
        'profiles': links(bio.first(cls='text-links')),
        'currentRole': current[0],
        'education': {'credential': qualification[1], 'institution': qualification[2],
                      'lab': links(education)[0]['label'], 'labURL': links(education)[0]['url'],
                      'supervisor': {'name': supervisor['label'], 'url': supervisor['url']},
                      'description': education.text()},
        'career': career,
        'news': news,
        'earlierNews': earlier,
        'publications': papers,
        'patents': patents,
        'mentorship': people,
        'photographyURL': BASE + 'images.html',
        'sourceNotes': [
            'Research goals describe a direction of work, not a claim of solved or deployed capabilities.',
            'Dates retain their available precision. A null endDate for a current role means ongoing; other null fields mean no value is supplied on the website.',
            'The linked CV was supplied by Mert on 11 November 2026.',
            'The ESMO 2026 abstract is linked to Agendia’s publication page. Its presenter is credited separately; the full author list and journal/DOI record are not supplied.',
            'The publication archive is the archive on this website, not a claim to include every subsequent work.',
            'Patent citation labels are preserved from the original archive and are not independently verified jurisdiction or grant dates.',
        ],
    }


def schema(profile, title):
    person_id = BASE + '#mert-kilickaya'
    person = {
        '@type': 'Person', '@id': person_id, 'name': profile['name'], 'url': BASE,
        'description': profile['researchGoal'], 'image': profile['imageURL'],
        'jobTitle': profile['currentRole']['roleTitle'],
        'worksFor': {'@type': 'Organization', 'name': profile['currentRole']['organization']},
        'alumniOf': {'@type': 'CollegeOrUniversity', 'name': profile['education']['institution']},
        'hasCredential': {'@type': 'EducationalOccupationalCredential',
                          'name': profile['education']['credential'], 'credentialCategory': 'Doctoral degree',
                          'description': profile['education']['description']},
        'knowsAbout': profile['researchTopics'],
        'sameAs': [p['url'] for p in profile['profiles'] if p['label'] in ['Google Scholar', 'LinkedIn']],
        'email': next(p['url'] for p in profile['profiles'] if p['url'].startswith('mailto:')).removeprefix('mailto:'),
        'mainEntityOfPage': {'@id': BASE + '#webpage'},
    }
    graph = [
        {'@type': 'WebSite', '@id': BASE + '#website', 'url': BASE,
         'name': profile['name'] + ' — ' + profile['identity'], 'author': {'@id': person_id}},
        {'@type': 'ProfilePage', '@id': BASE + '#webpage', 'url': BASE,
         'name': title, 'mainEntity': {'@id': person_id}, 'isPartOf': {'@id': BASE + '#website'}, 'inLanguage': 'en'},
        person,
    ]
    for p in profile['publications']:
        paper = {'@type': 'ScholarlyArticle', '@id': p['sourceURL'], 'headline': p['title'],
                 'author': [{'@id': person_id} if a == profile['name'] else {'@type': 'Person', 'name': a} for a in p['authors']],
                 'datePublished': str(p['year']), 'description': p['description'],
                 'url': p['links'][0]['url'], 'image': p['illustrationURL']}
        if not p['authors']:
            del paper['author']
        if p['venue'].startswith('Preprint'):
            paper['creativeWorkStatus'] = 'Preprint'
        else:
            paper['isPartOf'] = {'@type': 'CreativeWork', 'name': p['venue']}
        graph.append(paper)
    return {'@context': 'https://schema.org', '@graph': graph}


def markdown(profile):
    current, edu = profile['currentRole'], profile['education']
    out = [f"# {profile['name']}", f"> {profile['identity']}. {current['roleTitle']} at {current['organization']}.",
           profile['researchGoal'], profile['researchOverview'],
           f"Canonical website: {BASE}", '## Education', edu['description'],
           f"- Lab: [{edu['lab']}]({edu['labURL']})",
           f"- PhD supervisor: [{edu['supervisor']['name']}]({edu['supervisor']['url']})", '## Profiles & contact']
    out.extend(f"- [{p['label']}]({p['url']})" for p in profile['profiles'])
    out.append('## Experience')
    for r in profile['career']:
        out += [f"### {r['organization']}", f"{r['roleTitle']} · {r['dateLabel']}"]
        if r['researchFocus']:
            out.append('Research focus: ' + r['researchFocus'])
        if r['location']:
            out.append('Location: ' + r['location'])
        out.extend(f"- [{p['label']}]({p['url']})" for p in r['links'])
    out.append('## News')
    for n in profile['news'] + profile['earlierNews']:
        out.append(f"- **{n['date']}** — {n['text']}")
        out.extend(f"  - [{p['label']}]({p['url']})" for p in n['links'])
    out.append('## Research')
    for p in profile['publications']:
        out += [f"### {p['title']}", p.get('authorNote', ', '.join(p['authors'])), p['venue'], p['description']]
        out.extend(f"- [{l['label']}]({l['url']})" for l in p['links'])
        out.append(f"- [Publication on the website]({p['sourceURL']})")
    out.append('## Patents')
    for p in profile['patents']:
        out += [f"### {p['title']}", ', '.join(p['authors']),
                f"[{p['originalCitationLabel']}]({p['url']})"]
    out.append('## People & mentorship')
    for p in profile['mentorship']:
        out += [f"- [{p['name']}]({p['profileURL']}) — {p['degreeAndInstitution']}, {p['period']}. [{p['project']}]({p['projectURL']})"]
    out += ['## Beyond research', f"[Personal photography and visual memories]({profile['photographyURL']})", '## Source notes']
    out.extend('- ' + note for note in profile['sourceNotes'])
    return '\n\n'.join(out) + '\n'


def bibtex(profile):
    def esc(value):
        return value.replace('\\', r'\textbackslash{}').replace('{', r'\{').replace('}', r'\}').replace('&', r'\&').replace('%', r'\%').replace('_', r'\_').replace('#', r'\#')
    entries = []
    for p in profile['publications']:
        preprint = p['venue'].startswith('Preprint')
        key = 'kilickaya' + str(p['year']) + p['id'].removeprefix('publication-')
        fields = {'title': p['title'], 'author': ' and '.join(p['authors']), 'year': str(p['year'])}
        fields['howpublished' if preprint else 'booktitle'] = re.sub(r'\s*\(Oral\)$', '', p['venue'])
        if '(Oral)' in p['venue']:
            fields['note'] = 'Oral presentation'
        if not p['authors']:
            del fields['author']
            fields['note'] = p['authorNote'] + '; full author list unavailable in the linked source'
        fields['url'] = p['links'][0]['url']
        fields = ',\n'.join('  ' + k + ' = {' + (v if k == 'url' else '{' + esc(v) + '}' if k == 'title' else esc(v)) + '}' for k, v in fields.items())
        entries.append('@' + ('misc' if preprint else 'inproceedings') + '{' + key + ',\n' + fields + '\n}')
    return '% Exported from the publication metadata on https://kilickaya.github.io/\n% Venue names and year-only date precision follow the website.\n\n' + '\n\n'.join(entries) + '\n'


def metadata(source, canonical, image_url, graph=None):
    doc = Document(source).root
    title = doc.first('title').text()
    description = next(m.attrs['content'] for m in doc.all('meta') if m.attrs.get('name') == 'description')
    escape = lambda value: html.escape(value, quote=True)
    lines = [BEGIN, f'<link rel="canonical" href="{canonical}" />',
             f'<link rel="alternate" type="text/markdown" href="{BASE}profile.md" title="Research profile in Markdown" />',
             f'<link rel="alternate" type="application/json" href="{BASE}profile.json" title="Structured research profile" />',
             f'<link rel="alternate" type="application/x-bibtex" href="{BASE}publications.bib" title="Publication citations" />',
             f'<link rel="sitemap" type="application/xml" href="{BASE}sitemap.xml" />',
             '<meta name="author" content="Mert Kilickaya" />',
             f'<meta property="og:type" content="{"profile" if graph else "website"}" />',
             f'<meta property="og:title" content="{escape(title)}" />',
             f'<meta property="og:description" content="{escape(description)}" />',
             f'<meta property="og:url" content="{canonical}" />',
             f'<meta property="og:image" content="{image_url}" />',
             '<meta property="og:image:alt" content="Mert Kilickaya" />',
             '<meta name="twitter:card" content="summary" />']
    if graph:
        data = json.dumps(graph, ensure_ascii=False, indent=2).replace('<', r'\u003c')
        lines.append('<script type="application/ld+json" id="research-structured-data">\n' + data + '\n</script>')
    lines.append(END)
    block = '\n'.join('    ' + l if l else '' for l in '\n'.join(lines).splitlines())
    # Match generator markers independently of indentation; unrelated head content stays untouched.
    pattern = r'[ \t]*' + re.escape(BEGIN) + r'.*?' + re.escape(END)
    if BEGIN in source:
        return re.sub(pattern, lambda _: block, source, count=1, flags=re.S)
    return source.replace('  </head>', block + '\n  </head>', 1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if generated exports or metadata are stale.')
    args = parser.parse_args()
    source = (ROOT / 'index.html').read_text()
    doc = Document(source).root
    profile = read_profile(doc)
    graph = schema(profile, doc.first('title').text())
    current = profile['currentRole']
    llms = f'''# {profile['name']}

> {profile['identity']}. {current['roleTitle']} at {current['organization']} since {current['startDate']}. PhD in computer vision, University of Amsterdam; supervised by {profile['education']['supervisor']['name']}.

{profile['researchGoal']}

## Profile and evidence

- [Research profile]({BASE}profile.md): Biography, career dates, education, news, publications, patents and mentorship in Markdown, generated from the homepage.
- [Structured profile]({BASE}profile.json): The same facts as JSON, with explicit date precision and source links.
- [Publications in BibTeX]({BASE}publications.bib): Citations for the research archive, including the ESMO 2026 abstract with its available metadata.
- [Experience]({BASE}#experience): Current and previous research roles, dates, and PhD supervision.
- [Research]({BASE}#research): Research illustrations and paper, abstract, code and slide links.
- [News]({BASE}#news): Includes the ESMO 2026 Agendia research presentation and the move to Greyparrot.
- [Google Scholar]({next(p['url'] for p in profile['profiles'] if p['label'] == 'Google Scholar')}): External academic profile.
- [LinkedIn]({next(p['url'] for p in profile['profiles'] if p['label'] == 'LinkedIn')}): External professional profile.

## Personal

- [Memories]({profile['photographyURL']}): Personal photography and visual memories.
'''
    outputs = {
        'profile.json': json.dumps(profile, ensure_ascii=False, indent=2) + '\n',
        'profile.md': markdown(profile),
        'llms.txt': llms,
        'publications.bib': bibtex(profile),
        'robots.txt': 'User-agent: *\nAllow: /\n\nSitemap: ' + BASE + 'sitemap.xml\n',
        'sitemap.xml': '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>' + BASE + '</loc></url>\n  <url><loc>' + BASE + 'images.html</loc></url>\n</urlset>\n',
        'index.html': metadata(source, BASE, profile['imageURL'], graph),
        'images.html': metadata((ROOT / 'images.html').read_text(), BASE + 'images.html', profile['imageURL']),
    }
    stale = []
    for file, content in outputs.items():
        path = ROOT / file
        if not path.exists() or path.read_text() != content:
            stale.append(file)
            if not args.check:
                path.write_text(content)
    if args.check and stale:
        raise SystemExit('Stale profile output: ' + ', '.join(stale) + '. Run python3 scripts/build-profile.py.')
    print(('Checked' if args.check else 'Generated') + ' profile exports and discovery metadata: ' + ', '.join(outputs))


if __name__ == '__main__':
    main()
