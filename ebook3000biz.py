from __future__ import unicode_literals, division, absolute_import
from builtins import *  # noqa pylint: disable=unused-import, redefined-builtin

import logging
import re

from flexget import plugin
from flexget.event import event
from flexget.plugins.internal.urlrewriting import UrlRewritingError
from flexget.utils.soup import get_soup
from flexget.utils.search import normalize_unicode

from requests.exceptions import RequestException

log = logging.getLogger('rlsbb')


class UrlRewriteEbook3000biz(object):
    """
    ebook3000.biz urlrewriter
    Version 0.1

    Rewrites urls for ebook3000.biz
    
    On ebook3000.biz, each link points to a page which contains the links to the actual files. 
    Often these pages contain more than one link.

    If more than one valid link is found, the url of the entry is rewritten to
    the first link found. The complete list of valid links is placed in the
    'urls' field of the entry.

    Therefore, it is recommended, that you configure your output to use the
    'urls' field instead of the 'url' field.

    For example, to use jdownloader 2 as output, you would use the exec plugin:
    exec:
      - echo "text={{urls}}" >> "/path/to/jd2/folderwatch/{{title}}.crawljob"

    The plugin is intended to be used in conjunction with the rss plugin.

    Example configuration for the rss plugin:

    html:
      url: "http://www.ebook3000.biz/category/magazine/"
      title_from: link
      links_re
        - ebook3000.biz/[^/]*/$  
    """

    # urlrewriter API
    def url_rewritable(self, task, entry):
        url = entry['url']
        rewritable_regex = '^https?:\/\/(www.)?ebook3000\.biz\/.*'
        return re.match(rewritable_regex, url) is not None

    def _get_soup(self, task, url):
        try:
            page = task.requests.get(url)
        except RequestException as e:
            raise UrlRewritingError(str(e))
        try:
            return get_soup(page.text)
        except Exception as e:
            raise UrlRewritingError(str(e))

    @plugin.internet(log)
    # urlrewriter API
    def url_rewrite(self, task, entry):
        soup = self._get_soup(task, entry['url'])

        # grab links from the main post:
        # Can't work perfectly filescdn\.com.*/*$  
        # Can't work perfectly suprafiles\.net.*/*$
        link_re = re.compile('dailyuploads\.net.*/*$|dropupload\.com.*/*$|cloudyfiles\.com.*/*$|upload4earn\.com.*/*$')

        num_links = 0
        link_list = None
        blog_entry = soup.find('div', class_="box-inner-block")
        for paragraph in blog_entry.find_all('p'):
            links = paragraph.find_all('a', href=link_re)
            if len(links) > num_links:
                link_list = links
                num_links = len(links)
        if 'urls' in entry:
            urls = list(entry['urls'])
        else:
            urls = []
        if link_list is not None:
            for link in link_list:
                urls.append(normalize_unicode(link['href']))
        else:
            raise UrlRewritingError('No useable links found at %s' % entry['url'])

        num_links = len(urls)
        log.verbose('Found %d links at %s.', num_links, entry['url'])
        if num_links:
            entry['urls'] = urls
            entry['url'] = urls[0]
        else:
            raise UrlRewritingError('No useable links found at %s' % entry['url'])

@event('plugin.register')
def register_plugin():
    plugin.register(UrlRewriteEbook3000biz, 'ebook3000biz', interfaces=['urlrewriter'], api_ver=2)
