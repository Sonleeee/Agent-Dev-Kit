/**
 * Tool Registry (Command Pattern)
 * Centralizes all tool registrations and provides unified dispatching.
 */

import { tool as searchArchetypes } from './search-archetypes.js';
import { tool as getDesignTokens } from './get-design-tokens.js';
import { tool as getComponentBlueprint } from './get-component-blueprint.js';
import { tool as verifyColorContrast } from './verify-color-contrast.js';
import { tool as auditUiCode } from './audit-ui-code.js';
import { tool as fixUiSlop } from './fix-ui-slop.js';
import { tool as scaffoldDesignContract } from './scaffold-design-contract.js';

export const TOOL_REGISTRY = [
  searchArchetypes,
  getDesignTokens,
  getComponentBlueprint,
  verifyColorContrast,
  auditUiCode,
  fixUiSlop,
  scaffoldDesignContract
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
