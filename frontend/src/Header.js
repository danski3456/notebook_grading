import { useNavigate } from "react-router";
import React from "react";

export default function Profile() {

    const navigate = useNavigate();

    const signOut = () => {
        localStorage.removeItem("temitope");
        navigate("/");
    };

    return (
        <div className="header">
            <div className="title">
                <h1>Title</h1>
            </div>
            <div className="menu">
                <div className="menu-item">
                    <a href="/">Home</a>
                </div>
                <div className="menu-item">
                    <a href="/profile">Profile</a>
                </div>
                <div className="menu-item">
                    <a href="/results">Results</a>
                </div>
                <div className="menu-item">
                    <button onClick={signOut}>Sign Out</button>
                </div>

            </div>
        </div>
    )

}

