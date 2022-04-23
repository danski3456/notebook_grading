import React, { useState } from "react";
import { useNavigate } from "react-router";
import { fetchToken, setToken } from "./Auth";
import axios from "axios";

export default function Profile() {
    const navigate = useNavigate();
    const [data, setData] = useState(new Map());
    const [isLoading, setIsLoading] = React.useState(true);


    const signOut = () => {
        localStorage.removeItem("temitope");
        navigate("/");
    };


    React.useEffect(() => {
        const token = fetchToken();
        axios.get("http://localhost:8000/users/me",
            {
                "headers": {
                    "Authorization": token,
                }
            })
            .then((response) => setData(response.data))
            .catch((error) => console.log(error))
        console.log("Hello");
    }, []);

    React.useEffect(() => {
        if (data.size !== 0) {
            setIsLoading(false);
        }
        console.log(data);
    }, [data]);

    return (
        <>
            <div style={{ marginTop: 20, minHeight: 700 }}>
                <h1>Profile page</h1>
                <p>Hello there, welcome to your profile page</p>

                {/* {userinfo.courses.map((course, index) => (
                    <p key={index}>{course.name}</p>
                ))} */}
                {isLoading ? (
                    <h1>Loading...</h1>
                ) : (
                    data.courses.map((course, index) => (
                        <p key={index}>{course.name}</p>
                    ))
                )}

                <button onClick={signOut}>sign out</button>
            </div>
        </>
    );
}