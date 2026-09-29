import re
def sub_line(s, prefix, new):
    """Replace the whole line that starts (after indentation) with prefix."""
    lines = s.split('\n'); hits = [i for i, l in enumerate(lines) if l.lstrip().startswith(prefix)]
    assert len(hits) == 1, (prefix, len(hits))
    ind = lines[hits[0]][:len(lines[hits[0]]) - len(lines[hits[0]].lstrip())]
    lines[hits[0]] = ind + new
    return '\n'.join(lines)
def rep(s, a, b):
    assert s.count(a) == 1, (a[:60], s.count(a)); return s.replace(a, b)
