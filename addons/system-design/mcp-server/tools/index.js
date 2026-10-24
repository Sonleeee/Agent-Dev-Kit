/**
 * Tool Registry (Command Pattern)
 * System Design MCP Tools Registry and Dispatcher.
 */

import { tool as searchPatterns } from './search-patterns.js';
import { tool as getPatternDetails } from './get-pattern-details.js';
import { tool as evaluateInterview } from './evaluate-interview.js';
import { tool as listArchitectures } from './list-architectures.js';
import { tool as scaffoldProject } from './scaffold-project.js';
import { tool as injectPattern } from './inject-pattern.js';
import { tool as recommendArchitecture } from './recommend-architecture.js';

export const TOOL_REGISTRY = [
  searchPatterns,
  getPatternDetails,
  evaluateInterview,
  listArchitectures,
  scaffoldProject,
  injectPattern,
  recommendArchitecture
];

export const TOOLS_SCHEMA = TOOL_REGISTRY.map(({ name, description, inputSchema }) => ({
  name,
  description,
  inputSchema
}));

const toolMap = new Map(TOOL_REGISTRY.map((t) => [t.name, t]));

export function dispatchTool(name, args = {}, ctx = {}) {
  const handler = toolMap.get(name);
  if (!handler) {
    return {
      isError: true,
      content: [{ type: 'text', text: `Tool không tồn tại: ${name}` }]
    };
  }
  return handler.execute(args, ctx);
}
