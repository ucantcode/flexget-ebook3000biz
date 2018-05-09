<h2>Brief</h2>
    This is the python code for flexget. Put it into the "/usr/local/lib/python2.7/dist-packages/flexget/plugins/sites/".
<h2>Configuration</h2>

    html:
      url: "http://www.ebook3000.biz/category/magazine/"
      title_from: link
      links_re
        - ebook3000.biz/[^/]*/$  
    exec:
      - echo "text={{urls}}" >> "/path/to/jd2/folderwatch/{{title}}.crawljob"
