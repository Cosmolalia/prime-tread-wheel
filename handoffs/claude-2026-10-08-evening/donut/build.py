import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(HERE, "dims_compact.json")))
tpl = open(os.path.join(HERE, "template.html")).read()
assert tpl.count("__DATA__") == 1
html = tpl.replace("__DATA__", json.dumps(data, separators=(",", ":")))
open(os.path.join(HERE, "donut-view.html"), "w").write(html)
print("wrote donut-view.html", len(html), "bytes")
