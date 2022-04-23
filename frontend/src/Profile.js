import React, { useState } from "react";
import { useNavigate } from "react-router";
import { fetchToken, setToken } from "./Auth";
import axios from "axios";
import ShowCourse from "./ShowCourse";

export default function Profile() {
    const navigate = useNavigate();
    const [data, setData] = useState(new Map());
    const [isLoading, setIsLoading] = React.useState(true);

    const [course, setCourse] = useState("Select a course");
    const [courseData, setCourseData] = useState(new Map());


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

    const handleCourseChange = (e) => {
        setCourse(e.target.value)
    }

    const getCourse = () => {
        if (course === "Select a course") {
            return;
        } else {
            // make api call to our backend. we'll leave thisfor later
            const url = "http://localhost:8000/results/" + course;
            const token = fetchToken();
            axios
                .get(url, {
                    headers: {
                        'Authorization': token,
                    }
                })
                .then(function (response) {
                    console.log(response);
                    setCourseData(response.data);
                })
                .catch(function (error) {
                    console.log(error, "error");
                });
        }
    };




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

                    <div>
                        <select onChange={handleCourseChange}>
                            <option value="Select a course"> -- Select a course -- </option>
                            {/* Mapping through each fruit object in our fruits array
                        and returning an option element with the appropriate attributes / values.
                        */}
                            {data.courses.map((course, index) => <option key={index} value={course.name}>{course.name}</option>)}

                        </select>
                        <button type="button" onClick={getCourse}>Get Course Info</button>
                        {Object.keys(courseData).length !== 0 ? (
                            <ShowCourse results={courseData} />) : (<div></div>)}
                    </div>)}

            </div>
        </>
    );
}