import React from "react";
import "../styles/components/LoginBtn.css"

const LoginBtn = ({ children, ...props }) => {
    return(
        <button {...props} className="login_btn">
            { children }
        </button>
    )
}

export default LoginBtn
