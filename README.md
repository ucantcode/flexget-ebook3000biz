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
