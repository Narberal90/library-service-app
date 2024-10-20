import axios from "axios"

const API_URL = "http://localhost:8000/api"

export const login = async (email, password) => {
    try {
        const response = await axios.post(`${API_URL}/users/token/`, {
            email,
            password,
        },);

        if (response.data && response.data.access && response.data.refresh) {
            console.log('Login successful:', response.data);

            localStorage.setItem('accessToken', response.data.access);
            localStorage.setItem('refreshToken', response.data.refresh);

            axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`
            return response.data;
        } else {
            console.error('Tokens not found in response:', response.data);
            throw new Error('Invalid response: Tokens not found');
        }
    } catch (error) {
        if (error.response) {
            console.error('Error response from server:', error.response.data);
            console.error('Status code:', error.response.status);
            console.error('Headers:', error.response.headers);
        } else if (error.request) {
            console.error('No response received:', error.request);
        } else {
            console.error('Error during request setup:', error.message);
        }
        throw error;
    }
};


export const register  = async (username, password, email) => {
    const response = await axios.post(`${API_URL}/users/register/`, {
        username, password, email
    })
    return response.data
}

export const refreshToken = async () => {
    const refreshToken = localStorage.getItem('refreshToken')
    if (refreshToken){
        const response = await axios.post(`${API_URL}/users/token/refresh/`, {
            refresh: refreshToken
        })
        localStorage.setItem('accessToken', response.data.access)
        return response.data.access
    }
}

export const verifyToken = async () => {
    const accessToken = localStorage.getItem('accessToken')
    if (accessToken){
        const response = await axios.post(`${API_URL}/users/token/verify/`, {
            token: accessToken
        })
        return response.data
    }
}

export const getProtectedData = async () => {
    const accessToken = localStorage.getItem('accessToken')
    const response = await axios.get(`${API_URL}/library/`, {
        headers: {
            Authorization: `Bearer ${accessToken}`
        }
    })
    return response.data
}
