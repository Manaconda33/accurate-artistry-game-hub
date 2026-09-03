import { execFileSync } from 'node:child_process';
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { extname, join, relative } from 'node:path';

const repositoryRoot = new URL('../', import.meta.url);
const oldDisplayName = ['Accurate', 'Artistry'].join(' ');
const oldSlug = ['accurate', 'artistry', 'game', 'hub'].join('-');
const forbidden = [oldDisplayName, oldSlug];
const textExtensions = new Set([
  '.css',
  '.html',
  '.js',
  '.json',
  '.md',
  '.mjs',
  '.py',
  '.ts',
  '.yaml',
  '.yml',
]);
const skippedDirectories = new Set(['.git', 'coverage', 'dist', 'history', 'node_modules']);
const skippedFiles = new Set(['tools/verify-branding.mjs']);
const failures = [];

function inspectText(path, displayPath) {
  const contents = readFileSync(path, 'utf8');
  for (const term of forbidden) {
    if (contents.toLowerCase().includes(term.toLowerCase()))
      failures.push(`${displayPath}: ${term}`);
  }
}

function walk(path) {
  for (const entry of readdirSync(path)) {
    const fullPath = join(path, entry);
    const displayPath = relative(repositoryRoot.pathname, fullPath);
    const stats = statSync(fullPath);
    if (stats.isDirectory()) {
      if (!skippedDirectories.has(entry)) walk(fullPath);
      continue;
    }
    if (skippedFiles.has(displayPath)) continue;
    for (const term of forbidden) {
      if (displayPath.toLowerCase().includes(term.toLowerCase()))
        failures.push(`${displayPath}: filename`);
    }
    if (textExtensions.has(extname(entry))) inspectText(fullPath, displayPath);
  }
}

walk(repositoryRoot.pathname);

const approvalArtifact = join(
  repositoryRoot.pathname,
  'docs/Manacondas_Minigame_Mayhem_PRD_v1.1.docx',
);
const approvalXml = execFileSync('unzip', ['-p', approvalArtifact, 'word/document.xml'], {
  encoding: 'utf8',
});
for (const term of forbidden) {
  if (approvalXml.toLowerCase().includes(term.toLowerCase()))
    failures.push(`approval DOCX: ${term}`);
}

if (failures.length > 0) {
  throw new Error(
    `Former-brand references remain outside preserved history:\n${failures.join('\n')}`,
  );
}

console.log("Verified Manaconda's Minigame Mayhem branding.");
