from ..engine import SearchEngine
from ..config import PROXY, TIMEOUT, FAKE_USER_AGENT
from ..utils import unquote_url


class Yandex(SearchEngine):
    """Searches yandex.com"""

    def __init__(self, proxy=PROXY, timeout=TIMEOUT):
        super(Yandex, self).__init__(proxy, timeout)
        self._base_url = 'https://www.yandex.com'
        self._delay = (2, 6)
        self._current_page = 1

        self.set_headers({'User-Agent': FAKE_USER_AGENT})

    def _selectors(self, element):
        """Returns the appropriate CSS selector."""
        selectors = {
            'url': 'a[href]',
            'title': 'h2',
            'text': 'div.TextContainer',
            'links': 'div.Organic.organic.Typo.Typo_text_m.Typo_line_s.i-bem',
            'next': 'a[href][aria-label="Page {page}"]'
        }
        return selectors[element]

    def _first_page(self):
        """Returns the initial page and query."""
        url = u'{}/search/?text={}&lr=11495&cee=1'.format(self._base_url, self._query)
        return {'url': url, 'data': None}

    def _next_page(self, tags):
        """Returns the next page URL and post data (if any)"""
        self._current_page += 1
        selector = self._selectors('next').format(page=self._current_page)
        next_page = self._get_tag_item(tags.select_one(selector), 'href')
        url = None
        if next_page:
            url = self._base_url + next_page
        return {'url': url, 'data': None}

    def _get_url(self, tag, item='href'):
        """Returns the URL of search results item."""
        selector = self._selectors('url')

        url = self._get_tag_item(tag.select_one(selector), item)

        if url.startswith(u'/url?q='):
            url = url.replace(u'/url?q=', u'').split(u'&sa=')[0]

        return unquote_url(url)
