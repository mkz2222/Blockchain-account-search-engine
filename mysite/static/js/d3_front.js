var dataArray = {{ key_vol|safe }};
var width = document.getElementsByClassName("p01ar3_2_2")[0].offsetWidth;
var height = 360;


var widthScale = d3.scaleLinear()
                .domain([0, d3.max(dataArray)])
                .range([0, width*0.96]);

var canvas = d3.select(".p01ar3_2_2")
              .append("svg")
              .attr("width", width)
              .attr("height", height);

var bars = canvas.selectAll("rect")
            .data(dataArray)
            .enter()
                .append("rect")
                .attr("width", function(d) {return widthScale(d); })
                .attr("height", 22)
                .attr("fill", "#21b1ef")
                .attr("y", function(d, i) { return i * 32});