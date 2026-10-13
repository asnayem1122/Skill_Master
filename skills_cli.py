import sys
import os
import re
import json
import shutil
import urllib.request
import urllib.error

# Reconfigure sys.stdout/stderr to UTF-8 for Windows terminal compatibility.
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

CATALOG_URL = "https://raw.githubusercontent.com/rmyndharis/antigravity-skills/main/catalog.json"
RAW_BASE_URL = "https://raw.githubusercontent.com/rmyndharis/antigravity-skills/main/"
API_BASE_URL = "https://api.github.com/repos/rmyndharis/antigravity-skills/contents/"

GLOBAL_SKILLS_DIR = os.path.join(os.path.expanduser("~"), ".gemini", "antigravity", "skills")
LOCAL_SKILLS_DIR = os.path.join(os.getcwd(), ".agent", "skills")

def get_skills_dir(is_global=False, is_workspace=False):
    override = os.environ.get("AG_SKILLS_DIR")
    if override:
        if override == "~" or override.startswith(("~/", "~\\")):
            override = os.path.expanduser("~") + override[1:]
        return os.path.abspath(override)
    if is_global:
        return os.path.abspath(GLOBAL_SKILLS_DIR)
    if is_workspace:
        return os.path.abspath(LOCAL_SKILLS_DIR)
    
    # Auto-detect: if current directory has .agent/skills, use workspace scope
    if os.path.isdir(LOCAL_SKILLS_DIR):
        return os.path.abspath(LOCAL_SKILLS_DIR)
    return os.path.abspath(GLOBAL_SKILLS_DIR)

SKILL_PATH_RE = re.compile(r'^skills/([A-Za-z0-9._-]+)/SKILL\.md$')

def skill_folder_from_catalog(cat_path, skill_id):
    candidate = cat_path or f"skills/{skill_id}/SKILL.md"
    match = SKILL_PATH_RE.match(candidate)
    if not match or match.group(1) in ('.', '..'):
        raise ValueError(f"unsafe skill path in catalog entry: {candidate!r}")
    return candidate[:-len('/SKILL.md')]

def contained_join(base, *parts):
    base_abs = os.path.abspath(base)
    target = os.path.abspath(os.path.join(base_abs, *parts))
    if target != base_abs and not target.startswith(base_abs + os.sep):
        raise ValueError(f"refusing to write outside {base_abs}: {target}")
    return target

