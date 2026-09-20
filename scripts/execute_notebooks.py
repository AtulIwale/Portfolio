"""Execute each notebook in a fresh kernel; fail rather than saving partial success."""
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys
import nbformat
from nbclient import NotebookClient

def execute_in_process(path, root):
    """Socket-free fallback: execute real cells with IPython and capture MIME output."""
    from IPython.core.interactiveshell import InteractiveShell
    from IPython.utils.capture import capture_output
    os.chdir(root)
    shell = InteractiveShell.instance()
    # Inline figures and display() use the same rich display publisher as a notebook.
    import matplotlib
    matplotlib.use('module://matplotlib_inline.backend_inline')
    from matplotlib_inline.backend_inline import configure_inline_support
    configure_inline_support(shell, 'module://matplotlib_inline.backend_inline')
    nb = nbformat.read(path, as_version=4)
    count = 0
    for cell in nb.cells:
        if cell.cell_type != 'code':
            continue
        count += 1
        with capture_output() as captured:
            result = shell.run_cell(cell.source, store_history=True)
        if result.error_before_exec or result.error_in_exec:
            raise RuntimeError(f'{path.name} cell {count}: {captured.stdout}\n{captured.stderr}') from (result.error_before_exec or result.error_in_exec)
        cell.execution_count = count
        cell.outputs = []
        if captured.stdout:
            cell.outputs.append(nbformat.v4.new_output('stream', name='stdout', text=captured.stdout))
        if captured.stderr:
            cell.outputs.append(nbformat.v4.new_output('stream', name='stderr', text=captured.stderr))
        for output in captured.outputs:
            cell.outputs.append(nbformat.v4.new_output('display_data', data=output.data, metadata=output.metadata))
    nb.metadata['execution_validation'] = {'method': 'fresh Python process with IPython rich output capture; not a Jupyter kernel or hosted Colab'}
    nbformat.validate(nb)
    nbformat.write(nb, path)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--kernel',default='python3')
    parser.add_argument('--in-process',action='store_true',help='Use a fresh IPython process per notebook when kernel sockets are unavailable')
    parser.add_argument('--worker',default=None,help=argparse.SUPPRESS)
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    if args.worker:
        execute_in_process(Path(args.worker), root)
        return
    results=[]
    for path in sorted((root/'notebooks').glob('*.ipynb')):
        if args.in_process:
            subprocess.run([sys.executable, str(Path(__file__).resolve()), '--worker', str(path)], check=True, timeout=600)
            nb=nbformat.read(path,as_version=4)
        else:
            nb=nbformat.read(path,as_version=4)
            client=NotebookClient(nb,timeout=600,kernel_name=args.kernel,resources={'metadata':{'path':str(root)}})
            client.execute(cleanup_kc=True)
        nbformat.validate(nb)
        errors=[o for c in nb.cells if c.cell_type=='code' for o in c.outputs if o.output_type=='error']
        assert not errors,path
        assert all(c.execution_count is not None for c in nb.cells if c.cell_type=='code' and c.source.strip())
        nbformat.write(nb,path)
        charts=sum('image/png' in o.get('data',{}) for c in nb.cells if c.cell_type=='code' for o in c.outputs)
        results.append({'notebook':path.name,'code_cells':sum(c.cell_type=='code' for c in nb.cells),
            'saved_png_outputs':charts,'errors':len(errors),'execution':('fresh Python process with IPython rich output capture' if args.in_process else 'fresh local Jupyter kernel')+'; not hosted Colab'})
        print(results[-1],flush=True)
    (root/'outputs/notebook-validation.json').write_text(json.dumps(results,indent=2)+'\n')

if __name__=='__main__':main()
