"""Create the self-contained terminal profile card SVG."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "info-card.svg"
ROWS = [
    ("name", "Aswin Unni P B"),
    ("role", "Senior DevOps Engineer"),
    ("experience", "4+ years · production platforms"),
    ("now", "Healthcare cloud-native systems"),
    ("cloud", "AWS · GCP · hybrid cloud"),
    ("orchestration", "Kubernetes · Helm · Karpenter"),
    ("automation", "Terraform · Ansible · CI/CD · GitOps"),
    ("observe", "Prometheus · Grafana · CloudWatch"),
]


def main() -> None:
    row_svg = []
    for index, (key, value) in enumerate(ROWS):
        y = 68 + index * 34
        delay = index * 0.14
        row_svg.append(f'''<g style="animation:line .35s {delay:.2f}s both">
  <text x="28" y="{y}" class="key">{key}</text><text x="176" y="{y}" class="colon">:</text><text x="192" y="{y}" class="value">{value}</text>
</g>''')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="490" height="358" viewBox="0 0 490 358" role="img" aria-label="Aswin Unni P B profile">
  <style>
    .title {{ fill:#58a6ff; font:600 16px ui-monospace, SFMono-Regular, Menlo, monospace }}
    .key {{ fill:#7ee787; font:14px ui-monospace, SFMono-Regular, Menlo, monospace }}
    .colon {{ fill:#8b949e; font:14px ui-monospace, SFMono-Regular, Menlo, monospace }}
    .value {{ fill:#c9d1d9; font:14px ui-monospace, SFMono-Regular, Menlo, monospace }}
    @keyframes line {{ from {{ opacity:0; transform:translateX(-8px) }} to {{ opacity:1; transform:translateX(0) }} }}
  </style>
  <rect width="490" height="358" rx="10" fill="#0d1117" stroke="#30363d"/>
  <circle cx="24" cy="24" r="5" fill="#ff7b72"/><circle cx="42" cy="24" r="5" fill="#d29922"/><circle cx="60" cy="24" r="5" fill="#3fb950"/>
  <text x="88" y="30" class="title">aswin@github:~$ neofetch</text>
  <line x1="24" y1="45" x2="466" y2="45" stroke="#30363d"/>
  {''.join(row_svg)}
</svg>'''
    OUTPUT.write_text(svg + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
