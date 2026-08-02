import os

def create_info_card(output_path="info-card.svg"):
    width = 490
    height = 560

    lines = [
        {"type": "prompt", "text": "nikhil@github ~ $ neofetch --system"},
        {"type": "separator", "text": "----------------------------------------"},
        {"type": "header", "label": "USER", "val": "Nikhil Chalamalla"},
        {"type": "kv", "label": "Role", "val": "Java Full Stack & Backend Engineer"},
        {"type": "kv", "label": "Education", "val": "B.Tech CSE Student"},
        {"type": "kv", "label": "Specialization", "val": "Backend Systems & System Design"},
        {"type": "kv", "label": "Primary Stack", "val": "Java, SpringBoot, React.js, Express"},
        {"type": "kv", "label": "Databases", "val": "MongoDB, MySQL, PostgreSQL, Oracle"},
        {"type": "kv", "label": "Cloud & DevOps", "val": "AWS, Azure, Docker, Kubernetes, Jenkins"},
        {"type": "kv", "label": "Algorithms", "val": "360+ LeetCode Solved 🧠"},
        {"type": "kv", "label": "Core Project", "val": "Real-Time Chat App (SpringBoot+STOMP)"},
        {"type": "kv", "label": "Goal", "val": "Building High-Throughput Cloud Systems 🚀"},
        {"type": "separator", "text": "----------------------------------------"},
        {"type": "palette"}
    ]

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('<style>')
    svg.append('  .bg { fill: #0d1117; rx: 10px; ry: 10px; stroke: #30363d; stroke-width: 1; }')
    svg.append('  .dot { rx: 50%; ry: 50%; }')
    svg.append('  .title-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 11px; fill: #8b949e; font-weight: 600; }')
    svg.append('  .prompt { font-family: "Cascadia Code", "Fira Code", Consolas, monospace; font-size: 12px; fill: #39d353; font-weight: bold; }')
    svg.append('  .sep { font-family: "Cascadia Code", "Fira Code", Consolas, monospace; font-size: 12px; fill: #30363d; }')
    svg.append('  .header-name { font-family: "Cascadia Code", "Fira Code", Consolas, monospace; font-size: 14px; fill: #58a6ff; font-weight: bold; }')
    svg.append('  .key { font-family: "Cascadia Code", "Fira Code", Consolas, monospace; font-size: 12px; fill: #79c0ff; font-weight: bold; }')
    svg.append('  .val { font-family: "Cascadia Code", "Fira Code", Consolas, monospace; font-size: 12px; fill: #c9d1d9; }')
    svg.append('  .highlight-val { font-family: "Cascadia Code", "Fira Code", Consolas, monospace; font-size: 12px; fill: #f0883e; font-weight: 500; }')
    svg.append('</style>')

    # Card Background & Header Bar
    svg.append(f'  <rect class="bg" x="0" y="0" width="{width}" height="{height}" />')
    svg.append('  <circle class="dot" cx="16" cy="16" r="5" fill="#ff5f56" />')
    svg.append('  <circle class="dot" cx="30" cy="16" r="5" fill="#ffbd2e" />')
    svg.append('  <circle class="dot" cx="44" cy="16" r="5" fill="#27c93f" />')
    svg.append(f'  <text class="title-text" x="{width//2}" y="20" text-anchor="middle">nikhil@system:~ (neofetch)</text>')
    svg.append(f'  <line x1="0" y1="30" x2="{width}" y2="30" stroke="#30363d" stroke-width="1" />')

    y_start = 55
    y_step = 34
    
    for i, item in enumerate(lines):
        y = y_start + i * y_step
        begin_sec = 0.15 + i * 0.12
        anim_tag = f'<animate attributeName="opacity" from="0" to="1" dur="0.35s" begin="{begin_sec:.2f}s" fill="freeze" />'

        if item["type"] == "prompt":
            svg.append(f'  <text class="prompt" x="20" y="{y}" opacity="0">{item["text"]}{anim_tag}</text>')
        elif item["type"] == "separator":
            svg.append(f'  <text class="sep" x="20" y="{y}" opacity="0">{item["text"]}{anim_tag}</text>')
        elif item["type"] == "header":
            svg.append(f'  <text class="header-name" x="20" y="{y}" opacity="0">⚡ {item["val"]}{anim_tag}</text>')
        elif item["type"] == "kv":
            is_hl = item["label"] in ["Highlight", "Core Project", "Goal", "Algorithms"]
            val_class = "highlight-val" if is_hl else "val"
            svg.append(f'  <text x="20" y="{y}" opacity="0">')
            svg.append(f'    <tspan class="key">{item["label"]}: </tspan>')
            svg.append(f'    <tspan class="{val_class}">{item["val"]}</tspan>')
            svg.append(f'    {anim_tag}')
            svg.append('  </text>')
        elif item["type"] == "palette":
            colors = ["#ff5f56", "#ffbd2e", "#27c93f", "#58a6ff", "#bc8cff", "#f0883e", "#39d353", "#79c0ff"]
            svg.append(f'  <g opacity="0">')
            svg.append(f'    {anim_tag}')
            for c_idx, col in enumerate(colors):
                cx = 20 + c_idx * 26
                svg.append(f'    <rect x="{cx}" y="{y - 10}" width="20" height="14" rx="3" fill="{col}" />')
            svg.append('  </g>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
        
    print(f"SMIL-animated Info Card SVG generated at: {output_path}")

if __name__ == "__main__":
    create_info_card("info-card.svg")
