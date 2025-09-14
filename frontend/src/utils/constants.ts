const BASE_BACKEND_URL = 'http://localhost:8000/';

const BASE_AUTH_URL = `${BASE_BACKEND_URL}auth/`;

const BASE_API_URL = `${BASE_BACKEND_URL}api/`;

const BASE_CHATS_URL = `${BASE_API_URL}chats/`;

const API_ENDPOINTS = {
    REGISTER: `${BASE_AUTH_URL}users/`,
    LOGIN: `${BASE_AUTH_URL}jwt/create/`,
    REFRESH_TOKEN: `${BASE_AUTH_URL}jwt/refresh/`,
    VERIFY_TOKEN: `${BASE_AUTH_URL}jwt/verify/`,
    LOGGED_IN_USER: `${BASE_AUTH_URL}users/me/`,
    CHATS: `${BASE_CHATS_URL}`,
};

export { API_ENDPOINTS };
