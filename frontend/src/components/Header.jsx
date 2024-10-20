import React from "react";
import "../styles/components/Header.css"


const Header = () => {
    return (
        <header className="header_container">
            <article className="logo"><span>Read</span>Stream</article>
            <article className="nav">
                <nav className="link_container">
                    <a className="nav_links" href="#">books</a>
                    <a className="nav_links" href="#">authors</a>
                    <a className="nav_links" href="#">genres</a>
                </nav>
            </article>
            <article className="user">
                <p>username</p>
                <i className="fa-solid fa-user"></i>
            </article>
        </header>
    )
}

export default Header
