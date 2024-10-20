import React from "react"
import "../styles/components/OrderBtn.css"


const OrderBtn = ({ children }) => {
    return (
        <button className="order_btn">
            { children }
        </button>
    )
}

export default OrderBtn