import { useNavigate } from "react-router";
import { fetchToken, setToken } from "./Auth";
import { useState } from "react";
import axios from "axios";
import React from "react";




export default function Login() {
    const navigate = useNavigate();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    //check to see if the fields are not empty
    const login = () => {
        if ((username == "") & (password == "")) {
            return;
        } else {
            // make api call to our backend. we'll leave thisfor later
            const params = new URLSearchParams();
            params.append('username', username);
            params.append('password', password);
            axios
                .post("http://localhost:8000/token/", params)
                .then(function (response) {
                    console.log(response.data["access_token"], "response.data.token");
                    if (response.data["access_token"]) {
                        setToken("Bearer " + response.data["access_token"]);
                        navigate("/profile");
                    }
                })
                .catch(function (error) {
                    console.log(error, "error");
                });
        }
    };

    return (
        <div style={{ minHeight: 800, marginTop: 30 }}>
            <h1>login page</h1>
            <div style={{ marginTop: 30 }}>
                {fetchToken() ? (
                    <p>you are logged in</p>
                ) : (
                    <div className="login-form">
                        <form>
                            <label style={{ marginRight: 10 }}>Input Username</label>
                            <input
                                type="text"
                                onChange={(e) => setUsername(e.target.value)}
                            />

                            <label style={{ marginRight: 10 }}>Input Password</label>
                            <input
                                type="text"
                                onChange={(e) => setPassword(e.target.value)}
                            />

                            <button type="button" onClick={login}>
                                Login
                            </button>
                        </form>
                    </div>
                )}
            </div>
        </div>
    );
}