/* -------------------------- REVENUE LINE CHART STARTS --------------------------*/
function renderRevenueChart(revenueData) {
    const margin = { top: 50, right: 50, bottom: 100, left: 60 },
          width = 960 - margin.left - margin.right,
          height = 500 - margin.top - margin.bottom;

    const svg = d3.select("#revenue-chart")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    // Scale the range of the data
    var x = d3.scaleBand()
        .range([0, width])
        .padding(0.1);
    var y = d3.scaleLinear()
        .range([height, 0]);

    x.domain(revenueData.map(function(d) { return d.date; }));
    y.domain([0, d3.max(revenueData, function(d) { return d.revenue; })]);

    // Add the X Axis
    svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x))
        .selectAll("text")
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", ".15em")
        .attr("transform", "rotate(-65)");

    // Add the Y Axis
    svg.append("g")
        .call(d3.axisLeft(y));

    // Define the line
    var line = d3.line()
        .x(function(d) { return x(d.date) + x.bandwidth() / 2; }) // center the line in the band
        .y(function(d) { return y(d.revenue); });

    // Add the line path
    svg.append("path")
        .data([revenueData])
        .attr("class", "line")
        .attr("d", line);

    var tooltip = d3.select("#tooltip");
    // Add circles for each data point
    svg.selectAll(".dot")
        .data(revenueData)
        .enter().append("circle")
        .attr("class", "dot")
        .attr("cx", function(d) { return x(d.date) + x.bandwidth() / 2; })
        .attr("cy", function(d) { return y(d.revenue); })
        .attr("r", 5)
        .on("mouseover", function(event, d) {
            tooltip.transition()
                .duration(200)
                .style("opacity", .9);
            // Set the content of the tooltip directly
            tooltip.html(`<strong>Date:</strong> ${d3.timeFormat("%B, %Y")(d.date)}<br/><strong>Revenue:</strong> £${d.revenue.toFixed(2)}`)
                .style("left", (event.pageX + 10) + "px")
                .style("top", (event.pageY - 10) + "px");
            d3.select(this).attr("r", 8); // Enlarge the circle on hover
        })
        .on("mouseout", function(d) {
            tooltip.transition()
                .duration(500)
                .style("opacity", 0);
            d3.select(this).attr("r", 5); // Reset the circle size
    });
}

function fetchAndRenderCharts() {
    fetch('/api/revenue')
        .then(response => response.json())
        .then(data => {
            console.log("Fetched revenue data:", data);
            renderRevenueChart(data);
        })
        .catch(error => console.error('Error fetching revenue data:', error));
}
/* -------------------------- REVENUE LINE CHART ENDS --------------------------*/


/* -------------------------- SERVICE POPULARITY CHART STARTS --------------------------*/
function renderCustomerSegmentationChart(segmentationData) {
    const width = 450,
          height = 450,
          margin = 40,
          radius = Math.min(width, height) / 2 - margin;

    const svg = d3.select("#customer-segmentation-chart")
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", `translate(${width / 2}, ${height / 2})`);

    const color = d3.scaleOrdinal(d3.schemeCategory10);

    const pie = d3.pie()
        .sort(null)
        .value(d => d.count);

    const arc = d3.arc()
        .innerRadius(radius * 0.4)
        .outerRadius(radius * 0.8);

    const arcs = pie(segmentationData);

    svg.selectAll("arc")
        .data(arcs)
        .enter()
        .append("path")
        .attr("fill", d => color(d.data.service_name))
        .attr("d", arc);

    svg.selectAll("text")
        .data(arcs)
        .enter()
        .append("text")
        .attr("transform", d => `translate(${arc.centroid(d)})`)
        .attr("text-anchor", "middle")
        .text(d => d.data.service_name)
        .style("fill", "#fff")
        .style("font-size", 12);
}

function fetchAndRenderServicePopularityChart() {
    fetch('/api/service-popularity')
        .then(response => response.json())
        .then(data => {
            renderCustomerSegmentationChart(data);
        })
        .catch(error => console.error('Error fetching service popularity data:', error));
}
/* -------------------------- SERVICE POPULARITY CHART ENDS --------------------------*/


/* -------------------------- CUSTOMER SEGMENTATION CHART STARTS --------------------------*/
function renderCustomerSegmentationPieChart(segmentationData) {
    const width = 450,
          height = 450,
          margin = 40;

    const radius = Math.min(width, height) / 2 - margin;

    const svg = d3.select("#customer-segmentation-chart")
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", `translate(${width / 2}, ${height / 2})`);

    const color = d3.scaleOrdinal(d3.schemeCategory10);

    const pie = d3.pie()
        .value(d => d.bill_count);  // Updated to use 'bill_count'

    const data_ready = pie(segmentationData);

    const arc = d3.arc()
        .innerRadius(0)
        .outerRadius(radius);

    const arcLabel = d3.arc()
        .innerRadius(radius * 0.7)
        .outerRadius(radius);

    // Tooltip div for displaying names on hover
    const tooltip = d3.select("#customer-segmentation-chart")
        .append("div")
        .style("opacity", 0)
        .attr("class", "tooltip")
        .style("position", "absolute")
        .style("text-align", "center")
        .style("padding", "6px")
        .style("background", "white")
        .style("border", "1px solid #ccc")
        .style("border-radius", "5px")
        .style("pointer-events", "none");

    svg
      .selectAll('pieces')
      .data(data_ready)
      .enter()
      .append('path')
      .attr('d', arc)
      .attr('fill', d => color(d.data.customer_name))  // Updated to use 'customer_name'
      .attr("stroke", "white")
      .style("stroke-width", "2px")
      .style("opacity", 0.7)
      .on('mouseover', (event, d) => {
          tooltip.style("opacity", 1);
          tooltip.html(d.data.customer_name)  // Updated to use 'customer_name'
              .style("left", (event.pageX) + "px")
              .style("top", (event.pageY - 28) + "px");
      })
      .on('mouseout', () => {
          tooltip.style("opacity", 0);
      });
}

function fetchAndRenderCustomerSegmentationChart() {
    fetch('/api/customer-segmentation')
        .then(response => response.json())
        .then(data => {
            renderCustomerSegmentationPieChart(data);
        })
        .catch(error => console.error('Error fetching customer segmentation data:', error));
}
/* -------------------------- CUSTOMER SEGMENTATION CHART ENDS --------------------------*/


//Add event listener to the DOMContentLoaded event
document.addEventListener('DOMContentLoaded', function() {
    fetchAndRenderCharts();
    fetchAndRenderServicePopularityChart();
    fetchAndRenderCustomerSegmentationChart();
})
