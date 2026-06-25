import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io


def generate_pipeline_chart(data: dict) -> bytes:
    """Generate a bar chart of pipeline by stage."""
    stages = list(data.keys())
    values = list(data.values())
    colors = ['#2ecc71' if 'Won' in s else '#e74c3c' if 'Lost' in s
              else '#3498db' for s in stages]
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(stages, values, color=colors)
    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + max(values) * 0.01, bar.get_y() + bar.get_height() / 2,
                f'${val:,.0f}', va='center', fontsize=10, fontweight='bold')
    ax.set_xlabel('Deal Value (USD)', fontsize=12)
    ax.set_title('📊 Pipeline by Stage', fontsize=14, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return buf.read()


def generate_pie_chart(data: dict, title: str) -> bytes:
    """Generate a pie chart."""
    labels = list(data.keys())
    values = list(data.values())
    colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c']
    fig, ax = plt.subplots(figsize=(9, 7))
    wedges, texts, autotexts = ax.pie(
        values, labels=labels, colors=colors[:len(labels)],
        autopct='%1.1f%%', startangle=90,
        pctdistance=0.85, labeldistance=1.1)
    for text in autotexts:
        text.set_fontsize(10)
        text.set_fontweight('bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return buf.read()


def generate_leaderboard_chart(data: dict, title: str) -> bytes:
    """Generate a horizontal bar leaderboard chart."""
    names = list(data.keys())[:8]
    values = list(data.values())[:8]
    colors = ['#f39c12' if i == 0 else '#95a5a6' if i == 1
              else '#cd7f32' if i == 2 else '#3498db'
              for i in range(len(names))]
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(names[::-1], values[::-1], color=colors[::-1])
    for bar, val in zip(bars, values[::-1]):
        ax.text(bar.get_width() + max(values) * 0.01,
                bar.get_y() + bar.get_height() / 2,
                f'${val:,.0f}', va='center', fontsize=10, fontweight='bold')
    ax.set_xlabel('Value (USD)', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return buf.read()


def generate_line_chart(data: dict, title: str) -> bytes:
    """Generate a line chart for trends."""
    labels = list(data.keys())
    values = list(data.values())
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(labels, values, color='#3498db', linewidth=2.5,
            marker='o', markersize=8, markerfacecolor='#e74c3c')
    ax.fill_between(range(len(labels)), values, alpha=0.1, color='#3498db')
    for i, (label, val) in enumerate(zip(labels, values)):
        ax.annotate(f'${val:,.0f}', (i, val),
                    textcoords="offset points", xytext=(0, 10),
                    ha='center', fontsize=9, fontweight='bold')
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.set_xlabel('Period', fontsize=12)
    ax.set_ylabel('Value (USD)', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return buf.read()


def generate_funnel_chart(data: dict, title: str) -> bytes:
    """Generate a funnel chart for sales pipeline conversion."""
    stages = list(data.keys())
    values = list(data.values())
    max_val = max(values)
    fig, ax = plt.subplots(figsize=(10, 7))
    colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6']
    bar_height = 0.6
    for i, (stage, val) in enumerate(zip(stages, values)):
        width = (val / max_val)
        left = (1 - width) / 2
        ax.barh(i, width, left=left, height=bar_height,
                color=colors[i % len(colors)], alpha=0.85)
        ax.text(0.5, i, f'{stage}: ${val:,.0f}',
                ha='center', va='center', fontsize=8,
                fontweight='bold', color='white', clip_on=True)
    ax.set_xlim(0, 1)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    for i in range(len(values) - 1):
        rate = (values[i + 1] / values[i] * 100) if values[i] > 0 else 0
        ax.text(0.98, i + 0.5, f'↓ {rate:.0f}%',
                ha='right', va='center', fontsize=9,
                color='#7f8c8d', style='italic')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return buf.read()


def generate_heatmap(data: dict, title: str) -> bytes:
    """Generate a heatmap chart."""
    import numpy as np
    rows = []
    cols = []
    for key in data.keys():
        if '|' in key:
            r, c = key.split('|', 1)
            if r not in rows:
                rows.append(r)
            if c not in cols:
                cols.append(c)
    if not rows or not cols:
        return generate_pipeline_chart(data)
    matrix = np.zeros((len(rows), len(cols)))
    for key, val in data.items():
        if '|' in key:
            r, c = key.split('|', 1)
            matrix[rows.index(r)][cols.index(c)] = val
    fig, ax = plt.subplots(figsize=(10, 7))
    im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto')
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels(cols, rotation=45, ha='right', fontsize=9)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels(rows, fontsize=9)
    for i in range(len(rows)):
        for j in range(len(cols)):
            val = matrix[i][j]
            ax.text(j, i, f'${val:,.0f}' if val > 0 else '-',
                    ha='center', va='center', fontsize=8,
                    fontweight='bold',
                    color='white' if val > matrix.max() * 0.6 else 'black')
    plt.colorbar(im, ax=ax, label='Value (USD)')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return buf.read()