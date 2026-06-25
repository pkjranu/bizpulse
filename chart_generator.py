import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
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
        pctdistance=0.85, labeldistance=1.1
    )
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