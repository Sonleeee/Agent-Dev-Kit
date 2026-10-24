#!/usr/bin/env node
/**
 * Agent-Dev-Kit System Design CLI & MCP Server
 * Entry point: Bootstrap, CLI Router and Stdio JSON-RPC 2.0 Transport.
 */

import fs from 'node:fs';
import path from 'node:path';
import readline from 'node:readline';
import { fileURLToPath } from 'node:url';
import { TOOLS_SCHEMA, dispatchTool } from './tools/index.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 1. Tải cơ sở tri thức patterns & blueprints
const patternsPath = path.join(__dirname, 'data', 'patterns.json');
const blueprintsPath = path.join(__dirname, 'data', 'blueprints.json');

function loadJsonSafe(filePath, key, label) {
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'))[key] || [];
  } catch (e) {
    console.error(`[SystemDesignMCP] Warning: Unable to load ${label}:`, e.message);
    return [];
  }
}

const patternsDb = loadJsonSafe(patternsPath, 'patterns', 'patterns.json');
const blueprintsDb = loadJsonSafe(blueprintsPath, 'blueprints', 'blueprints.json');

const ctx = {
  patternsDb,
  blueprintsDb
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
Agent-Dev-Kit System Design CLI & MCP Server
Cách dùng:
  node index.js search <từ_khóa>          : Tìm kiếm pattern
  node index.js get <pattern_id>          : Xem chi tiết pattern
  node index.js blueprints                : Liệt kê các bộ source base
  node index.js scaffold <id> <thư_mục>   : Sinh source base dự án ra đĩa
  node index.js                           : Khởi chạy dưới dạng MCP Server (Stdio)
`);
    process.exit(0);
  } else if (cmd === 'search') {
    const q = cliArgs.slice(1).join(' ');
    const res = handleToolCall('search_patterns', { query: q });
    console.log(res.content[0].text);
    process.exit(0);
  } else if (cmd === 'get') {
    const id = cliArgs[1];
    const res = handleToolCall('get_pattern_details', { pattern_id: id });
    console.log(res.content[0].text);
    process.exit(0);
  } else if (cmd === 'blueprints') {
    const res = handleToolCall('list_architectures', {});
    console.log(res.content[0].text);
    process.exit(0);
  } else if (cmd === 'scaffold') {
    const archId = cliArgs[1];
    const target = cliArgs[2] || './new-project';
    const res = handleToolCall('scaffold_project', {
      architecture_id: archId,
      target_dir: target,
      project_name: path.basename(target)
    });
    console.log(res.content[0].text);
    process.exit(0);
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
          name: 'system-design',
          version: '1.1.0'
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

console.error('[SystemDesignMCP] Server v1.1.0 initialized with Ephemeral Scratchpad support.');
