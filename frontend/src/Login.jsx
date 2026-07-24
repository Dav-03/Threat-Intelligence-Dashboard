import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios"
import { setToken } from "./services/auth"

function Login() {
    const [form, setForm] = useState({
        username: '',
        password: '',
    })
    const [error, setError] = useState(null)
    const navigate = useNavigate()

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value })
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        try{
            const response = await axios.post(
                'http://localhost:8000/auth/token',
                new URLSearchParams({
                    username: form.username,
                    password: form.password,
                    grant_type: 'password'
                }),
                { headers: { 'Content-Type': 'application/x-www-form-urlcoded'}}
            )
            setToken(response.data.access_token)
            navigate('/dashboard')

        } catch (err) {
            setError('Invalid username or password')
        }
    }

    return (
        <div>
            <h1>Threat Intel Dashboard</h1>
            {error && <p>{error}</p>}
            <form onSubmit={handleSubmit}>
                <input
                    name="username"
                    placeholder="username"
                    value={form.username}
                    onChange={handleChange}  
                />
                <input
                    name="password"
                    type="password"
                    placeholder="password"
                    value={form.password}
                    onChange={handleChange}
                />
                <button type="submit">Login</button>
            </form>
        </div>
    )
    
}

export default Login

