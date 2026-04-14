import axios from 'axios';
import type { AxiosInstance, InternalAxiosRequestConfig, AxiosError } from 'axios';

const API_URL = (import.meta.env.VITE_API_URL as string) || 'http://localhost:8000';

/**
 * Token manager using a closure — the access token is never stored
 * in localStorage, sessionStorage, cookies, or any other persistent storage.
 * It lives only in memory inside this closure.
 */
const tokenManager = (() => {
  let token: string | null = null;

  return {
    get: () => token,
    set: (t: string | null) => { token = t; },
    clear: () => { token = null; },
  };
})();

export const setAccessToken = tokenManager.set;
export const getAccessToken = tokenManager.get;
export const clearAccessToken = tokenManager.clear;

function extractErrorMessage(err: unknown): string {
  if (axios.isAxiosError(err)) {
    const data = err.response?.data as Record<string, unknown> | undefined;
    return (data?.detail as string) || (data?.message as string) || err.message;
  }
  return err instanceof Error ? err.message : 'Request failed';
}

/** Authenticated client — attaches access token to every request. */
export const apiClient: AxiosInstance = axios.create({ baseURL: API_URL, withCredentials: true });

/** Raw client — no interceptors, used for auth endpoints to avoid loops. */
const rawClient: AxiosInstance = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: { 'Content-Type': 'application/json' },
});

/*
 * REQUEST interceptor — reads token from closure and sets Authorization header.
 */
apiClient.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const t = tokenManager.get();
  config.headers = config.headers || {};
  if (t) {
    config.headers.Authorization = `Bearer ${t}`;
  }
  if (!(config.data instanceof FormData)) {
    config.headers['Content-Type'] = 'application/json';
  } else {
    delete config.headers['Content-Type'];
  }
  return config;
});

/*
 * Refresh deduplication — if multiple 401s fire at once, only one
 * refresh request is made; all waiters share the same promise.
 */
let refreshInFlight: Promise<string> | null = null;

async function refreshAccessToken(): Promise<string> {
  if (!refreshInFlight) {
    refreshInFlight = rawClient
      .post<{ access_token: string }>('/api/auth/token')
      .then((res) => {
        const newToken = res.data.access_token;
        tokenManager.set(newToken);
        return newToken;
      })
      .finally(() => { refreshInFlight = null; });
  }
  return refreshInFlight;
}

/** Ensure the user is authenticated — tries to refresh if no token. */
export async function ensureAuth(): Promise<void> {
  if (tokenManager.get()) return;
  await refreshAccessToken();
}

/** Logout — calls backend, clears token from closure. */
export async function logout(): Promise<void> {
  try { await rawClient.get('/api/auth/logout'); } catch { /* ignore */ }
  finally { tokenManager.clear(); }
}

/*
 * RESPONSE interceptor — on 401, automatically refreshes the access token
 * via POST /api/auth/token (refresh token is sent as httpOnly cookie by the
 * browser), then retries the original request with the new token.
 */
apiClient.interceptors.response.use(
  (res) => res,
  async (error: AxiosError) => {
    const req = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

    if (!error.response) {
      throw new Error(`Unable to connect to server at ${API_URL}`);
    }

    // If the refresh endpoint itself failed, don't loop
    if (req?.url?.includes('/api/auth/token')) {
      tokenManager.clear();
      throw new Error(extractErrorMessage(error));
    }

    // On 401, try to refresh once
    if (error.response.status === 401 && req && !req._retry) {
      req._retry = true;
      try {
        const newToken = await refreshAccessToken();
        req.headers = req.headers || {};
        req.headers.Authorization = `Bearer ${newToken}`;
        return apiClient.request(req);
      } catch (refreshErr) {
        tokenManager.clear();
        throw new Error(extractErrorMessage(refreshErr));
      }
    }

    throw new Error(extractErrorMessage(error));
  }
);
