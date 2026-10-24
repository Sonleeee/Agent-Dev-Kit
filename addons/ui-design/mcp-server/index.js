#!/usr/bin/env node
/**
 * Agent-Dev-Kit UI Design Craft CLI & MCP Server
 * Entry point: Bootstrap, CLI Router and Stdio JSON-RPC 2.0 Transport.
 */

import fs from 'node:fs';
import path from 'node:path';
import readline from 'node:readline';
import { fileURLToPath } from 'node:url';
import { TOOLS_SCHEMA, dispatchTool } from './tools/index.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const kitRoot = path.resolve(__dirname, '..', '..', '..');

// 1. Tải cơ sở tri thức archetypes, motion recipes & blueprints
const archetypesPath = path.join(__dirname, 'data', 'archetypes.json');
const motionRecipesPath = path.join(__dirname, 'data', 'motion-recipes.json');
const componentBlueprintsPath = path.join(__dirname, 'data', 'component-blueprints.json');

function loadJsonSafe(filePath, key, label) {
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'))[key] || [];
  } catch (e) {
    console.error(`[UIDesignMCP] Warning: Unable to load ${label}:`, e.message);
    return [];
  }
}

const archetypesDb = loadJsonSafe(archetypesPath, 'archetypes', 'archetypes.json');
const motionRecipesDb = loadJsonSafe(motionRecipesPath, 'recipes', 'motion-recipes.json');
const componentBlueprintsDb = loadJsonSafe(componentBlueprintsPath, 'blueprints', 'component-blueprints.json');

const ctx = {
  archetypesDb,
  motionRecipesDb,
  componentBlueprintsDb,
  kitRoot
};

function handleToolCall(name, args = {}) {
  return dispatchTool(name, args, ctx);
}

// 2. Chế độ CLI
const cliArgs = process.argv.slice(2);
if (cliArgs.length > 0 && !cliArgs.includes('--stdio')) {
  const cmd = cliArgs[0].toLowerCase();

  if (cmd === '--help' || cmd === '-h' || cmd === 'help') {
    console.log(`
Agent-Dev-Kit UI Design Craft CLI & MCP Server
Cách dùng:
  node index.js search [query]                             : Tìm kiếm Design Archetypes
  node index.js tokens <archetype_id> [format]             : Xuất Design Tokens (design-md | tailwind-v4 | css-vars | dtcg-json)
  node index.js component <component_id>                   : Xem Component Blueprint + Motion Physics + break-ui payloads
  node index.js contrast <fg_hex> <bg_hex> [AA|AAA]        : Kiểm tra độ tương phản màu WCAG 2.2 & gợi ý màu sửa
  node index.js audit <path...>                            : Kiểm toán mã nguồn UI chấm điểm Impeccable 20/20
  node index.js fix <path...>                              : Tự động sửa các lỗi UI Anti-Slop tĩnh
  node index.js scaffold <archetype_id> <target_dir> [name]: Sinh hợp đồng thiết kế DESIGN.md vào thư mục đích
  node index.js                                            : Khởi chạy dưới dạng MCP Server (Stdio)
`);
    process.exit(0);
  } else if (cmd === 'search') {
    const q = cliArgs.slice(1).join(' ');
    const res = handleToolCall('search_design_archetypes', { query: q });
    console.log(res.content[0].text);
    process.exit(res.isError ? 1 : 0);
  } else if (cmd === 'tokens') {
    const archetypeId = cliArgs[1];
    const format = cliArgs[2] || 'design-md';
    const res = handleToolCall('get_design_tokens', { archetype_id: archetypeId, format });
    console.log(res.content[0].text);
    process.exit(res.isError ? 1 : 0);
  } else if (cmd === 'component') {
    const componentId = cliArgs[1];
    const res = handleToolCall('get_component_blueprint', { component_id: componentId });
    console.log(res.content[0].text);
    process.exit(res.isError ? 1 : 0);
  } else if (cmd === 'contrast') {
    const fg = cliArgs[1];
    const bg = cliArgs[2];
    const level = cliArgs[3] || 'AA';
    const res = handleToolCall('verify_color_contrast', {
      foreground_hex: fg,
      background_hex: bg,
      level
    });
    console.log(res.content[0].text);
    process.exit(res.isError ? 1 : 0);
  } else if (cmd === 'audit') {
    const rawArgs = cliArgs.slice(1);
    const strict = rawArgs.includes('--strict');
    const paths = rawArgs.filter((a) => a !== '--strict');
    const res = handleToolCall('audit_ui_code', { paths, strict });
    console.log(res.content[0].text);
    process.exit(res.isError ? 1 : 0);
  } else if (cmd === 'fix') {
    const paths = cliArgs.slice(1);
    const res = handleToolCall('fix_ui_slop', { paths });
    console.log(res.content[0].text);
    process.exit(res.isError ? 1 : 0);
  } else if (cmd === 'scaffold') {
    const archetypeId = cliArgs[1];
    const targetDir = cliArgs[2] || '.';
    const projectName = cliArgs[3];
    const overwrite = cliArgs.includes('--overwrite');
    const res = handleToolCall('scaffold_design_contract', {
      archetype_id: archetypeId,
      target_dir: targetDir,
      project_name: projectName,
      overwrite
    });
    console.log(res.content[0].text);
    process.exit(res.isError ? 1 : 0);
  } else {
    console.error(`Lệnh CLI không hợp lệ: "${cmd}". Chạy với --help để xem hướng dẫn.`);
    process.exit(1);
  }
}

// 3. Chế độ MCP Server (JSON-RPC 2.0 qua Stdio)
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
});

function sendResponse(id, result, error = null) {
  const response = { jsonrpc: '2.0', id };
  if (error) {
    response.error = error;
  } else {
    response.result = result;
  }
  process.stdout.write(JSON.stringify(response) + '\n');
}

rl.on('line', (line) => {
  const trimmed = line.trim();
  if (!trimmed) return;

  let request;
  try {
    request = JSON.parse(trimmed);
  } catch (err) {
    sendResponse(null, null, { code: -32700, message: 'Parse error' });
    return;
  }

  const { id, method, params } = request;

  switch (method) {
    case 'initialize':
      sendResponse(id, {
        protocolVersion: '2024-11-05',
        capabilities: {
          tools: {}
        },
        serverInfo: {
          name: 'ui-design',
          version: '1.0.0'
        }
      });
      break;

    case 'notifications/initialized':
      break;

    case 'ping':
      sendResponse(id, {});
      break;

    case 'tools/list':
      sendResponse(id, { tools: TOOLS_SCHEMA });
      break;

    case 'tools/call': {
      if (!params || !params.name) {
        sendResponse(id, null, { code: -32602, message: 'Missing tool name' });
        break;
      }
      try {
        const result = handleToolCall(params.name, params.arguments || {});
        sendResponse(id, result);
      } catch (callErr) {
        sendResponse(id, {
          isError: true,
          content: [{ type: 'text', text: `Tool error: ${callErr.message}` }]
        });
      }
      break;
    }

    default:
      if (id !== undefined && id !== null) {
        sendResponse(id, null, { code: -32601, message: `Method not found: ${method}` });
      }
      break;
  }
});

console.error('[UIDesignMCP] Server v1.0.0 initialized.');
