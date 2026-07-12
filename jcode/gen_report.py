import json, os, datetime

USERPROFILE = os.environ.get("USERPROFILE", "C:\\Users\\guohua")
OUT_PATH = r"F:\OneDrive\Project\DOCS\jcode\jcode_session.md"
JCODE_DIR = os.path.join(USERPROFILE, ".jcode", "sessions")
CODEX_DIR = os.path.join(USERPROFILE, ".codex", "sessions")
CONTINUE_DIR = os.path.join(USERPROFILE, ".continue", "sessions")

results = []

def parse_jcode(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
    except Exception:
        return None
    msgs = data.get("messages", [])
    return {
        "source": "jcode",
        "file": os.path.basename(path),
        "title": data.get("title") or "",
        # custom_title is the user-renamed session name
        "name": data.get("custom_title") or data.get("short_name") or data.get("name") or "",
        "total": len(msgs),
        "user": sum(1 for m in msgs if m.get("role") == "user"),
        "ai": sum(1 for m in msgs if m.get("role") == "assistant"),
        "created": data.get("created_at", ""),
        "wd": data.get("working_dir") or "",
        "provider": data.get("provider_key", "jcode"),
    }

def parse_codex(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            lines = f.readlines()
    except Exception:
        return None
    sid = ctime = cwd = provider = ""
    uc = ac = 0
    for line in lines:
        line = line.strip()
        if not line: continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        t, pl = obj.get("type", ""), obj.get("payload", {})
        if t == "session_meta":
            sid = pl.get("id", "")
            ctime = pl.get("timestamp", "")
            cwd = pl.get("cwd", "")
            provider = pl.get("model_provider", "")
        elif t == "response_item" and pl.get("type") == "message":
            r = pl.get("role", "")
            if r == "user": uc += 1
            elif r == "assistant": ac += 1
    return {
        "source": "codex",
        "file": os.path.basename(path),
        "name": "",
        "title": "Codex session",
        "total": uc + ac,
        "user": uc,
        "ai": ac,
        "created": ctime,
        "wd": cwd,
        "provider": provider or "codex",
    }

def parse_continue(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
    except Exception:
        return None
    hist = data.get("history", [])
    uc = sum(1 for h in hist if h.get("message", {}).get("role") == "user")
    ac = sum(1 for h in hist if h.get("message", {}).get("role") == "assistant")
    return {
        "source": "continue",
        "file": os.path.basename(path),
        "name": "",
        "title": data.get("title", ""),
        "total": uc + ac,
        "user": uc,
        "ai": ac,
        "wd": data.get("workspaceDirectory", ""),
        "provider": "continue",
    }

# Collect
if os.path.isdir(JCODE_DIR):
    for fn in os.listdir(JCODE_DIR):
        if not fn.endswith(".json") or fn.endswith(".bak") or ".journal" in fn:
            continue
        r = parse_jcode(os.path.join(JCODE_DIR, fn))
        if r: results.append(r)

if os.path.isdir(CODEX_DIR):
    for root, dirs, files in os.walk(CODEX_DIR):
        for fn in files:
            if fn.endswith(".jsonl"):
                r = parse_codex(os.path.join(root, fn))
                if r: results.append(r)

if os.path.isdir(CONTINUE_DIR):
    for fn in os.listdir(CONTINUE_DIR):
        if not fn.endswith(".json") or fn == "sessions.json":
            continue
        r = parse_continue(os.path.join(CONTINUE_DIR, fn))
        if r: results.append(r)

total = len(results)
tmsgs = sum(r["total"] for r in results)
jrs = [r for r in results if r["source"] == "jcode"]
crs = [r for r in results if r["source"] == "codex"]
nrs = [r for r in results if r["source"] == "continue"]
now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

lines = [
    "# AI Session Analysis Report",
    "",
    "**Generated**: %s" % now_str,
    "**Total Sessions**: %d (Jcode: %d, Codex: %d, Continue: %d)" % (total, len(jrs), len(crs), len(nrs)),
    "**Total Messages**: %d" % tmsgs,
    "",
    "---",
    "",
]

# Section 1: Jcode
lines.append("## 1. Jcode Native Sessions")
lines.append("")
lines.append("%d sessions from jcode." % len(jrs))
lines.append("")
# Table with name and work_dir added
lines.append("| # | Name | Session File | Model/Provider | Messages | User | AI | Work Dir | Created At |")
lines.append("|---|------|-------------|---------------|----------|------|----|----------|-----------|")
for idx, s in enumerate(sorted(jrs, key=lambda r: r["created"], reverse=True), 1):
    name = s["name"] or "-"
    sfile = s["file"].replace(".json", "")
    wd = s["wd"] or "-"
    lines.append("| %d | %s | %s | %s | %d | %d | %d | %s | %s |" % (idx, name, sfile, s["provider"], s["total"], s["user"], s["ai"], wd, s["created"]))

lines.append("")
lines.append("### Top 10 by Messages")
lines.append("")
lines.append("| # | Name | Messages | User | AI | Created At |")
lines.append("|---|------|----------|------|----|-----------|")
for idx, s in enumerate(sorted(jrs, key=lambda r: -r["total"])[:10], 1):
    name = s["name"] or s["file"].replace("session_", "").replace(".json", "")[:20]
    lines.append("| %d | %s | %d | %d | %d | %s |" % (idx, name, s["total"], s["user"], s["ai"], s["created"]))

# Section 2: Codex
lines.append("")
lines.append("## 2. Codex Sessions")
if crs:
    lines.append("")
    lines.append("%d sessions from Codex CLI (JSONL format)." % len(crs))
    lines.append("")
    lines.append("| # | Session ID | Title | Model | Messages | User Msgs | AI Msgs | Work Dir | Created At |")
    lines.append("|---|-----------|-------|-------|----------|----------|---------|---------|-----------|")
    for idx, s in enumerate(sorted(crs, key=lambda r: r["created"], reverse=True), 1):
        sid = (s["file"][:8] + "...")
        title = (s["title"] or "-")[:40].replace("|", "/")
        wd = os.path.basename(s["wd"]) or "-"
        lines.append("| %d | %s | %s | %s | %d | %d | %d | %s | %s |" % (idx, sid, title, s["provider"], s["total"], s["user"], s["ai"], wd, s["created"]))
else:
    lines.append("")
    lines.append("_No Codex sessions found._")

# Section 3: Continue
lines.append("")
lines.append("## 3. Continue Sessions")
if nrs:
    lines.append("")
    lines.append("%d sessions from Continue (JSON with history[])." % len(nrs))
    lines.append("")
    lines.append("| # | Session ID | Title | Messages | User Msgs | AI Msgs | Work Dir |")
    lines.append("|---|-----------|-------|----------|----------|---------|---------|")
    for idx, s in enumerate(sorted(nrs, key=lambda r: -r["total"]), 1):
        sid = (s["file"][:8] + "...")
        title = (s["title"] or "-")[:40].replace("|", "/")
        wd = os.path.basename(s["wd"]) or "-"
        lines.append("| %d | %s | %s | %d | %d | %d | %s |" % (idx, sid, title, s["total"], s["user"], s["ai"], wd))
else:
    lines.append("")
    lines.append("_No Continue sessions found._")

# Section 4: Residual files
residuals = {}
if os.path.isdir(JCODE_DIR):
    active_bases = set()
    for fn in os.listdir(JCODE_DIR):
        if fn.endswith(".json") and ".journal" not in fn:
            active_bases.add(fn[:-len(".json")])
    orphan_groups = {}
    for fn in os.listdir(JCODE_DIR):
        base = None
        if fn.endswith(".bak"):
            base = fn[:-len(".bak")]
        elif fn.endswith(".journal.jsonl"):
            base = fn[:-len(".journal.jsonl")]
        if base:
            orphan_groups.setdefault(base, []).append(fn)
    for base, files in sorted(orphan_groups.items()):
        if base not in active_bases:
            residuals[base] = files

if residuals:
    lines.append("")
    lines.append("## 4. Residual / Ghost Files")
    lines.append("")
    lines.append("These are leftover files (`.bak` or `.journal.jsonl`) without a corresponding `.json` session file. They can be safely deleted.")
    lines.append("")
    lines.append("| # | Session ID | Orphan Files |")
    lines.append("|---|-----------|-------------|")
    total_res = len(residuals)
    for idx, (base, files) in enumerate(residuals.items(), 1):
        fstr = ", ".join(files)
        lines.append("| %d | %s | %s |" % (idx, base, fstr))
    lines.append("")
    lines.append("**Total residual entries: %d**" % total_res)

# Section 5: Summary
lines.append("")
lines.append("## 5. Summary Statistics")
lines.append("")
lines.append("| Metric | Value |")
lines.append("|--------|-------|")
jmsgs = sum(r["total"] for r in jrs)
cmsgs = sum(r["total"] for r in crs)
nmsgs = sum(r["total"] for r in nrs)
lines.append("| Jcode Sessions | %d |" % len(jrs))
lines.append("| Jcode Messages | %d |" % jmsgs)
lines.append("| Codex Sessions | %d |" % len(crs))
lines.append("| Codex Messages | %d |" % cmsgs)
lines.append("| Continue Sessions | %d |" % len(nrs))
lines.append("| Continue Messages | %d |" % nmsgs)
lines.append("| **Total Sessions** | **%d** |" % total)
lines.append("| **Total Messages** | **%d** |" % tmsgs)
if total > 0:
    lines.append("| Avg Messages/Session | %.1f |" % (tmsgs / total))
lines.append("| Sessions with Title | %d |" % sum(1 for r in results if r["title"]))

lines.append("")
lines.append("### Activity Distribution")
lines.append("")
lines.append("| Msg Count Range | Sessions | %% |")
lines.append("|----------------|----------|---|")
r1 = sum(1 for r in results if 1 <= r["total"] <= 5)
r2 = sum(1 for r in results if 6 <= r["total"] <= 20)
r3 = sum(1 for r in results if 21 <= r["total"] <= 50)
r4 = sum(1 for r in results if r["total"] > 50)
lines.append("| 1-5 | %d | %.1f%% |" % (r1, r1/total*100))
lines.append("| 6-20 | %d | %.1f%% |" % (r2, r2/total*100))
lines.append("| 21-50 | %d | %.1f%% |" % (r3, r3/total*100))
lines.append("| 50+ | %d | %.1f%% |" % (r4, r4/total*100))

lines.append("")
lines.append("### Source Distribution")
lines.append("")
lines.append("| Source | Sessions | Messages | %% |")
lines.append("|--------|----------|----------|---|")
sm = {}
for r in results:
    sm.setdefault(r["source"], {"c": 0, "m": 0})
    sm[r["source"]]["c"] += 1
    sm[r["source"]]["m"] += r["total"]
for src, v in sorted(sm.items(), key=lambda x: -x[1]["c"]):
    lines.append("| %s | %d | %d | %.1f%% |" % (src, v["c"], v["m"], v["c"]/total*100))

content = "\n".join(lines)
os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
with open(OUT_PATH, "w", encoding="utf-8-sig", newline="") as f:
    f.write(content)

print("Report saved to: " + OUT_PATH)
print("Total sessions: %d (Jcode: %d, Codex: %d, Continue: %d)" % (total, len(jrs), len(crs), len(nrs)))
