#!/usr/bin/env node
/**
 * deploy.js — Deploy built HTML to Netlify (or local preview)
 *
 * Usage:
 *   node deploy.js <file.html>                    # Deploy to Netlify
 *   node deploy.js <file.html> --local            # Open in browser
 *   node deploy.js <file.html> --site <name>      # Deploy to specific site
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const args = process.argv.slice(2);

const htmlPath = args.find(a => !a.startsWith('--'));
const isLocal = args.includes('--local');
const siteIdx = args.indexOf('--site');
const siteName = siteIdx >= 0 ? args[siteIdx + 1] : null;

if (!htmlPath || !fs.existsSync(htmlPath)) {
  console.error('Usage: node deploy.js <file.html> [--local] [--site name]');
  process.exit(1);
}

if (isLocal) {
  // Create temp directory with the HTML
  const tmpDir = '/tmp/montest-preview';
  fs.mkdirSync(tmpDir, { recursive: true });
  const dest = path.join(tmpDir, 'index.html');
  fs.copyFileSync(htmlPath, dest);
  console.log(`Preview: ${dest}`);
  try { execSync(`open "${dest}"`, { stdio: 'ignore' }); } catch(e) {}
  process.exit(0);
}

// Deploy to Netlify
const dir = path.dirname(htmlPath);
const name = siteName || 'montest-' + Date.now();

console.log(`Deploying ${path.basename(htmlPath)} to Netlify...`);
try {
  // Try deploying to existing site first
  const result = execSync(
    `netlify deploy --dir="${dir}" --prod --site="${name}" 2>&1`,
    { encoding: 'utf8', timeout: 120000 }
  );
  console.log(result);

  // Extract URL
  const urlMatch = result.match(/https?:\/\/[^\s]+\.netlify\.app/);
  if (urlMatch) {
    console.log(`\nDeployed: ${urlMatch[0]}`);
  }
} catch(e) {
  // Site doesn't exist, create new one
  console.log('Site not found, creating new one...');
  try {
    execSync(`netlify sites:create --name="${name}" --disable-sso`, { stdio: 'inherit' });
    const result = execSync(
      `netlify deploy --dir="${dir}" --prod --site="${name}" 2>&1`,
      { encoding: 'utf8', timeout: 120000 }
    );
    console.log(result);
    console.log(`\nDeployed: https://${name}.netlify.app`);
  } catch(e2) {
    console.error('Deploy failed. Try: netlify login first');
    console.error(e2.message);
    process.exit(1);
  }
}
