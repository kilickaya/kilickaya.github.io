#!/usr/bin/env python3
"""Draw the site's publication and patent concept illustrations. No dependencies."""
from pathlib import Path
from html import escape

DEST = Path(__file__).resolve().parents[1] / 'images' / 'research'
PAPER, OAT, INK, STONE = '#f8f5ed', '#eee8dc', '#514b40', '#655f55'
CLAY, SAGE, PALE, SAND = '#ad7056', '#7b8873', '#dce0d4', '#dfc5b5'

def line(x1,y1,x2,y2,color=INK,dash=False):
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}"'+(' stroke-dasharray="6 9"' if dash else '')+'/>'
def path(d,color=INK,fill='none',extra=''):
    return f'<path d="{d}" stroke="{color}" fill="{fill}" {extra}/>'
def box(x,y,w,h,fill=PAPER,stroke=INK,r=8,extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" {extra}/>'
def circle(x,y,r=5,fill=INK,stroke='none'):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}"/>'
def text(x,y,label,size=26,anchor='middle',color=STONE):
    return f'<text x="{x}" y="{y}" fill="{color}" stroke="none" font-size="{size}" text-anchor="{anchor}">{escape(label)}</text>'
def arrow(x1,y1,x2,y2,color=INK,dash=False):
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" marker-end="url(#arrow)"'+(' stroke-dasharray="6 9"' if dash else '')+'/>'
def group(content,x=0,y=0,scale=1):
    return f'<g transform="translate({x} {y}) scale({scale})">{content}</g>'
def network(x,y,w=100,h=80,fill=PAPER,accent=INK):
    nodes=[(0,h*.25),(0,h*.75),(w*.5,0),(w*.5,h*.5),(w*.5,h),(w,h*.25),(w,h*.75)]
    s=''
    for i,j in [(0,2),(0,3),(1,3),(1,4),(2,5),(3,5),(3,6),(4,6)]:
        s+=line(*nodes[i],*nodes[j],accent)
    for a,b in nodes:s+=circle(a,b,6,fill,accent)
    return group(s,x,y)
def patch(x,y,scale=1,highlight=False):
    s=''
    for row in range(4):
        for col in range(4):
            fill=[PAPER,PALE,OAT,SAND][(row*3+col*2)%4]
            s+=box(col*25,row*25,22,22,fill,INK,2)
    if highlight:s+=box(22,22,54,54,'none',CLAY,4,extra='stroke-width="4"')
    return group(s,x,y,scale)
def cube(x,y):
    s=''
    for k in [3,2,1,0]:
        s+=box(k*12,-k*12,94,94,[PALE,SAND,OAT,PAPER][k],INK,4)
    for j in range(1,4):s+=line(j*23.5,0,j*23.5,94)+line(0,j*23.5,94,j*23.5)
    return group(s,x,y)
def phone(x,y,fill=PAPER,rotation=0):
    s=box(-22,-38,44,76,fill,INK,8)+box(-15,-28,30,38,OAT,INK,3)+line(-7,20,7,20)+circle(0,30,2,INK)
    return f'<g transform="translate({x} {y}) rotate({rotation})">{s}</g>'
def save(name,title,desc,content,directory=DEST):
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="500" viewBox="0 0 800 500" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title>
<desc id="desc">{escape(desc)}</desc>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M1 1 L8 5 L1 9" fill="none" stroke="{INK}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>
<rect width="800" height="500" fill="{OAT}"/>
<g fill="none" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" font-family="Arial, sans-serif">{content}</g>
</svg>\n'''
    directory.mkdir(parents=True, exist_ok=True)
    (directory / f'{name}.svg').write_text(svg)

# HyTAS: spectral data and a search space, with one candidate architecture selected.
s=cube(67,212)+arrow(212,247,260,247)
s+=box(285,112,205,270,'none','#bdb3a1',16)
for y,accent in [(145,INK),(228,CLAY),(311,INK)]:
    if accent==CLAY:s+=box(299,y-13,176,85,PAPER,CLAY,10)
    s+=network(322,y,126,58,PAPER,accent)
s+=arrow(514,247,569,247)+network(612,202,111,88,PALE,SAGE)
s+=text(130,432,'Spectral data',28)+text(388,432,'Search',28)+text(665,432,'Architecture',28)
s+=text(388,72,'HyTAS',22,color=INK)
save('hytas','Searching for a hyperspectral transformer','A stack of spectral image planes enters a set of candidate networks. One candidate is highlighted and leads to a selected architecture. Conceptual illustration of the architecture-search benchmark, not a performance comparison.',s)

# HyLITE: local neighborhood and spectral information converge, rather than a generic ViT.
s=patch(66,131,1.15,True)+text(124,100,'Local context',28)
s+=path('M194 186 C250 186 260 244 302 244')
for i,h in enumerate([30,58,42,78,52]):s+=box(74+i*21,349-h,14,h,[SAGE,CLAY,SAND,SAGE,CLAY][i],'none',2)
s+=text(124,395,'Spectra',28)+path('M194 314 C250 314 260 254 302 254')
s+=box(311,191,190,118,PAPER,INK,12)
for x in [342,392,442]:
    s+=box(x,226,26,48,PALE,SAGE,4)
s+=line(368,250,392,250,SAGE)+line(418,250,442,250,SAGE)
s+=text(406,350,'HyLITE',28)+arrow(521,250,574,250)
for r in range(4):
 for c in range(4):s+=box(607+c*23,203+r*23,20,20,[PALE,SAND,SAGE][(r//2+c//2)%3],'none',2)
s+=text(650,350,'Classify',28)
save('hylite','Local and spectral context together','A highlighted image neighborhood and a spectral profile converge in HyLITE, then produce a classification map. This represents local and spectral information jointly, without depicting a literal model architecture.',s)

# Survey: three kinds of supervision on the same continuing time axis.
s=''
rows=[(142,'Semi-supervised'),(252,'Few-shot'),(362,'Self-supervised')]
for y,label in rows:
 s+=text(52,y+8,label,25,'start')
 s+=arrow(294,y,748,y,'#bdb3a1')
 for k,x in enumerate([346,502,658]):
  s+=circle(x,y,27,PAPER,INK)
  if label=='Semi-supervised':
   s+=circle(x-7,y,5,CLAY)+circle(x+7,y,5,PAPER,INK)
  elif label=='Few-shot':
   s+=circle(x,y,5,CLAY)
  else:
   s+=path(f'M{x-13} {y+1} Q{x} {y-22} {x+13} {y+1}',SAGE)
   s+=path(f'M{x-13} {y+1} Q{x} {y+22} {x+13} {y+1}',SAGE)
   s+=circle(x,y,3,SAGE)
for x,label in [(346,'Past'),(502,'Present'),(658,'Next')]:s+=text(x,77,label,26)
s+=text(400,448,'Learning over time, with fewer labels',26)
save('label-efficient-learning','Three paths to label-efficient incremental learning','Semi-supervised, few-shot and self-supervised learning are shown as three conceptual paths through past, present and future data. Filled dots indicate labels; paired arcs indicate self-supervised views. The diagram makes no numerical comparison.',s)

# VINIL: two augmentations of each observed instance, then sequential updating.
s=box(62,145,118,100,PAPER,INK,10)+phone(121,196,PAPER,-10)
s+=box(62,267,118,100,PALE,SAGE,10)+phone(121,318,PALE,12)
s+=path('M198 195 C248 195 245 250 285 250')+path('M198 317 C248 317 245 250 285 250')
s+=box(300,193,184,114,PAPER,INK,12)+text(392,259,'VINIL',30,color=INK)
s+=arrow(505,250,555,250)
# A continuation line carries previously seen and future instance representations.
s+=line(571,250,737,250,'#bdb3a1')
for x,fill in [(592,SAND),(648,PALE),(704,PAPER)]:
 s+=circle(x,250,19,fill,INK)
s+=path('M335 171 C335 119 451 119 451 171',SAGE,extra='marker-end="url(#arrow)"')
s+=text(121,421,'Two views',28)+text(392,421,'Self-supervision',28)+text(651,421,'Keep learning',28)
save('vinil','Learning instances from their own views','Two transformed views of the same phone feed VINIL. A loop represents continued self-supervised updating and a sequence of instance symbols represents learning over time. This is not a replay-buffer diagram.',s)

# Align-Former: an image and image-level interaction labels, not annotated pairs.
s=box(54,152,215,181,PAPER,INK,12)
# Minimal person reaching toward an object, contained in a simple scene.
s+=circle(112,204,13,PAPER,INK)+path('M112 220 L112 267 M112 237 L157 247 M112 265 L91 304 M112 265 L133 304')
s+=box(178,239,32,47,PALE,SAGE,6)
s+=text(162,381,'Image',28)
s+=box(306,74,190,51,SAND,'none',6)+text(401,108,'Image-level label',22,color=INK)
s+=path('M401 126 L401 177',INK,extra='marker-end="url(#arrow)"')
s+=arrow(285,250,322,250)+box(338,195,126,111,PAPER,INK,12)
# Alignment marks pair symbols, not a densely detailed architecture.
s+=circle(370,233,8,CLAY)+circle(432,269,8,SAGE)+line(378,238,424,264)
s+=arrow(482,250,523,250)+box(549,152,198,181,PAPER,INK,12)
s+=box(574,181,52,128,'none',CLAY,5)+box(662,235,48,62,'none',SAGE,5)
s+=circle(600,208,11,PAPER,INK)+path('M600 221 L600 265 M600 236 L671 249 M600 265 L585 296 M600 265 L614 296')
s+=box(671,245,30,42,PALE,SAGE,4)+path('M626 226 Q650 207 681 235',CLAY)
s+=text(401,381,'Align',28)+text(648,381,'Localize',28)
save('align-former','Finding interactions from image-level supervision','A simple scene and an image-level interaction label feed an alignment step. The output localizes a person and an object and connects their interaction. No region-pair annotations are depicted as inputs.',s)

# Composition-aware visual search: relation changes correspond to representation changes.
s=''
for x,side in [(71,False),(515,True)]:
 s+=box(x,102,212,185,PAPER,INK,10)
 # The same two tokens change relative arrangement. These are relation symbols, not detections.
 if not side:
  s+=box(x+84,127,40,69,SAND,CLAY,5)+box(x+45,199,120,48,PALE,SAGE,5)
  s+=path(f'M{x+104} 184 L{x+104} 207',INK)
 else:
  s+=box(x+26,165,40,69,SAND,CLAY,5)+box(x+91,165,96,48,PALE,SAGE,5)
  s+=path(f'M{x+67} 189 L{x+94} 189',INK)
 s+=arrow(x+106,304,x+106,350)
 s+=box(x+58,369,96,53,PAPER,INK,6)
 s+=circle(x+82,407 if side else 385,5,CLAY)+circle(x+106,396,5,SAGE)+circle(x+130,385 if side else 407,5,INK)
s+=arrow(310,194,488,194)+text(400,154,'Recompose',26)
s+=arrow(310,396,488,396)+text(400,444,'Change together',26)
s+=text(177,66,'Visual query',26)+text(621,66,'New relation',26)
save('composition-aware-search','Keeping visual relationships in a representation','Two visual queries contain the same abstract person and object tokens but different spatial relationships. Corresponding representations below are linked to emphasize structure-preserving learning. This is a conceptual account of composition-aware visual search.',s)

# Caption evaluation: a common visual scene, different wording, and semantic word matching.
s=box(54,153,174,167,PAPER,INK,12)
s+=path('M74 282 Q104 274 135 282 T209 282',SAGE)
s+=path('M93 253 L190 253 L172 274 L111 274 Z',INK,PALE)+circle(143,211,10,PAPER,INK)+path('M143 223 L143 251 M143 233 L172 245')
s+=text(141,374,'Image',28)+arrow(245,236,292,236)
s+=box(314,107,430,89,PAPER,INK,9)+box(314,271,430,89,PAPER,INK,9)
s+=text(529,143,'A person in a boat',27,color=INK)+text(529,179,'Reference',20)
s+=text(529,307,'Someone on the water',27,color=INK)+text(529,343,'Candidate',20)
for x1,x2 in [(401,390),(527,539),(663,654)]:
 s+=path(f'M{x1} 210 C{x1} 235 {x2} 235 {x2} 257',SAGE)
 s+=circle(x1,209,4,SAGE)+circle(x2,258,4,SAGE)
s+=text(529,422,'Compare meaning',28)
save('caption-evaluation','Evaluating the meaning of image captions','A minimal scene of a person in a boat is paired with a reference caption and a differently worded candidate caption. Correspondence lines illustrate semantic comparison, inspired by Word Mover’s Distance, without assigning invented scores.',s)

# Digital pathology: conceptual WSI-to-network-to-score flow, without a numerical claim.
s=box(53,151,173,185,PAPER,INK,12)+box(65,163,149,21,OAT,'none',3)
s+=path('M80 221 C94 184 138 200 148 215 C185 194 205 239 183 262 C204 293 163 319 141 295 C100 319 68 281 86 260 C69 249 70 233 80 221 Z',CLAY,SAND)
for x,y in [(96,231),(122,218),(158,232),(176,250),(144,264),(109,278),(164,285),(99,251)]:
 s+=circle(x,y,4,CLAY)
s+=box(129,236,35,35,'none',SAGE,2,extra='stroke-width="3"')
s+=arrow(248,247,301,247)
s+=network(338,193,124,108,PAPER,SAGE)
s+=arrow(492,247,546,247)
s+=box(576,190,169,112,PAPER,INK,12)
s+=text(660,223,'Recurrence',23)+text(660,253,'risk score',23)
s+=line(597,278,723,278,STONE)+circle(671,278,7,CLAY)
s+=text(140,412,'Whole-slide image',25)+text(400,412,'Neural network',25)+text(660,412,'Risk score',25)
save('digital-pathology','From whole-slide tissue images to recurrence risk','A conceptual whole-slide tissue image is passed into a neural network that outputs a recurrence risk score. The marker is illustrative and gives no numerical or clinical prediction.',s)

print(f'Wrote eight SVG illustrations to {DEST}')

# Patent concepts share the publication palette, proportions and drawing helpers.
PATENTS = DEST.parent / 'patents'

def human(x,y):
    return group(circle(0,-43,12,PAPER,INK)+path('M0 -29 L0 22 M0 -10 L34 7 M0 22 L-18 53 M0 22 L23 53'),x,y)

def scene(x,y,highlight=False):
    s=box(0,0,170,160,PAPER,INK,10)+human(60,83)
    s+=box(100,70,35,45,SAND,CLAY,5)
    if highlight:s+=box(91,61,53,63,'none',SAGE,5,extra='stroke-width="3"')
    return group(s,x,y)

# A visual query and conversational refinement select a different matching item.
s=box(55,174,148,138,PAPER,INK,10)
s+=path('M80 255 L106 224 L122 238 L166 251 L179 272 L80 272 Z',INK,SAND)
s+=box(234,100,222,79,PAPER,INK,12)
s+=path('M267 179 L267 196 L287 179',INK,PAPER)
s+=line(255,127,428,127,STONE)+line(255,148,374,148,STONE)
s+=arrow(225,250,293,250)+network(322,220,102,70,PAPER,SAGE)+arrow(455,250,514,250)
for y,color in [(130,PAPER),(244,PALE)]:
 s+=box(550,y,190,94,color,SAGE if y==244 else INK,10)
 s+=path(f'M578 {y+54} L600 {y+29} L618 {y+42} L701 {y+55} L711 {y+71} L578 {y+71} Z',INK,SAND if y==130 else PALE)
s+=text(130,413,'Visual query',27)+text(374,413,'Refine',27)+text(643,413,'Matches',27)
save('conversational-search','Visual search through conversation','A visual query and a conversation bubble guide a network toward refined image matches. Conceptual illustration, not a literal interface or architecture.',s,PATENTS)

# Human cues guide the location of the interacted object.
s=scene(45,170)+arrow(237,250,294,250)+network(329,207,111,86,PAPER,SAGE)+arrow(474,250,529,250)+scene(573,170,True)
s+=text(131,413,'Human cues',27)+text(385,413,'Locate',27)+text(657,413,'Object',27)
save('object-localization','Locating an interacted object','Human and hand cues pass through a conceptual network, highlighting the interacted object in the image.',s,PATENTS)

# Distinct subject and object branches meet in a relation representation.
s=box(60,129,142,112,PAPER,INK,10)+human(127,181)
s+=box(60,276,142,99,PAPER,INK,10)+box(111,301,40,49,SAND,CLAY,6)
s+=path('M223 185 C268 185 264 250 307 250',SAGE)+path('M223 326 C268 326 264 250 307 250',CLAY)
s+=network(334,208,113,84,PAPER,SAGE)+arrow(476,250,536,250)
s+=circle(589,250,22,PALE,SAGE)+circle(715,250,22,SAND,CLAY)+line(613,250,690,250)+circle(652,250,8,PAPER,INK)
s+=text(131,100,'Subject',25)+text(131,417,'Object',25)+text(391,417,'Recognize',25)+text(651,417,'Interaction',25)
save('interaction-recognition','Recognizing subject-object interactions','Subject and object branches converge in a network and form a relationship representation. A conceptual view of interaction recognition.',s,PATENTS)

# Surrounding scene context informs learning about a human-object pair.
s=box(54,118,224,246,PAPER,INK,12)
s+=line(73,309,257,309,STONE)+box(78,146,52,55,PALE,SAGE,5)+line(104,146,104,201,SAGE)+line(78,174,130,174,SAGE)
s+=human(146,241)+box(185,230,35,43,SAND,CLAY,5)
s+=box(106,181,130,130,'none',SAGE,8,extra='stroke-dasharray="6 8"')
s+=arrow(303,250,357,250)+network(390,206,105,88,PAPER,SAGE)+arrow(526,250,578,250)
s+=box(607,179,135,143,PAPER,INK,12)+human(645,241)+box(689,232,27,35,SAND,CLAY,5)
s+=path('M647 185 C679 168 708 183 710 207',SAGE)+path('M710 207 L701 199 M710 207 L716 197',SAGE)
s+=text(167,413,'Scene context',27)+text(444,413,'Learn',27)+text(675,413,'Interaction',27)
save('context-learning','Learning interactions from context','Surrounding scene information informs a network learning about a human-object interaction. Conceptual illustration, not a performance result.',s,PATENTS)
print(f'Wrote four patent SVG illustrations to {PATENTS}')
