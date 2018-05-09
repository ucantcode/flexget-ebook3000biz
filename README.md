<h2>Brief</h2>

<h2>Configuration</h2>

    html:
      url: "http://www.ebook3000.biz/category/magazine/"
      title_from: link
      links_re
        - ebook3000.biz/[^/]*/$  
    exec:
      - echo "text={{urls}}" >> "/path/to/jd2/folderwatch/{{title}}.crawljob"
