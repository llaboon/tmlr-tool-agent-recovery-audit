from pathlib import Path
p=Path('main.tex'); lines=p.read_text().splitlines(); idx=next(i for i,x in enumerate(lines) if 'input{main.bbl}' in x); p.write_text('\n'.join(lines[:idx]+['\\input{main.bbl}','\\end{document}'])+'\n')
