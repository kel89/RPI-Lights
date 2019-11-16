/* color wheel */

var ColorWheel = function(config){
	this.targetID = config.targetID;
	this.numColors = 12;
	this.bands = 4;

	// Creation sequence
	this.setupData();
	this.createSVG();
	this.setupHelpers();
	this.addWheel();
}

ColorWheel.prototype.setupData = function(){
	/*
	Setsup the color data for use in the wheel
	*/
	this.colors = d3.range(this.numColors).map((d,i) => d3.interpolateRainbow(i/this.numColors));


}

ColorWheel.prototype.createSVG = function(){
	/*
	Creates and places the SVG and other needed axes
	on the targetID Div
	*/
	this.divWidth = $("#" + this.targetID).width();
	// this.divHeight = $("#" + this.targetID).height();
	this.divHeight = this.divWidth;

	this.margin = {top: 10, right: 10, bottom: 10, left: 10};

	this.r = Math.min(this.divWidth - this.margin.right - this.margin.left,
			 this.divHeight - this.margin.top - this.margin.bottom)/2;

	this.bandwidth = this.r / this.bands;

	// Add the svg
	this.svg = d3.select("#"+this.targetID).append('svg')
			.attr('id', 'wheelSVG')
			.attr('width', this.divWidth)
			.attr('height', this.divHeight);

	// add the chart g, then move it to the *center*
	this.g = this.svg.append('g')
			.attr('transform', `translate(${this.margin.left + this.r}, ${this.margin.top + this.r})`);

}

ColorWheel.prototype.setupHelpers = function(){
	/*
	Sets up the axis helpers and arc helpers
	*/

	// Setup the radial scale
	this.rScale = d3.scaleLinear()
		.domain([0, this.bands])
		.range([0, this.r - this.bandwidth]);

	// setup the theta sacle
	this.angleScale = d3.scaleLinear()
		.domain([0, this.numColors])
		.range([0, 2*Math.PI]);

	// setup the arc
	this.arc = d3.arc()
		.cornerRadius(5)
		.padAngle(.02)
		.innerRadius(.5*this.r)
		.outerRadius(this.r);

	// setup the pie (does angles for us)
	this.pie = d3.pie()
		.sort(null)
		.value(d => 1);

}

ColorWheel.prototype.addWheel = function(){
	/*
	Adds the graphic to the SVG and attaches
	all the event handlers
	*/
	let _this = this;

	// make the pie data
	this.plotData = this.pie(this.colors);

	// add the slices
	this.slices = this.g.selectAll('.slices')
		.data(this.plotData)
		.enter()
		.append('path')
		.style('fill', d => d.data)
		.on('click', function(d){
			_this.centerCircle.style('fill', d.data);
			_this.centerText.style('opacity', '1')
						.style('fill', _this.getTextColor(d.data));

			console.log("Send color " + d.data);
		})

	// Transition the slices
	this.slices.transition()
		.delay((d,i) => i*80)
		.tween('data', d => {
			let i = d3.interpolate({endAngle:d.startAngle}, d);
			return t => d.current = i(t);
		})
		.attrTween('d', d => () => this.arc(d.current));

	// Add center circle
	this.centerCircle = this.g
		.append('circle')
		.attr('id', 'centerColorCircle')
		.attr('x', 0)
		.attr('y', 0)
		.attr('r', this.r*.47)
		.style('fill', 'none')
		.on('click', function(d){
			d3.select(this).style('fill', 'none')
			_this.centerText.style('opacity', '0');

			console.log("Command off");
		})

	// Add center text
	this.centerText = this.g.append('text')
		.text('Press to turn off')
		.style('text-anchor', 'middle')
		.style('opacity', '0')
		.attr('dy', '.5em');

}


ColorWheel.prototype.getTextColor = function(backgroundColor){
	let rgb = backgroundColor.substring(4, backgroundColor.length-1)
				.split(', ');
	let testVal = rgb[0]*.299 + rgb[1]*.587 + rgb[2]*.114;
	return (testVal > 130 ? 'black' : 'white');
}

 