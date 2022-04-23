import React from "react";
import CourseResults from "./CourseResults";



export default function ShowCourse(props) {

    const results = props.results;
    console.log(results);
    console.log(students);
    const students = Object.keys(props.results);

    const exercises = Object.keys(results[students[0]]);
    const columns = ["Student ID"].concat(exercises).concat(["Total"]);

    return (
        <div>
            <table>
                <tr>
                    {columns.map((col, index) => (
                        <th key={index}>{col}</th>
                    ))}
                </tr>
                {students.map((student, index) => (
                    <tr key={index}>
                        <td>{student}</td>
                        {exercises.map((ex, index2) => (
                            <td key={index2}>{results[student][ex]["correct"]} ({results[student][ex]["total"]})</td>

                        ))}
                        <td> {exercises.map((e) => results[student][e]["correct"]).reduce((p, c) => p + c, 0)} ({exercises.map((e) => results[student][e]["total"]).reduce((p, c) => p + c, 0)}) </td>


                    </tr>
                ))}
            </table>
            {/* <ul>
                {Object.keys(students).map((student, index) => (
                    <div key={index}>
                        <h1>{student}</h1>
                        <CourseResults results={students[student]} />
                    </div>
                ))}
            </ul> */}

        </div>
    );

}