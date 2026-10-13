#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const https = require('https');
const os = require('os');

const CATALOG_URL = "https://raw.githubusercontent.com/rmyndharis/antigravity-skills/main/catalog.json";
const RAW_BASE_URL = "https://raw.githubusercontent.com/rmyndharis/antigravity-skills/main/";
const API_BASE_URL = "https://api.github.com/repos/rmyndharis/antigravity-skills/contents/";

const GLOBAL_SKILLS_DIR = path.join(os.homedir(), '.gemini', 'config', 'skills');
const LOCAL_SKILLS_DIR = path.join(process.cwd(), '.agent', 'skills');

function getSkillsDir(isGlobal = false, isWorkspace = false) {
  if (process.env.AG_SKILLS_DIR) {
    let override = process.env.AG_SKILLS_DIR;
    if (override.startsWith('~')) {
      override = path.join(os.homedir(), override.slice(1));
    }
    return path.resolve(override);
  }
  if (isGlobal) return path.resolve(GLOBAL_SKILLS_DIR);
  if (isWorkspace) return path.resolve(LOCAL_SKILLS_DIR);
  if (fs.existsSync(LOCAL_SKILLS_DIR) && fs.statSync(LOCAL_SKILLS_DIR).isDirectory()) {
    return path.resolve(LOCAL_SKILLS_DIR);
  }
  return path.resolve(GLOBAL_SKILLS_DIR);
}

function containedJoin(base, ...parts) {
  const baseAbs = path.resolve(base);
  const target = path.resolve(baseAbs, ...parts);
  if (target !== baseAbs && !target.startsWith(baseAbs + path.sep)) {
    throw new Error(`Refusing to write outside ${baseAbs}: ${target}`);
  }
  return target;
}

function fetchJson(url) {
  return new Promise((resolve) => {
    https.get(url, { headers: { 'User-Agent': 'AntigravitySkillsCLI/1.0' }, timeout: 10000 }, (res) => {
      if (res.statusCode < 200 || res.statusCode >= 300) {
        return resolve(null);
      }
      let raw = '';
      res.on('data', chunk => raw += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(raw)); } catch { resolve(null); }
      });
    }).on('error', () => resolve(null));
  });
}

function fetchBuffer(url) {
  return new Promise((resolve) => {
    https.get(url, { headers: { 'User-Agent': 'AntigravitySkillsCLI/1.0' }, timeout: 15000 }, (res) => {
      if (res.statusCode < 200 || res.statusCode >= 300) {
        return resolve(null);
      }
      const chunks = [];
      res.on('data', chunk => chunks.push(chunk));
      res.on('end', () => resolve(Buffer.concat(chunks)));
    }).on('error', () => resolve(null));
  });
}

function loadCatalog() {
  const localCatalog = path.join(__dirname, 'catalog.json');
  if (fs.existsSync(localCatalog)) {
    try {
      return JSON.parse(fs.readFileSync(localCatalog, 'utf8'));
    } catch {}
  }
  return null;
}

function loadAliases() {
  const localAliases = path.join(__dirname, 'aliases.json');
  if (fs.existsSync(localAliases)) {
    try {
      return JSON.parse(fs.readFileSync(localAliases, 'utf8'));
    } catch {}
  }
  return {};
}

function loadBundles() {
  const localBundles = path.join(__dirname, 'bundles.json');
  if (fs.existsSync(localBundles)) {
    try {
      return JSON.parse(fs.readFileSync(localBundles, 'utf8'));
    } catch {}
  }
  return {};
}

function resolveSkillId(skillInput) {
  const aliases = loadAliases();
  return aliases[skillInput] || skillInput;
}

function skillMatches(s, query) {
  if (!query) return true;
  const haystack = [
    s.id || '',
    s.name || '',
    s.description || '',
    s.category || '',
    (s.tags || []).join(' '),
    (s.triggers || []).join(' ')
  ].join(' ').toLowerCase();

  const tokens = query.toLowerCase().split(/\s+/).filter(Boolean);
  return tokens.every(token => haystack.includes(token));
}

function cmdList(category = null, query = null) {
  const catalog = loadCatalog();
  if (!catalog || !catalog.skills) {
    console.error('Failed to load catalog.json.');
    process.exit(1);
  }

  let skills = catalog.skills;
  if (category) {
    skills = skills.filter(s => (s.category || '').toLowerCase() === category.toLowerCase());
  }
  if (query) {
    skills = skills.filter(s => skillMatches(s, query));
  }

  console.log(`\n[+] Found ${skills.length} skill(s) in catalog:\n` + '-'.repeat(60));
  if (skills.length === 0) {
    console.log('No skills found matching query.');
    return;
  }

  const limit = (category || query) ? null : 40;
  const display = limit ? skills.slice(0, limit) : skills;
  display.forEach(s => {
    const cat = `[${s.category || 'general'}]`;
    console.log(`* ${(s.id || '').padEnd(48)} ${cat.padEnd(12)}`);
    if (s.description) {
      const desc = s.description.length > 80 ? s.description.slice(0, 80) + '...' : s.description;
      console.log(`  └─ ${desc}`);
    }
  });

  if (limit && skills.length > limit) {
    console.log(`\n... and ${skills.length - limit} more. Use search <term> to filter.`);
  }
}

