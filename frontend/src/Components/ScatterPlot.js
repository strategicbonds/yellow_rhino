import React, { useEffect, useState, useRef } from 'react';
import * as d3 from 'd3';

const ScatterPlot = () => {
    const [data, setData] = useState([]);
    const d3Container = useRef(null);

    // Correctly separated useEffect for fetching data
    useEffect(() => {
        // Fetch the data from the new endpoint that provides both mileage and price
        fetch('/api/car-price-mileage')
        .then(response => {
            console.log(response); // Log the raw response
            return response.json();
        })
        .then(data => {
            console.log("Fetched data:", data);
            setData(data);
        })
        .catch(error => console.error('Error fetching data:', error));
    
    }, []);    

    // useEffect for drawing the scatter plot
    useEffect(() => {
        if (data && d3Container.current) {
            const svg = d3.select(d3Container.current);
            const width = +svg.attr('width');
            const height = +svg.attr('height');

            // Define scales
            const xScale = d3.scaleLinear()
                .domain([0, d3.max(data, d => d.mileage)]) // Assuming 'mileage' is your x-value
                .range([0, width]);

            const yScale = d3.scaleLinear()
                .domain([0, d3.max(data, d => d.price)]) // Assuming 'price' is your y-value
                .range([height, 0]);

            // Add dots
            svg.selectAll(".dot")
                .data(data)
                .enter().append("circle") // Adds a new circle for each new data point
                .attr("class", "dot")
                .attr("cx", d => xScale(d.mileage))
                .attr("cy", d => yScale(d.price))
                .attr("r", 5); // Size of the dot

            console.log(d3.max(data, d => d.mileage));
            console.log(d3.max(data, d => d.price));
                
        }
    }, [data]); // This effect depends on the 'data' state

    return (
        <svg
            className="d3-component"
            width={600}
            height={400}
            ref={d3Container}
        />
    );
};

export default ScatterPlot;
