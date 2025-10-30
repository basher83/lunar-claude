#!/usr/bin/env python3
"""
Extract and structure documentation for AI consumption
"""
import subprocess
import json
from pathlib import Path
from datetime import datetime


class DocExtractor:
    def __init__(self, output_dir: str = "~/.ai-docs"):
        self.output_dir = Path(output_dir).expanduser()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def jina_extract(self, url: str, project: str, section: str):
        """Extract single page using Jina Reader"""
        project_dir = self.output_dir / project / section
        project_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename from URL
        filename = url.split('/')[-1] or 'index'
        if not filename.endswith('.md'):
            filename += '.md'

        output_path = project_dir / filename

        # Use Jina Reader
        jina_url = f"https://r.jina.ai/{url}"
        result = subprocess.run(
            ['curl', '-s', jina_url],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            # Add metadata header
            content = f"""---
source: {url}
extracted: {datetime.now().isoformat()}
project: {project}
section: {section}
---

{result.stdout}
"""
            output_path.write_text(content)
            print(f"✓ Saved: {output_path}")
            return str(output_path)
        else:
            print(f"✗ Failed: {url}")
            return None

    def extract_repo(self, repo_url: str, project: str):
        """Extract entire GitHub repo using Repomix"""
        project_dir = self.output_dir / project
        project_dir.mkdir(parents=True, exist_ok=True)

        output_path = project_dir / "repo-full.md"

        result = subprocess.run(
            [
                'repomix',
                '--style', 'markdown',
                '--output', str(output_path),
                repo_url
            ],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"✓ Repo saved: {output_path}")
            return str(output_path)
        else:
            print(f"✗ Failed: {repo_url}")
            return None


# Example usage
if __name__ == "__main__":
    extractor = DocExtractor()

    # Extract Proxmox documentation
    extractor.jina_extract(
        "https://pve.proxmox.com/pve-docs/chapter-pveceph.html",
        project="proxmox",
        section="ceph"
    )

    # Extract Terraform provider docs
    extractor.extract_repo(
        "https://github.com/bpg/terraform-provider-proxmox",
        project="terraform-proxmox"
    )
