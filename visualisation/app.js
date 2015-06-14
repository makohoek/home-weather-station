function addAxesAndLegend (svg, xAxis, yAxis, margin, chartWidth, chartHeight) {
  // clipping to make sure nothing appears behind legend
  svg.append('clipPath')
    .attr('id', 'axes-clip')
    .append('polygon')
      .attr('points', (-margin.left)                 + ',' + (-margin.top)                 + ' ' +
                      (chartWidth)                   + ',' + (-margin.top)                 + ' ' +
                      (chartWidth)                   + ',' + 0                  + ' ' +
                      (chartWidth + margin.right)    + ',' + 0                  + ' ' +
                      (chartWidth + margin.right)    + ',' + (chartHeight + margin.bottom) + ' ' +
                      (-margin.left)                 + ',' + (chartHeight + margin.bottom));

  var axes = svg.append('g')
    .attr('clip-path', 'url(#axes-clip)');

  axes.append('g')
    .attr('class', 'x axis')
    .attr('transform', 'translate(0,' + chartHeight + ')')
    .call(xAxis);

  axes.append('g')
    .attr('class', 'y axis')
    .call(yAxis)
    .append('text')
      .attr('transform', 'rotate(-90)')
      .attr('y', 6)
      .attr('dy', '.71em')
      .style('text-anchor', 'end')
      .text('Temperature (c)');
}

function drawPaths (svg, data, x, y) {

  var medianLine = d3.svg.line()
    .interpolate('basis')
    .x(function (d) { return x(d.time); })
    .y(function (d) { return y(d.temperature); });

  svg.datum(data);

  svg.append('path')
    .attr('class', 'median-line')
    .attr('d', medianLine)
    .attr('clip-path', 'url(#rect-clip)');
}

function makeChart (data) {
  var svgWidth  = 960,
      svgHeight = 500,
      margin = { top: 20, right: 20, bottom: 40, left: 40 },
      chartWidth  = svgWidth  - margin.left - margin.right,
      chartHeight = svgHeight - margin.top  - margin.bottom;

  var maxTemperatureValue = 30;
  var minTemperatureValue = 18;

  var x = d3.time.scale().range([0, chartWidth])
            .domain(d3.extent(data, function (d) { return d.time; })),
      y = d3.scale.linear().range([chartHeight, 0])
            .domain([minTemperatureValue, maxTemperatureValue]);

  var xAxis = d3.svg.axis().scale(x).orient('bottom')
                .innerTickSize(-chartHeight).outerTickSize(0).tickPadding(10),
      yAxis = d3.svg.axis().scale(y).orient('left')
                .innerTickSize(-chartWidth).outerTickSize(0).tickPadding(10);

  var svg = d3.select('body').append('svg')
    .attr('width',  svgWidth)
    .attr('height', svgHeight)
    .append('g')
      .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

  addAxesAndLegend(svg, xAxis, yAxis, margin, chartWidth, chartHeight);
  drawPaths(svg, data, x, y);
}

var parseDate  = d3.time.format('%Y-%m-%d').parse;
var parseTime = d3.time.format('%H:%M:%S').parse;

var today = new Date();
var format = d3.time.format('%Y-%m-%d');
var today_string = format(today);

function drawChartByDateName(filename){
  d3.json(filename, function (error, rawData) {
    if (error) {
      console.error(error);
      return;
    }

    var data = rawData.map(function (d) {
      return {
        date:  parseDate(d.date),
        time:  parseTime(d.time),
        temperature: d.temperature,
      };
    });
    makeChart(data);
  });
}
drawChartByDateName(today_string)
