import React from "react";
import { useNavigate } from "react-router";
import { fetchToken, setToken } from "./Auth";
import { useState } from "react";
import axios from "axios";
import CourseResults from "./CourseResults";


export default function Results() {
    const navigate = useNavigate();
    const [student, setStudent] = useState("");
    const [course, setCourse] = useState("");
    const [results, setResults] = useState(new Map());
    const [isLoading, setIsLoading] = useState(true);

    //check to see if the fields are not empty
    const getResults = () => {
        if ((course == "") & (student == "")) {
            return;
        } else {
            // make api call to our backend. we'll leave thisfor later
            const url = "http://localhost:8000/results/" + course + "/" + student + "/"
            axios
                .get(url)
                .then(function (response) {
                    console.log(response)
                    setResults(response.data)
                })
                .catch(function (error) {
                    console.log(error, "error");
                });
        }
    };


    return (
        <div>

            <h1> Search your results </h1>

            <form>
                <label>Student Name</label>
                <input type="text" onChange={(e) => setStudent(e.target.value)} />
                <label>Course</label>
                <input type="text" onChange={(e) => setCourse(e.target.value)} />
                <button type="button" onClick={getResults}>Get Results!</button>
            </form>

            {<CourseResults results={results} />}


        </div>
    );
}