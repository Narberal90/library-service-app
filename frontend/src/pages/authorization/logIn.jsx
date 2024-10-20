import React, { useState } from "react";
import { useNavigate } from "react-router-dom"
import { login } from "../../apiService";

import "../../styles/pages/authorization/Login.css"
import LoginBtn from "../../components/LoginBtn";


const Login = () => {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState("")
    const navigate = useNavigate()

    const handleLogin = async (event) => {
        event.preventDefault()
        try {
            const data = await login(email, password)
            if (data){
                navigate("/books")
            }
        }
        catch (error) {
            setError("Data is not valid")
        }
    }

    return(
        <div className="authenticate_container">
            <div className="login">
                <h1>Authorization</h1>
                <form onSubmit={handleLogin} className="login_form">
                    <div>
                        <input
                            type="email"
                            value={email}
                            onChange={event => setEmail(event.target.value)}
                            className="login_input"
                            placeholder="email..."
                            required
                        />
                    </div>
                    <div>
                        <input
                            type="password"
                            value={password}
                            onChange={event => setPassword(event.target.value)}
                            className="login_input"
                            placeholder="password..."
                            required
                        />
                    </div>
                    {error && <p>{error}</p>}
                    <LoginBtn type="submit">Login</LoginBtn>
                </form>
            </div>
        </div>
    )
}

export default Login
