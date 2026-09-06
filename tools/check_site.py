"""Validate the static site as crawlers receive it, without browser JavaScript."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote, urljoin
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://shutupfly.timhudson.com'
APP = 'https://apps.apple.com/us/app/shut-up-fly/id6797986930'


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.tags, self.ids, self.schemas = path, [], [], []
        self.title, self.schema, self.in_title = '', None, False
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'title':
            self.in_title = True
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.schema = ''

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.schema is not None:
            self.schema += data

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        if tag == 'script' and self.schema is not None:
            self.schemas.append(json.loads(self.schema))
            self.schema = None

    def find(self, tag, **attrs):
        return [a for t, a in self.tags if t == tag and all(a.get(k) == v for k, v in attrs.items())]


def path_for(url):
    path = ROOT / unquote(urlsplit(url).path).lstrip('/')
    return path / 'index.html' if path.is_dir() else path


urls = [node.text for node in ET.parse(ROOT / 'sitemap.xml').findall('.//{*}loc')]
assert len(urls) == len(set(urls)) == 5, 'Sitemap should list five unique canonical pages'
pages = {url: Page(path_for(url)) for url in urls}
titles = []
for url, page in pages.items():
    assert len(page.find('h1')) == 1, (url, 'one H1 required')
    assert len(page.ids) == len(set(page.ids)), (url, 'duplicate IDs')
    assert len(page.find('title')) == 1 and page.title, (url, 'title required')
    titles.append(page.title)
    assert page.find('link', rel='canonical') == [{'rel': 'canonical', 'href': url}], (url, 'canonical mismatch')
    descriptions = page.find('meta', name='description')
    assert len(descriptions) == 1 and descriptions[0].get('content'), (url, 'description required')
    assert not any('noindex' in a.get('content', '').lower() for a in page.find('meta', name='robots')), url
    for tag, attrs in page.tags:
        for attr in ('href', 'src', 'poster'):
            value = attrs.get(attr)
            if not value or urlsplit(value).scheme or value.startswith('//'):
                continue
            target = path_for(urljoin(url, value))
            assert target.exists(), (url, 'missing resource', value)
            fragment = urlsplit(value).fragment
            if fragment and target.suffix == '.html':
                assert fragment in Page(target).ids, (url, 'broken anchor', value)
    for img in page.find('img'):
        assert 'alt' in img and img.get('width') and img.get('height'), (url, 'image metadata')

assert len(titles) == len(set(titles)), 'Page titles must be unique'
home = pages[ORIGIN + '/']
game = home.schemas[0]
assert set(game['@type']) == {'VideoGame', 'MobileApplication'}
assert game['offers']['price'] == '0' and game['operatingSystem'] == 'iOS 18.0 or later'
assert game['downloadUrl'] == APP
assert 'aggregateRating' not in game and 'review' not in game, 'Do not invent or freeze ratings'
for route in ('/offline-iphone-game/', '/how-to-play/'):
    assert home.find('a', href=route), ('unlinked guide', route)
    guide = pages[ORIGIN + route]
    assert guide.find('a', href=APP), ('missing download action', route)
    graph = guide.schemas[0]['@graph']
    assert graph[0]['url'] == ORIGIN + route
    assert graph[1]['itemListElement'][-1]['item'] == ORIGIN + route
    assert guide.find('a', href='/'), ('missing return path', route)

robots = (ROOT / 'robots.txt').read_text()
assert 'Disallow: /' not in robots
assert f'Sitemap: {ORIGIN}/sitemap.xml' in robots
print(f'PASS: {len(pages)} static pages; titles, canonicals, sitemap, schema, images, internal links, anchors, and download paths')
