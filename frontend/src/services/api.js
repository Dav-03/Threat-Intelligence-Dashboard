import axios from "axios"
import { getToken } from "./auth"

const BASE_URL = "http://localhost:8000"

const authHeaders = () => ({
    headers: {
        Authorization: `Bearer ${getToken()}`
    }
})

export const getIndicators = async (severity = null, type = null) => {
    const response = await axios.get(`${BASE_URL}/indicators/`, {
        params: { severity, type },
        headers: authHeaders()
    });

    return response.data;
};


export const getAlerts = async (severity = null) => { 
    const response = await axios.get(`${BASE_URL}/alerts/`, {
        params: { severity },
        headers: authHeaders()
    });
    return response.data
};

export const getFeeds = async (country = null, city = null) => {
    const response = await axios.get(`${BASE_URL}/feeds`, {
        params: {country, city},
        headers: authHeaders()
    });
    return response.data
};

export const getStats = async () => {
    const response = await axios.get(
        `${BASE_URL}/stats/summary`,
        authHeaders()
    )
    return response.data
};