// Single source of truth for backend URLs.
// Set VITE_API_URL in Netlify (build-time). Falls back to local dev server.
const rawBase = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

export const API_BASE_URL = rawBase.replace(/\/+$/, "");

export const ENDPOINTS = {
  chat: `${API_BASE_URL}/chat`,
  health: `${API_BASE_URL}/health`,
} as const;
