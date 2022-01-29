import re
import json
import sys
from pathlib import Path
import nbformat.v4 as nbf
from nbformat import write as nbf_write

start_re = re.compile("#sss")
end_re = re.compile("#eee")
delete_re = re.compile("#ddd")
tasks_re = re.compile("#ttt")

filename = sys.argv[1] # get path
folder = sys.argv[2]

filename = Path(filename)
with open(filename, 'r') as fh: data = json.load(fh)

cells = data["cells"]


nb = nbf.new_notebook()

tasks_content = None
new_cells = []
for c in cells:
    src = c["source"]
    start = None
    end = None
    delete = False
    tasks = False
    for i, l in enumerate(src):
        if start_re.search(l):
            start = i
        if end_re.search(l):
            end = i
        if delete_re.search(l):
            delete = True
        if tasks_re.search(l):
            tasks = True

    if start is not None and end is not None:
        new_src = src[:start] + ["    # Write your code here\n"] + src[end + 1:]
    else:
        new_src = src

    if tasks:
        tasks_content = src

    #c["source"] = new_src
    if delete or tasks:
        pass
    elif c["cell_type"] == "markdown":
        cell = nbf.new_markdown_cell(new_src)
        new_cells.append(cell)
    elif c["cell_type"] == "code":
        cell = nbf.new_code_cell(new_src)
        new_cells.append(cell)
    
try:
    tasks_content = "".join(tasks_content[1:]).replace("TASKS = ", "")
except TypeError as e:
    print("".join(tasks_content[1:]))
    raise(e)
submission = f"""

proposed_solution = {{
'attempt': {{
    'course_name': COURSE_NAME,
    'exercise_name': EXERCISE_NAME,
    'username': STUDENT_NAME,
}},
'task_attempts': {tasks_content}

}}
check_solution(proposed_solution)
"""
cell = nbf.new_code_cell(submission)
new_cells.append(cell)

nb["cells"] = new_cells

new_name = filename.with_name(filename.stem + "_public" + filename.suffix)
print(new_name)
if folder is not None:
    new_name = (filename.parent / folder) / new_name.name
print(new_name)
with open(new_name, 'w') as f:
        nbf_write(nb, f, 4)
