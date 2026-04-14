import { setAccessToken, getAccessToken, clearAccessToken } from '@/utils/api';

describe('Token manager (closure)', () => {
  afterEach(() => {
    clearAccessToken();
  });

  it('starts with null token', () => {
    expect(getAccessToken()).toBeNull();
  });

  it('stores and retrieves a token', () => {
    setAccessToken('abc123');
    expect(getAccessToken()).toBe('abc123');
  });

  it('clears the token', () => {
    setAccessToken('abc123');
    clearAccessToken();
    expect(getAccessToken()).toBeNull();
  });

  it('overwrites previous token', () => {
    setAccessToken('first');
    setAccessToken('second');
    expect(getAccessToken()).toBe('second');
  });

  it('token is not in localStorage', () => {
    setAccessToken('secret');
    expect(localStorage.getItem('accessToken')).toBeNull();
    expect(localStorage.getItem('access_token')).toBeNull();
    expect(localStorage.getItem('token')).toBeNull();
  });

  it('token is not in sessionStorage', () => {
    setAccessToken('secret');
    expect(sessionStorage.getItem('accessToken')).toBeNull();
    expect(sessionStorage.getItem('access_token')).toBeNull();
    expect(sessionStorage.getItem('token')).toBeNull();
  });
});
