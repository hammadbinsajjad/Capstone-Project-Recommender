import { Message } from "../types";
import { API_ENDPOINTS } from "./constants";
import { authHeaders, jsonHeaders } from "./helpers";

const registerUser = async (fullName: string, email: string, password: string) => {
    const response = await fetch(API_ENDPOINTS.REGISTER, {
        method: "POST",
        headers: jsonHeaders(),
        body: JSON.stringify({
            full_name: fullName,
            email: email,
            password: password,
        }),
    });

    if (!response.ok) {
        throw new Error("Unable to register user, please try again");
    }

    return await response.json();
};


const loginUser = async (email: string, password: string) => {
    const response = await fetch(API_ENDPOINTS.LOGIN, {
        method: "POST",
        headers: jsonHeaders(),
        body: JSON.stringify({
            email: email,
            password: password,
        }),
    });

    if (!response.ok) {
        throw new Error("Unable to login user, please try again");
    }

    return await response.json();
};


const loggedInUser = async () => {
    const response = await fetch(API_ENDPOINTS.LOGGED_IN_USER, {
        method: "GET",
        headers: authHeaders(),
    });

    if (!response.ok) {
        throw new Error("Unable to fetch user data");
    }

    return await response.json();
};


const chatHistory = async () => {
    const response = await fetch(API_ENDPOINTS.CHATS, {
        method: "GET",
        headers: authHeaders(),
    });

    if (!response.ok) {
        throw new Error("Unable to fetch chat history");
    }

    const chats = [];

    for (const chat of (await response.json())) {
        chats.push({
            id: chat.id,
            title: chat.title,
            queryPreview: chat.query_preview,
            lastUpdated: chat.last_updated,
            messageCount: chat.message_count,
        });
    }

    return chats;
};


const verifyToken = async (token: string) => {
    const response = await fetch(API_ENDPOINTS.VERIFY_TOKEN, {
        method: "POST",
        headers: jsonHeaders(),
        body: JSON.stringify({
            token: token,
        }),
    });

    return response;
};


const refreshToken = async (refreshToken: string) => {
    const response = await fetch(API_ENDPOINTS.REFRESH_TOKEN, {
        method: "POST",
        headers: jsonHeaders(),
        body: JSON.stringify({
            refresh: refreshToken,
        }),
    });

    if (!response.ok) {
        return {};
    }

    return await response.json();
}


const chatMessages = async (chatId: number) : Promise<Message[]> => {
    const response = await fetch(`${API_ENDPOINTS.CHATS}${chatId}`, {
        method: "GET",
        headers: authHeaders(),
    });

    if (!response.ok) {
        throw new Error("Unable to fetch chat messages");
    }

    const messages = [];
    const data = await response.json();
    const raw_messages = data.messages;

    for (let messageIndex = 0; messageIndex < raw_messages.length; messageIndex++) {
        const message = raw_messages[messageIndex];

        if (message.role !== "user" && message.role !== "assistant") {
            continue;
        }

        if (!message.content || message.content.trim() === "") {
            continue;
        }

        messages.push({
            id: messageIndex,
            content: message.content,
            isUser: message.role === "user",
        });
    }

    return messages;
};


const createChat = async (query: string) => {
    const response = await fetch(API_ENDPOINTS.CHATS, {
        method: "POST",
        headers: authHeaders(),
        body: JSON.stringify({
            user_query: query,
        }),
    });

    if (!response.ok) {
        throw new Error("Unable to create new chat");
    }

    return await response.json();
};


const continueChat = async (chatId: number, query: string) => {
    const response = await fetch(`${API_ENDPOINTS.CHATS}${chatId}/`, {
        method: "PUT",
        headers: authHeaders(),
        body: JSON.stringify({
            user_query: query,
        }),
    });

    if (!response.ok) {
        throw new Error("Unable to send message");
    }

    const raw_ai_response = await response.json();

    return raw_ai_response.ai_response;
};


export {
    registerUser, loginUser, loggedInUser,
    chatHistory, verifyToken, refreshToken,
    chatMessages, continueChat, createChat,
};
