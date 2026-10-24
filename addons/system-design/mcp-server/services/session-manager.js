/**
 * Ephemeral Session Scratchpad Manager
 * Prevents context drift and hallucinations during architectural interviews.
 */

import fs from 'node:fs';
import path from 'node:path';

const CACHE_DIR_NAME = path.join('.agents', '.cache');
const SESSION_FILE_NAME = 'scaffold-session.json';

export function saveSessionState(targetDir, state) {
  const cacheDir = path.join(targetDir, CACHE_DIR_NAME);
  if (!fs.existsSync(cacheDir)) {
    fs.mkdirSync(cacheDir, { recursive: true });
  }
  const filePath = path.join(cacheDir, SESSION_FILE_NAME);
  fs.writeFileSync(filePath, JSON.stringify(state, null, 2), 'utf8');
  return filePath;
}

export function loadSessionState(targetDir) {
  const possiblePaths = [
    path.join(targetDir, CACHE_DIR_NAME, SESSION_FILE_NAME),
    path.join(process.cwd(), CACHE_DIR_NAME, SESSION_FILE_NAME)
  ];
  for (const p of possiblePaths) {
    if (fs.existsSync(p)) {
      try {
        return { data: JSON.parse(fs.readFileSync(p, 'utf8')), path: p };
      } catch (e) {}
    }
  }
  return null;
}

export function clearSessionState(targetDir) {
  const session = loadSessionState(targetDir);
  if (session && fs.existsSync(session.path)) {
    try {
      fs.unlinkSync(session.path);
      console.error(
        '[SystemDesignMCP] Ephemeral session scratchpad automatically wiped:',
        session.path
      );
    } catch (e) {}
  }
}
