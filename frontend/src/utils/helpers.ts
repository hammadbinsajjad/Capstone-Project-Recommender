import { verifyToken, refreshToken } from "./api";

const jsonHeaders = () => {
    return {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    };
};


const authHeaders = () => {
    const token = JSON.parse(localStorage.getItem('tokens') || "{}");
    if (!token) {
        throw new Error("No authentication token found");
    }

    return {
        ...jsonHeaders(),
        'Authorization': `Bearer ${token.access}`,
    };
};


const isLoggedIn = async () => {
    const token = JSON.parse(localStorage.getItem('tokens') || "{}");

    if (!token || !token.access) {
        return false;
    }

    const response = await verifyToken(token.access);

    if (response.ok) {
        return true;
    }

    const refreshedToken = await refreshToken(token.refresh);

    if (refreshedToken && refreshedToken.access) {
        const previous_tokens = localStorage.getItem('tokens') || "{}";
        const updated_tokens = { ...JSON.parse(previous_tokens), ...refreshedToken };
        localStorage.setItem('tokens', JSON.stringify(updated_tokens));

        return true;
    }

    localStorage.removeItem('tokens');
    return false;
};


const formatDate = (date: string) => {
    return new Date(date).toLocaleString();
};


export {
    jsonHeaders, authHeaders, isLoggedIn,
    formatDate,
};