function copyFolderLocal(localSrc, localDst) {
  fs.mkdirSync(localDst, { recursive: true });
  fs.cpSync(localSrc, localDst, { recursive: true, force: true });
  return true;
}

async function downloadFolderRecursive(remotePath, localTargetDir) {
  fs.mkdirSync(localTargetDir, { recursive: true });
  const apiUrl = API_BASE_URL + remotePath;
  const items = await fetchJson(apiUrl);
  if (!items || !Array.isArray(items)) {
    const rawUrl = RAW_BASE_URL + remotePath + '/SKILL.md';
    const content = await fetchBuffer(rawUrl);
    if (content) {
      fs.writeFileSync(containedJoin(localTargetDir, 'SKILL.md'), content);
      console.log('  └─ Downloaded: SKILL.md (remote listing unavailable)');
      return true;
    }
    return false;
  }

  let success = true;
  for (const item of items) {
    const itemPath = item.path || '';
    const targetItemPath = containedJoin(localTargetDir, item.name);
    if (!itemPath.startsWith(remotePath + '/')) continue;

    if (item.type === 'file') {
      const downloadUrl = item.download_url || (RAW_BASE_URL + itemPath);
      const data = await fetchBuffer(downloadUrl);
      if (data) {
        fs.writeFileSync(targetItemPath, data);
        console.log(`  └─ Downloaded: ${item.name}`);
      } else {
        success = false;
      }
    } else if (item.type === 'dir') {
      const dirOk = await downloadFolderRecursive(itemPath, targetItemPath);
      if (!dirOk) success = false;
    }
  }
  return success;
}

async function cmdInstall(skillId, isGlobal = false, isWorkspace = false) {
  if (!skillId) {
    console.error('Please specify skill name/id to install.');
    process.exit(1);
  }

  const cleanId = resolveSkillId(skillId.trim());
  const catalog = loadCatalog();
  if (!catalog || !catalog.skills) {
    console.error('Failed to load catalog.json.');
    process.exit(1);
  }

  const found = catalog.skills.find(s => 
    (s.id || '').toLowerCase() === cleanId.toLowerCase() ||
    (s.name || '').toLowerCase() === cleanId.toLowerCase()
  );

  if (!found) {
    console.error(`Error: Skill '${cleanId}' not found in catalog.`);
    process.exit(1);
  }

  const skillsDir = getSkillsDir(isGlobal, isWorkspace);
  const targetSkillDir = containedJoin(skillsDir, found.id);
  const scopeLabel = isGlobal ? 'global' : 'workspace';
  console.log(`[*] Installing skill '${found.id}' (${scopeLabel}) into: ${targetSkillDir}`);

  if (fs.existsSync(targetSkillDir)) {
    console.log('  └─ Replacing existing installation');
    fs.rmSync(targetSkillDir, { recursive: true, force: true });
  }

  const candidates = [
    containedJoin(__dirname, 'temp_antigravity_skills', 'skills', found.id),
    containedJoin(__dirname, 'skills', found.id),
    containedJoin(__dirname, '.agent', 'skills', found.id)
  ];

  let localSrc = null;
  for (const cand of candidates) {
    if (fs.existsSync(cand) && fs.statSync(cand).isDirectory()) {
      localSrc = cand;
      break;
    }
  }

  let ok = false;
  if (localSrc) {
    ok = copyFolderLocal(localSrc, targetSkillDir);
    console.log(`  └─ Copied from local repository`);
  } else {
    ok = await downloadFolderRecursive(`skills/${found.id}`, targetSkillDir);
  }

  if (ok && fs.existsSync(path.join(targetSkillDir, 'SKILL.md'))) {
    console.log(`[OK] Successfully installed '${found.id}'!`);
    return true;
  } else {
    console.error(`[!] Installation incomplete for '${found.id}'.`);
    return false;
  }
}

function cmdBundles() {
  const data = loadBundles();
  const bundles = data.bundles || {};
  console.log(`\n[*] Available Skill Bundles (${Object.keys(bundles).length} total):\n` + '-'.repeat(60));
  for (const [name, b] of Object.entries(bundles)) {
    console.log(`* ${name.padEnd(20)} (${(b.skills || []).length} skills)`);
    console.log(`  └─ ${b.description || ''}`);
    console.log(`  └─ Command: node skills-cli.js install --bundle ${name}`);
  }
}

