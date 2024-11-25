import os

# for filename in os.listdir('../../docs/_build/html'):
# for filename in os.listdir('/Volumes/Crucial/gem5-dev/website/_pages/documentation/general_docs/sphinx_docs'):
search_bar_lines = []
html = []

with open(f"./_build/html/_modules/index.html", "r+") as f:
    html = f.readlines()
    f.seek(0, 0)

    # Add frontmatter so the docs pages can be accessed in the website
    f.write("---\n")
    f.write(f'title: "Sphinx Documentation"\n')
    f.write("parent: sphinx-docs\n")
    f.write(f"permalink: /documentation/general_docs/sphinx_docs/index.html\n")
    f.write("---\n")

    search_flag = False
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
                # For links to all Sphinx documentation pages from index, replace the `.` in the path with `/`. This makes things more consistent and allows both links from index.html to a Sphinx page and links between two Sphinx pages to work.
                modified_line = (
                    line.replace("/", ".")
                    .replace("<.a>", "</a>")
                    .replace("<.li>", "</li>")
                )
        if (
            '<li class="toctree-l1"><a class="reference internal" href="../gem5.html">gem5 package</a></li>'
            in line
        ):
            print("../gem5.html switched to ./gem5.html")
            modified_line = '<li class="toctree-l1"><a class="reference internal" href="./gem5.html">gem5 package</a></li>'

        if '<h1 class="logo"><a href="../index.html">gem5</a></h1>' in line:
            print("../index.html switched to ./index.html")
            modified_line = (
                '<h1 class="logo"><a href="./index.html">gem5</a></h1>'
            )

        # remove the search bar
        if 'id="searchbox"' in line:
            search_flag = True
            modified_line = ""
        elif "'searchbox').style.display = \"block\"</script>" in line:
            search_flag = False
            modified_line = ""
        elif search_flag == True:
            modified_line = ""
        else:
            modified_line = line
        # if '</html>searchbox\').style.display = "block"</script>' in line:
        #     f.write("</html>")
        # else:
        # f.write(modified_line)
        html[index] = modified_line
        # print("latest version gotten")

    # with open(f"./_build/html/_modules/index.html", "r+") as f:
    # html = f.readlines()
    # f.seek(0, 0)
    for index, line in enumerate(html):
        if '</html>searchbox\').style.display = "block"</script>' in line:
            # f.write("</html>")
            html[index] = "</html>"
        # else:
        #     f.write(line)
    f.write(html)


for filename in os.listdir("./_build/html"):

    # print(filename)
    if filename.startswith("gem5"):  # and filename != "gem5.html"
        # print(filename)
        # with open (f"../../docs/_build/html/{filename}", "r+") as f:
        # with open (f"/Volumes/Crucial/gem5-dev/website/_pages/documentation/general_docs/sphinx_docs/{filename}", "r+") as f:
        with open(f"./_build/html/{filename}", "r+") as f:
            html = f.read()
            f.seek(0, 0)
            f.write("---\n")
            f.write(f'title: "{filename}"\n')
            f.write("parent: sphinx-docs\n")
            # modified_filename = filename.replace(".", "/").replace(
            #     "/html", ".html"
            # )

            # f.write(
            #     f"permalink: /documentation/general_docs/sphinx_docs/{modified_filename}\n"
            # )
            f.write(
                f"permalink: /documentation/general_docs/sphinx_docs/{filename}\n"
            )
            f.write("---\n")
            f.write(html)
