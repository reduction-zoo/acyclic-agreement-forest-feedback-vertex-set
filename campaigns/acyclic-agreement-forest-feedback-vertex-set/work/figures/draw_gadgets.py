"""Exact cover-gadget vector figure and explicitly schematic threshold composition."""
from itertools import combinations
from pathlib import Path

directory = Path(__file__).parent
points = dict(q0=(65,125), q1=(190,125), z0=(385,125), z1=(510,125),
              a=(190,255), b=(510,255), c=(65,365), d=(510,365), e=(385,40))
edges = [('q0','q1'), ('z0','z1'), ('a','b'), ('c','d'),
         ('a','q1'), ('b','z1'), ('c','q0'), ('d','z1'), ('e','z0')]
selected = {'q1','z0','z1','a','c'}
assert len(points) == 9 and len(set(edges)) == 9
assert all(u in selected or v in selected for u,v in edges)
assert not any(all(u in subset or v in subset for u,v in edges)
               for subset in combinations(points,4))
labels = dict(q0='q₀',q1='q₁',z0='z₀',z1='z₁',a='c₁,q',b='c₁,z',
              c='c₂,¬q',d='c₂,z',e='c₃,¬z')
svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 650 420">',
       '<g fill="none" stroke="#222" stroke-width="2.4">']
for u,v in edges:
    x,y=points[u];a,b=points[v]
    if (u,v)==('d','z1'):
        svg.append(f'<path d="M{x},{y} C625,365 625,125 {a},{b}"/>')
    else:
        svg.append(f'<line x1="{x}" y1="{y}" x2="{a}" y2="{b}"/>')
svg.append('</g>')
for name,(x,y) in points.items():
    svg.append(f'<circle cx="{x}" cy="{y}" r="8" stroke="#111" stroke-width="2.4" fill="{"#111" if name in selected else "white"}"/>')
    anchor, label_x = ('middle',x) if name in ('a','b','c','d') else ('end',x-15)
    svg.append(f'<text x="{label_x}" y="{y+29}" text-anchor="{anchor}" font-family="Libertinus Serif,serif" font-size="23">{labels[name]}</text>')
svg.append('</svg>')
(directory/'guarded-cover.svg').write_text('\n'.join(svg)+'\n')

# Boxes denote entire graphs; no internal vertex or edge is claimed by this schematic.
(directory/'thresholds.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 650 160">
<g fill="none" stroke="#222" stroke-width="2.4">
<rect x="8" y="8" width="634" height="144" rx="9"/>
<rect x="35" y="40" width="145" height="85"/>
<rect x="215" y="40" width="145" height="85"/>
<rect x="470" y="40" width="145" height="85"/>
</g><g text-anchor="middle" fill="#111" font-family="Libertinus Serif,serif" font-size="24">
<text x="108" y="76">H₂</text><text x="288" y="76">H₃</text>
<text x="415" y="87">⋯</text><text x="543" y="76">H<tspan baseline-shift="sub" font-size="16">U</tspan></text>
<text x="108" y="107">Y ∩ V(H₂)</text><text x="288" y="107">Y ∩ V(H₃)</text>
<text x="543" y="107">Y ∩ V(H<tspan baseline-shift="sub" font-size="16">U</tspan>)</text></g></svg>
''')
print('PASS exact figure: 9 vertices, 9 undirected edges / 18 arcs, minimum cover 5, baseline 4.')
print('Threshold figure is schematic: disjoint graph boxes, all internal edges omitted.')
