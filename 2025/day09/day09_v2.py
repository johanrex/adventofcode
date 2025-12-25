import plotly.graph_objects as go


def parse(filename: str) -> list[tuple[int, int]]:
    polygon = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            row, col = line.split(",")
            polygon.append((int(row), int(col)))

    return polygon


def plot_polygon(polygon) -> go.Figure:
    texts = [f"({r}, {c})" for r, c in polygon]
    texts_closed = texts + [texts[0]]

    fig = go.Figure()
    # when building traces
    x = [c for (r, c) in polygon]  # cols
    y = [r for (r, c) in polygon]  # rows

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines+markers",
            name="Polygon",
            text=texts_closed,
            hovertemplate="%{text}<extra></extra>",
        )
    )
    # once per figure
    fig.update_yaxes(autorange="reversed")
    fig.update_xaxes(title_text="col")
    fig.update_yaxes(title_text="row", autorange="reversed", scaleanchor="x", scaleratio=1)

    return fig


def plot_rectangle(fig: go.Figure, p1, p2) -> go.Figure:
    r1, c1 = p1
    r2, c2 = p2

    rows = [r1, r1, r2, r2, r1]
    cols = [c1, c2, c2, c1, c1]

    x = cols
    y = rows
    texts = [f"({r}, {c})" for r, c in zip(rows, cols)]

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines+markers",
            name="Max rectangle",
            line=dict(color="red"),
            marker=dict(color="red"),
            text=texts,
            hovertemplate="%{text}<extra></extra>",
        )
    )
    return fig


def is_point_inside_polygon(row, col, vertical_lines) -> bool:
    """
    Determines if the point is inside the polygon by using ray-casting.
    Cast a ray from the starting point to the right and count how many times it crosses vertical polygon edges.
    This is slightly different than a normal grid based approach.
    """
    crosses_cnt = 0
    for line in vertical_lines:
        p1, p2 = line
        s_col = p1[1]
        s_min_row = min(p1[0], p2[0])
        s_max_row = max(p1[0], p2[0])

        if s_min_row < row < s_max_row and col <= s_col:
            crosses_cnt += 1

    return crosses_cnt % 2 == 1


def part1(polygon):
    max_area = -1
    for i in range(len(polygon)):
        r1, c1 = polygon[i]
        for j in range(i + 1, len(polygon)):
            r2, c2 = polygon[j]

            area = (abs(c1 - c2) + 1) * (abs(r1 - r2) + 1)
            max_area = max(max_area, area)

    print("Part 1:", max_area)


def part2(polygon):
    # visual inspection of input data to find two inner points
    a = (94808, 48629)
    b = (94808, 50147)

    max_area = -1
    # max_p1 = None
    # max_p2 = None

    # vertical line segments for ray casting
    vertical_line_segments = []
    for i in range(len(polygon)):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % len(polygon)]
        if p1[1] == p2[1]:
            vertical_line_segments.append((p1, p2))

    for far_corner in polygon:
        if far_corner[1] < a[1]:
            inner_corner = a
        elif far_corner[1] > b[1]:
            inner_corner = b
        else:
            continue

        area = (abs(inner_corner[0] - far_corner[0]) + 1) * (abs(inner_corner[1] - far_corner[1]) + 1)

        if area > max_area:
            if not is_point_inside_polygon(inner_corner[0], far_corner[1], vertical_line_segments):
                continue
            if not is_point_inside_polygon(far_corner[0], inner_corner[1], vertical_line_segments):
                continue

            max_area = area
            # max_p1 = inner_corner
            # max_p2 = far_corner

    # fig = plot_polygon(polygon)
    # fig = plot_rectangle(fig, max_p1, max_p2)
    # fig.show()

    assert max_area == 1473551379
    print("Part 2:", max_area)


filename = "day09/example"
filename = "day09/input"

polygon = parse(filename)
part1(polygon)
part2(polygon)
