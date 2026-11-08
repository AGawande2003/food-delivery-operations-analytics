"""
04_build_notebook.py
Turns scripts/03_eda_analysis.py (cells separated by '# %%') into notebooks/Food_Delivery_EDA.ipynb,
runs every cell and stores the outputs (text + charts) inside the notebook.
You can also open the notebook in Jupyter and press Run All yourself.
Run: python scripts/04_build_notebook.py
"""
import ast, base64, contextlib, io, json, os, re, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "03_eda_analysis.py")
OUT = os.path.join(HERE, "..", "notebooks", "Food_Delivery_EDA.ipynb")
os.chdir(os.path.join(HERE, "..", "notebooks"))

text = open(SRC, encoding="utf-8").read()
parts = re.split(r"^# %%", text, flags=re.M)[1:]
cells, ns, count = [], {"__name__": "__main__"}, 0

def src_lines(s):
    lines = s.strip("\n").split("\n")
    return [l + "\n" for l in lines[:-1]] + [lines[-1]]

for part in parts:
    first, _, body = part.partition("\n")
    if "[markdown]" in first:
        md = "\n".join(re.sub(r"^# ?", "", l) for l in body.strip("\n").split("\n"))
        cells.append({"cell_type": "markdown", "metadata": {}, "source": src_lines(md)})
        continue
    code = body.strip("\n")
    count += 1
    outputs = []
    buf = io.StringIO()
    tree = ast.parse(code)
    last_expr = None
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        last_expr = ast.Expression(tree.body.pop().value)
    with contextlib.redirect_stdout(buf):
        exec(compile(tree, "<cell>", "exec"), ns)
        value = eval(compile(last_expr, "<cell>", "eval"), ns) if last_expr is not None else None
    if buf.getvalue():
        outputs.append({"output_type": "stream", "name": "stdout", "text": src_lines(buf.getvalue().rstrip("\n"))})
    if value is not None:
        outputs.append({"output_type": "execute_result", "execution_count": count, "metadata": {},
                        "data": {"text/plain": src_lines(repr(value))}})
    for num in plt.get_fignums():
        fig = plt.figure(num); b = io.BytesIO(); fig.savefig(b, format="png", dpi=100, bbox_inches="tight")
        outputs.append({"output_type": "display_data", "metadata": {},
                        "data": {"image/png": base64.b64encode(b.getvalue()).decode(), "text/plain": ["<Figure>"]}})
    plt.close("all")
    cells.append({"cell_type": "code", "execution_count": count, "metadata": {}, "outputs": outputs,
                  "source": src_lines(code)})

nb = {"cells": cells, "nbformat": 4, "nbformat_minor": 5,
      "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                   "language_info": {"name": "python"}}}
json.dump(nb, open(OUT, "w", encoding="utf-8"), indent=1)
print("notebook written:", OUT, "| code cells:", count)
