import React from "react";


export default function CourseResults(props) {

    const results = props.results;

    return (
        <div>
            <ul>
                {Object.keys(results).map((ex, index) => (
                    <li key={index}>{ex}: {results[ex]["correct"]} / {results[ex]["total"]}</li>
                ))}
            </ul>

        </div>
    );

}