async function cmdInstallBundle(bundleName, isGlobal = false, isWorkspace = false) {
  const data = loadBundles();
  const bundles = data.bundles || {};
  if (!bundles[bundleName]) {
    console.error(`Error: Bundle '${bundleName}' not found in bundles.json.`);
    process.exit(1);
  }

  const skills = bundles[bundleName].skills || [];
  console.log(`[*] Installing bundle '${bundleName}' (${skills.length} skills)...`);
  let successes = 0;
  for (const s of skills) {
    const ok = await cmdInstall(s, isGlobal, isWorkspace);
    if (ok) successes++;
  }
  console.log(`\n[OK] Bundle '${bundleName}' complete: ${successes}/${skills.length} installed.`);
}

function cmdInstalled(isGlobal = false, isWorkspace = false) {
  const skillsDir = getSkillsDir(isGlobal, isWorkspace);
  if (!fs.existsSync(skillsDir)) {
    console.log(`No skills directory found at: ${skillsDir}`);
    return;
  }

  const dirs = fs.readdirSync(skillsDir).filter(d => {
    try { return fs.statSync(path.join(skillsDir, d)).isDirectory(); } catch { return false; }
  });

  console.log(`\n[*] Installed Skills in ${skillsDir} (${dirs.length} total):\n` + '-'.repeat(60));
  dirs.sort().forEach(d => {
    const skillMd = path.join(skillsDir, d, 'SKILL.md');
    const hasMd = fs.existsSync(skillMd) ? '[OK] SKILL.md' : '[X] No SKILL.md';
    console.log(`* ${d.padEnd(45)} ${hasMd}`);
  });
}

function cmdSyncGlobal() {
  const src = LOCAL_SKILLS_DIR;
  const dst = GLOBAL_SKILLS_DIR;
  if (!fs.existsSync(src)) {
    console.error(`Local skills directory not found: ${src}`);
    process.exit(1);
  }
  if (!fs.existsSync(dst)) {
    fs.mkdirSync(dst, { recursive: true });
  }

  const superseded = ['design-taste-frontend', 'high-end-visual-design', 'doc-coauthoring', 'vercel-cli-with-tokens'];
  for (const s of superseded) {
    const target = path.join(dst, s);
    if (fs.existsSync(target)) {
      fs.rmSync(target, { recursive: true, force: true });
      console.log(`- Removed superseded: ${s}`);
    }
  }

  const skills = fs.readdirSync(src, { withFileTypes: true }).filter(d => d.isDirectory()).map(d => d.name);
  let count = 0;
  for (const s of skills) {
    fs.cpSync(path.join(src, s), path.join(dst, s), { recursive: true, force: true });
    count++;
  }
  console.log(`\n[+] Successfully synced ${count} skills from workspace to global Antigravity config:`);
  console.log(`    Source: ${src}`);
  console.log(`    Target: ${dst}`);
}

async function main() {
  const args = process.argv.slice(2);
  const isGlobal = args.includes('--global') || args.includes('-g');
  const isWorkspace = args.includes('--workspace') || args.includes('-w');
  const filteredArgs = args.filter(a => !['--global', '-g', '--workspace', '-w'].includes(a));

  const cmd = (filteredArgs[0] || 'list').toLowerCase();

  if (cmd === 'list') {
    let cat = null;
    let q = null;
    if (filteredArgs[1] === '--category' && filteredArgs[2]) {
      cat = filteredArgs[2];
    } else if (filteredArgs[1]) {
      q = filteredArgs.slice(1).join(' ');
    }
    cmdList(cat, q);
  } else if (cmd === 'search') {
    const q = filteredArgs.slice(1).join(' ');
    if (!q) {
      console.error('Usage: node skills-cli.js search <query>');
      process.exit(1);
    }
    cmdList(null, q);
  } else if (cmd === 'bundles') {
    cmdBundles();
  } else if (cmd === 'install') {
    const bundleIdx = filteredArgs.indexOf('--bundle');
    if (bundleIdx !== -1 && filteredArgs[bundleIdx + 1]) {
      await cmdInstallBundle(filteredArgs[bundleIdx + 1], isGlobal, isWorkspace);
    } else if (filteredArgs[1]) {
      await cmdInstall(filteredArgs[1], isGlobal, isWorkspace);
    } else {
      console.error('Usage: node skills-cli.js install <skill-id> [--global|--workspace]');
      process.exit(1);
    }
  } else if (cmd === 'installed') {
    cmdInstalled(isGlobal, isWorkspace);
  } else if (cmd === 'sync-global' || cmd === 'sync') {
    cmdSyncGlobal();
  } else {
    console.log('Usage: node skills-cli.js [list|search|bundles|install|installed|sync-global] [options]');
  }
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
