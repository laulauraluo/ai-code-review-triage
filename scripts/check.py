"""Checks CI runs: skill frontmatter against the Agent Skills spec, evals, local links, and the runnable example."""
import json, pathlib, re, subprocess, sys

root = pathlib.Path(__file__).resolve().parent.parent
errors = []

skill = root / "skills/looks-good-to-ai/SKILL.md"
m = re.match(r"---\n(.*?)\n---\n", skill.read_text(), re.S)
fm = dict(line.split(": ", 1) for line in m.group(1).splitlines()) if m else {}
name, desc = fm.get("name", ""), fm.get("description", "")
if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
    errors.append(f"name {name!r} breaks the Agent Skills name rules")
if name != skill.parent.name:
    errors.append(f"name {name!r} must match its folder {skill.parent.name!r}")
if not 1 <= len(desc) <= 1024:
    errors.append(f"description is {len(desc)} chars, must be 1-1024")
if len(fm.get("compatibility", "")) > 500:
    errors.append("compatibility is over 500 chars")

ext = json.loads((root / "gemini-extension.json").read_text())
plugin = json.loads((root / ".claude-plugin/plugin.json").read_text())
if (ext.get("name"), ext.get("version")) != (name, plugin["version"]):
    errors.append("gemini-extension.json name/version must match the skill name and plugin.json version")

for e in json.loads((root / "evals/evals.json").read_text())["evals"]:
    if not e.get("prompt") or not e.get("expected_output"):
        errors.append(f"eval {e.get('id')} needs prompt and expected_output")

for md in root.rglob("*.md"):
    if ".git" in md.parts:
        continue
    for target in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", md.read_text()):
        if not re.match(r"[a-z]+:", target) and not (md.parent / target).exists():
            errors.append(f"{md.relative_to(root)}: broken link {target}")

walk = (root / "examples/pagination-limit-walkthrough.md").read_text()
code = re.search(r"python3 - <<'PY'\n(.*?)\nPY", walk, re.S).group(1)
run = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True)
if run.returncode:
    errors.append("pagination reproduction failed:\n" + run.stderr)

print("\n".join(errors) or "all checks passed")
sys.exit(bool(errors))
