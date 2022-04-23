import { useNavigate } from "react-router";
import React from "react";

export default function Profile() {

    const navigate = useNavigate();

    const signOut = () => {
        localStorage.removeItem("temitope");
        navigate("/");
    };

    return (
        <>
            <h1>Title</h1>
            <a href="/">Home</a>
            <a href="/profile">Profile</a>
            <a href="/results">Results</a>
            <button onClick={signOut}>Sign Out</button>
        </>
    )

}

