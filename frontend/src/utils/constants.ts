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


const STARTING_AI_MESSAGE = (
    "Hello! I'm your DataTalksClub capstone project assistant. " +
    "I'm here to help you brainstorm and develop ideas for your " +
    "capstone project across any of our courses - ML Engineering, " +
    "Data Engineering, MLOps, LLMs, and more!\n\nWhich " +
    "course are you taking, and what kind of project are you thinking about?"
)

export {
    API_ENDPOINTS, STARTING_AI_MESSAGE
};
