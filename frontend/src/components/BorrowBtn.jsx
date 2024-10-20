import React from "react"
import "../styles/components/BorrowBtn.css"


const BorrowBtn = ({ children }) => {
    return (
        <button className="borrow_btn">
            { children }
        </button>
    )
}

export default BorrowBtn
