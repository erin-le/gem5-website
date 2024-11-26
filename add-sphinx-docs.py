import os

search_bar_lines = []
html = []

def remove_searchbar(html):
    search_flag = False
    for index, line in enumerate(html):
        if '<div id="searchbox" style="display: none" role="search">' in line:
            search_flag = True
        if search_flag == True:
            html[index] = ""
        if '<script>document.getElementById(\'searchbox\').style.display = "block"</script>' in line:
            search_flag = False
    return html


with open(f"./_pages/documentation/general_docs/sphinx_docs/_modules/index.html", "r+") as f:
    html = f.readlines()
    f.seek(0, 0)
    f.truncate(0)
    # Add frontmatter so the docs pages can be accessed in the website
    f.write("---\n")
    f.write(f'title: "Sphinx Documentation"\n')
    f.write("parent: sphinx-docs\n")
    f.write(f"permalink: /documentation/general_docs/sphinx_docs/index.html\n")
    f.write("---\n")

    for index, line in enumerate(html):
        modified_line = None

        # make the links at the bottom of index.html work
        if "<li><a href=" in line:
            if (
                '<li><a href="../index.html">Documentation overview</a><ul>'
                in line
            ):
                modified_line = (
                    '<li><a href="./index.html">Documentation overview</a><ul>'
                )
            else:
                # For links to the other documentation pages from index.html, replace the `.` in the path with `/`. This makes things more consistent and allows links from index.html to a Sphinx page and links between two Sphinx pages to work.
                modified_line = (
                    line.replace("/", ".")
                    .replace("<.a>", "</a>")
                    .replace("<.li>", "</li>")
                )
        elif (
            '<li class="toctree-l1"><a class="reference internal" href="../gem5.html">gem5 package</a></li>'
            in line
        ):
            print("../gem5.html switched to ./gem5.html")
            modified_line = '<li class="toctree-l1"><a class="reference internal" href="./gem5.html">gem5 package</a></li>'

        elif '<h1 class="logo"><a href="../index.html">gem5</a></h1>' in line:
            print("../index.html switched to ./index.html")
            modified_line = (
                '<h1 class="logo"><a href="./index.html">gem5</a></h1>'
            )
        else:
            modified_line = line

        html[index] = modified_line

    html = remove_searchbar(html)
    
    for line in html:
        f.write(line)


for filename in os.listdir("./_pages/documentation/general_docs/sphinx_docs"):
    if filename.startswith("gem5"):
        with open(f"./_pages/documentation/general_docs/sphinx_docs/{filename}", "r+") as f:
            html = f.readlines()
            f.seek(0, 0)
            f.truncate(0)
            f.write("---\n")
            f.write(f'title: "{filename}"\n')
            f.write("parent: sphinx-docs\n")
            f.write(
                f"permalink: /documentation/general_docs/sphinx_docs/{filename}\n"
            )
            f.write("---\n")
            html = remove_searchbar(html)
            
            for line in html:
                f.write(line)