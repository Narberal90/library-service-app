import React, {useState} from "react";
import { useNavigate } from "react-router-dom";
import { register } from "../../apiService";

import "../../styles/pages/authorization/Login.css"
import LoginBtn from "../../components/LoginBtn";


const Register = () => {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [email, setEmail] = useState("")
    const [error, setError] = useState("")
    const navigate = useNavigate()

    const handleRegister = async (event) => {
        event.preventDefault()
        try {
            await register(username, password, email)
            navigate("/login")
        }
        catch (error){
            setError("Error of registration")
        }
    }
    return (
        <div className="authenticate_container">
            <div className="login">
                <h1>Registration</h1>
                <form onSubmit={handleRegister} className="login_form">
                    <div>
                        <input
                            type="text"
                            value={username}
                            onChange={event => setUsername(event.target.value)}
                            className="login_input"
                            placeholder="username..."
                            required
                        />
                    </div>
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
                    <LoginBtn type="submit">Sign up</LoginBtn>
                </form>
            </div>
        </div>
    )
}

export default Register
