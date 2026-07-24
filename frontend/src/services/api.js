import axios from "axios"
import { getToken } from "./auth"

const BASE_URL = "http://localhost:8000"

const authHeaders = () => ({
    Headers: {
        Authorization: `Bearer ${getToken()}`
    }
})

export const getIndicators = (severity = null, type = null) => {
    
}


export const getAlerts = (severity = null) => { ... }
export const getFeeds = (country = null, city = null) => { ... }
export const getStats = () => { ... }