def fetch_json(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AntigravitySkillsInstaller/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None

def fetch_bytes(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AntigravitySkillsInstaller/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read()
    except Exception as e:
        print(f"Error downloading {url}: {e}", file=sys.stderr)
        return None

def load_catalog():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_catalog = os.path.join(script_dir, "catalog.json")
    if os.path.exists(local_catalog):
        try:
            with open(local_catalog, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return fetch_json(CATALOG_URL)

def load_aliases():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_aliases = os.path.join(script_dir, "aliases.json")
    if os.path.exists(local_aliases):
        try:
            with open(local_aliases, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def load_bundles():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_bundles = os.path.join(script_dir, "bundles.json")
    if os.path.exists(local_bundles):
        try:
            with open(local_bundles, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def resolve_skill_id(skill_input):
    aliases = load_aliases()
    return aliases.get(skill_input, skill_input)

def skill_matches(s, query):
    if not query:
        return True
    haystack = " ".join([
        s.get('id', ''),
        s.get('name', ''),
        s.get('description', ''),
        s.get('category', ''),
        " ".join(s.get('tags', [])),
        " ".join(s.get('triggers', [])),
    ]).lower()
    return all(token in haystack for token in query.lower().split())

def cmd_list(category=None, query=None):
    catalog = load_catalog()
    if catalog is None or 'skills' not in catalog:
        print("Failed to load catalog.", file=sys.stderr)
        sys.exit(1)

    skills = catalog['skills']
    if not skills:
        print("\n[+] Found 0 skill(s) in catalog:\n" + "-"*60)
        print("No skills available in catalog.")
        return

    if category:
        skills = [s for s in skills if s.get('category', '').lower() == category.lower()]
    if query:
        skills = [s for s in skills if skill_matches(s, query)]

    print(f"\n[+] Found {len(skills)} skill(s) in catalog:\n" + "-"*60)
    if not skills:
        print("No skills found matching filter.")
        return

    limit = None if (category or query) else 40
    for s in (skills if limit is None else skills[:limit]):
        cat = f"[{s.get('category', 'general')}]"
        print(f"* {s.get('id', ''):<50} {cat:<12}")
        if s.get('description'):
            desc = s['description'][:80] + "..." if len(s['description']) > 80 else s['description']
            print(f"  └─ {desc}")
    if limit is not None and len(skills) > limit:
        print(f"\n... and {len(skills) - limit} more. Use --query <term> or search <term> to filter.")

def cmd_search(query):
    if not query or not query.strip():
        print("Usage: python skills_cli.py search <term>", file=sys.stderr)
        sys.exit(1)
    cmd_list(query=query.strip())

def copy_folder_local(local_src, local_dst):
    os.makedirs(local_dst, exist_ok=True)
    for root, _dirs, files in os.walk(local_src):
        rel_path = os.path.relpath(root, local_src)
        target_dir = local_dst if rel_path == "." else contained_join(local_dst, rel_path)
        os.makedirs(target_dir, exist_ok=True)
        for f in files:
            src_file = os.path.join(root, f)
            dst_file = contained_join(target_dir, f)
            with open(src_file, "rb") as rf:
                content = rf.read()
            with open(dst_file, "wb") as wf:
                wf.write(content)
            print(f"  └─ Copied: {f}")
    return True

def download_folder_recursive(remote_path, local_target_dir):
    os.makedirs(local_target_dir, exist_ok=True)
    api_url = API_BASE_URL + remote_path
    items = fetch_json(api_url)
    if not items or not isinstance(items, list):
        raw_url = RAW_BASE_URL + remote_path + "/SKILL.md"
        content = fetch_bytes(raw_url)
        if content:
            with open(contained_join(local_target_dir, "SKILL.md"), "wb") as f:
                f.write(content)
            print("  └─ Downloaded: SKILL.md (folder listing unavailable, other files skipped)")
            return True
        return False

    success = True
    for item in items:
        item_name = item.get('name', '')
        item_path = item.get('path', '')
        item_type = item.get('type', '')
        target_item_path = contained_join(local_target_dir, item_name)

        if not item_path.startswith(remote_path + "/"):
            print(f"  └─ Skipped (outside {remote_path}): {item_path}", file=sys.stderr)
            success = False
            continue

        if item_type == 'file':
            download_url = item.get('download_url') or (RAW_BASE_URL + item_path)
            if not download_url.startswith(RAW_BASE_URL):
                print(f"  └─ Skipped (unexpected download host): {download_url}", file=sys.stderr)
                success = False
                continue
            data = fetch_bytes(download_url)
            if data is not None:
                with open(target_item_path, "wb") as f:
                    f.write(data)
                print(f"  └─ Downloaded: {item_name}")
            else:
                success = False
        elif item_type == 'dir':
            dir_ok = download_folder_recursive(item_path, target_item_path)
            if not dir_ok:
                success = False

    return success

def cmd_install(skill_id, is_global=False, is_workspace=False):
    if not skill_id or not skill_id.strip():
        print("Please specify skill name/id to install.", file=sys.stderr)
        sys.exit(1)

    skill_id_clean = resolve_skill_id(skill_id.strip())
    catalog = load_catalog()
    if catalog is None or 'skills' not in catalog:
        print("Failed to load catalog.", file=sys.stderr)
        sys.exit(1)

    found = None
    for s in catalog['skills']:
        if s.get('id', '').lower() == skill_id_clean.lower() or s.get('name', '').lower() == skill_id_clean.lower():
            found = s
            break

    if not found:
        print(f"Error: Skill '{skill_id_clean}' not found in catalog.", file=sys.stderr)
        sys.exit(1)

    skills_dir = get_skills_dir(is_global=is_global, is_workspace=is_workspace)
    try:
        remote_skill_path = skill_folder_from_catalog(found.get('path', ''), found['id'])
        target_skill_dir = contained_join(skills_dir, found['id'])
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    scope_label = "global" if is_global else "workspace"
    print(f"[*] Installing skill '{found['id']}' ({scope_label}) into: {target_skill_dir}")

    if os.path.isdir(target_skill_dir):
        print("  └─ Replacing existing installation")
        shutil.rmtree(target_skill_dir)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        contained_join(script_dir, remote_skill_path),
        contained_join(script_dir, "temp_antigravity_skills", remote_skill_path),
        contained_join(script_dir, "skills", found['id']),
    ]
    
    local_skill_src = None
    for cand in candidates:
        if os.path.exists(cand) and os.path.isdir(cand):
            local_skill_src = cand
            break

    try:
        if local_skill_src:
            ok = copy_folder_local(local_skill_src, target_skill_dir)
        else:
            ok = download_folder_recursive(remote_skill_path, target_skill_dir)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if ok and os.path.exists(os.path.join(target_skill_dir, "SKILL.md")):
        print(f"[OK] Successfully installed '{found['id']}'!")
        return True
    else:
        print(f"[!] Installation incomplete for '{found['id']}' - some files could not be retrieved.", file=sys.stderr)
        return False

def cmd_bundles():
    data = load_bundles()
    bundles = data.get('bundles', {})
    if not bundles:
        print("No bundles found in bundles.json.")
        return
    print(f"\n[*] Available Skill Bundles ({len(bundles)} total):\n" + "-"*60)
    for b_name, b_info in bundles.items():
        skills = b_info.get('skills', [])
        desc = b_info.get('description', '')
        print(f"* {b_name:<20} ({len(skills)} skills)")
        print(f"  └─ {desc}")
        print(f"  └─ Example: python skills_cli.py install --bundle {b_name}")

def cmd_install_bundle(bundle_name, is_global=False, is_workspace=False):
    data = load_bundles()
    bundles = data.get('bundles', {})
    if bundle_name not in bundles:
        print(f"Error: Bundle '{bundle_name}' not found. Run 'python skills_cli.py bundles' to view list.", file=sys.stderr)
        sys.exit(1)

    b_info = bundles[bundle_name]
    skills = b_info.get('skills', [])
    print(f"[*] Installing bundle '{bundle_name}' ({len(skills)} skills)...")
    successes = 0
    for sid in skills:
        if cmd_install(sid, is_global=is_global, is_workspace=is_workspace):
            successes += 1
    print(f"\n[OK] Bundle '{bundle_name}' complete: {successes}/{len(skills)} skills installed.")

def cmd_installed(is_global=False, is_workspace=False):
    skills_dir = get_skills_dir(is_global=is_global, is_workspace=is_workspace)
    if not os.path.exists(skills_dir):
        print(f"No skills directory found at: {skills_dir}")
        return

    dirs = [d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))]
    if not dirs:
        print(f"No skills currently installed in: {skills_dir}")
        return

    print(f"\n[*] Installed Skills in {skills_dir} ({len(dirs)} total):\n" + "-"*60)
    for d in sorted(dirs):
        skill_md = os.path.join(skills_dir, d, "SKILL.md")
        has_md = "[OK] SKILL.md" if os.path.exists(skill_md) else "[X] No SKILL.md"
        print(f"* {d:<45} {has_md}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python skills_cli.py [list|search|install|installed|bundles] [options]")
        print("Options:")
        print("  --global, -g       Target global skills (~/.gemini/antigravity/skills/)")
        print("  --workspace, -w    Target workspace skills (.agent/skills/)")
        print("  --bundle <name>    Install all skills in a specified bundle")
        sys.exit(1)

    args = sys.argv[1:]
    is_global = "--global" in args or "-g" in args
    is_workspace = "--workspace" in args or "-w" in args
    filtered_args = [a for a in args if a not in ("--global", "-g", "--workspace", "-w")]

    cmd = filtered_args[0].lower() if filtered_args else "list"

    if cmd == "list":
        cat = None
        q = None
        if len(filtered_args) > 1:
            if filtered_args[1] == "--category" and len(filtered_args) > 2:
                cat = filtered_args[2]
            elif filtered_args[1] == "--query" and len(filtered_args) > 2:
                q = filtered_args[2]
            else:
                q = filtered_args[1]
        cmd_list(category=cat, query=q)
    elif cmd == "search":
        q = " ".join(filtered_args[1:]) if len(filtered_args) > 1 else ""
        cmd_search(q)
    elif cmd == "bundles":
        cmd_bundles()
    elif cmd == "install":
        if "--bundle" in filtered_args:
            idx = filtered_args.index("--bundle")
            if idx + 1 < len(filtered_args):
                cmd_install_bundle(filtered_args[idx + 1], is_global=is_global, is_workspace=is_workspace)
            else:
                print("Error: --bundle requires a bundle name.", file=sys.stderr)
                sys.exit(1)
        else:
            if len(filtered_args) < 2:
                print("Please specify skill name/id or --bundle <name> to install.", file=sys.stderr)
                sys.exit(1)
            cmd_install(filtered_args[1], is_global=is_global, is_workspace=is_workspace)
    elif cmd == "installed":
        cmd_installed(is_global=is_global, is_workspace=is_workspace)
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
