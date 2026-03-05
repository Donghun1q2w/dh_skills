# Graph Shape Types for math-hwpx

`graph_generator.py` supports function graphs (polynomial, trig, etc.) plus 5 geometry shape types.
Specify these in the problem JSON `graph` field to auto-generate PNG images.

## Table of Contents

- [triangle](#triangle)
- [circle](#circle)
- [quadrilateral](#quadrilateral)
- [coordinate](#coordinate)
- [solid3d](#solid3d)

---

## triangle

Defined by 3 vertex coordinates. Supports angle arcs, side labels, auxiliary lines (median/altitude/bisector), circumcircle, and incircle.

```json
{
  "type": "triangle",
  "vertices": [[0, 0], [6, 0], [2, 5]],
  "labels": {"A": [2, 5], "B": [0, 0], "C": [6, 0]},
  "show_angles": [true, true, true],
  "angle_labels": ["80\u00b0", "50\u00b0", "50\u00b0"],
  "side_labels": {"AB": "5", "BC": "6", "AC": "5"},
  "equal_marks": {"AB": 1, "AC": 1},
  "show_circumcircle": false,
  "show_incircle": false,
  "auxiliary_lines": [{"type": "bisector", "vertex": "B"}]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `vertices` | Yes | 3 vertex coordinates `[[x,y], [x,y], [x,y]]` |
| `labels` | No | Vertex name-to-coordinate mapping |
| `show_angles` | No | Show angle arc per vertex `[bool, bool, bool]` |
| `angle_labels` | No | Angle labels (e.g., `["80\u00b0", "50\u00b0", "50\u00b0"]`) |
| `side_labels` | No | Side name-to-length label (e.g., `{"AB": "5"}`) |
| `equal_marks` | No | Side name-to-tick count (e.g., `{"AB": 1, "AC": 1}`) |
| `show_circumcircle` | No | Show circumscribed circle |
| `show_incircle` | No | Show inscribed circle |
| `auxiliary_lines` | No | Array of `{type, vertex}`. type: `"median"`, `"altitude"`, `"bisector"` |

---

## circle

Center, radius, points on circle, chords, tangent lines, arc highlights, central/inscribed angles.

```json
{
  "type": "circle",
  "center": [0, 0],
  "radius": 3,
  "show_center": true,
  "points_on_circle": [
    {"angle_deg": 30, "label": "A"},
    {"angle_deg": 150, "label": "B"}
  ],
  "chords": [["A", "B"]],
  "tangent_at": ["A"],
  "arc_highlight": {"from": "A", "to": "B", "color": "gray"},
  "central_angle": true,
  "inscribed_angle": {"vertex": "C", "arc": ["A", "B"]}
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `center` | No | Center coordinates (default: `[0,0]`) |
| `radius` | No | Radius (default: 3) |
| `show_center` | No | Show center point O |
| `points_on_circle` | No | Points array `{angle_deg, label}` |
| `chords` | No | Chords `[["A","B"]]` |
| `tangent_at` | No | Tangent line at named point |
| `arc_highlight` | No | Arc highlight `{from, to, color}` |
| `central_angle` | No | Show central angle segments |
| `inscribed_angle` | No | Inscribed angle `{vertex, arc: [A, B]}` |

---

## quadrilateral

4 vertex coordinates. Supports diagonals, parallel marks, equal marks, right angle marks.

```json
{
  "type": "quadrilateral",
  "kind": "parallelogram",
  "vertices": [[0, 0], [5, 0], [7, 3], [2, 3]],
  "labels": {"A": [0, 0], "B": [5, 0], "C": [7, 3], "D": [2, 3]},
  "show_diagonals": true,
  "diagonal_intersection_label": "O",
  "parallel_marks": {"AB_DC": 1, "AD_BC": 2},
  "equal_marks": {"AB": 1, "DC": 1},
  "show_right_angles": [],
  "side_labels": {"AB": "10", "BC": "6"}
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `vertices` | Yes | 4 vertex coordinates |
| `kind` | No | Reference kind name (parallelogram, rectangle, etc.) |
| `labels` | No | Vertex name-to-coordinate mapping |
| `show_diagonals` | No | Show dashed diagonals |
| `diagonal_intersection_label` | No | Diagonal intersection label |
| `parallel_marks` | No | Parallel marks `{"AB_DC": 1}` (AB parallel DC, 1 arrow) |
| `equal_marks` | No | Equal tick marks |
| `show_right_angles` | No | Vertex names for right angle marks |
| `side_labels` | No | Side length labels |

---

## coordinate

Coordinate axes with segments, polygons, points, lines, and circles.

```json
{
  "type": "coordinate",
  "xlim": [-1, 7],
  "ylim": [-1, 7],
  "segments": [[[0, 6], [2, 0]], [[2, 0], [6, 0]], [[0, 6], [6, 0]]],
  "points": [
    {"pos": [0, 6], "label": "(0, 6)"},
    {"pos": [2, 0], "label": "(2, 0)"}
  ],
  "fill_polygon": [[0, 6], [2, 0], [6, 0]],
  "shade_alpha": 0.15,
  "lines": [{"slope": -3, "intercept": 6, "style": "k-"}],
  "circles": [{"center": [3, 3], "radius": 2}]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `xlim`, `ylim` | No | Axis range |
| `segments` | No | Segment array `[[[x1,y1],[x2,y2]], ...]` |
| `points` | No | Point array `{pos, label}` |
| `fill_polygon` | No | Polygon vertices to fill |
| `shade_alpha` | No | Fill opacity (default: 0.15) |
| `lines` | No | Lines `{slope, intercept, style}` |
| `circles` | No | Circles `{center, radius}` |

---

## solid3d

2D oblique projection of 3D solids, exam-style. Hidden edges shown as dashed lines.

```json
{
  "type": "solid3d",
  "kind": "cylinder",
  "params": {"radius": 2, "height": 4},
  "labels": {"r": "2", "h": "4"},
  "show_hidden": true
}
```

**Supported kinds**: `cylinder`, `cone`, `sphere`, `rectangular_prism`, `triangular_prism`, `pyramid`

| Field | Required | Description |
|-------|----------|-------------|
| `kind` | No | Solid type (default: `"cylinder"`) |
| `params` | No | Type-specific parameters |
| `labels` | No | Dimension labels (e.g., `{"r": "2", "h": "4"}`) |
| `show_hidden` | No | Show hidden edges as dashed (default: true) |

**Parameters by kind**:
- `cylinder`: `{radius, height}`
- `cone`: `{radius, height}`
- `sphere`: `{radius}`
- `rectangular_prism`: `{width, height, depth}`
- `triangular_prism`: `{base, height, depth}`
- `pyramid`: `{base, height, depth}`
