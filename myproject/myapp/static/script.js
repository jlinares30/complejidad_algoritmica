const grafoData = JSON.parse(document.getElementById('grafo-data').textContent);
        const svg = d3.select("svg")
            .attr("width", 1200)
            .attr("height", 800)

        const g = svg.append("g");

        const zoom = d3.zoom()
            .scaleExtent([0.5, 10])
            .on("zoom", (event) => {
                g.attr("transform", event.transform);
            });

        svg.call(zoom);

        const width = +svg.attr("width");
        const height = +svg.attr("height");


        const simulation = d3.forceSimulation(grafoData.nodos)
            .force("link", d3.forceLink(grafoData.aristas).id(d => d.id).distance(1200))
            .force("charge", d3.forceManyBody().strength(-1000))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("collision", d3.forceCollide().radius(160)); 

        const link = g.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(grafoData.aristas)
            .enter()
            .append("line")
            .attr("stroke-width", d => -60)
            .attr("stroke", "#999")
            .attr("opacity", 0.6);

        const node = g.append("g")
            .attr("class", "nodes")
            .selectAll("circle")
            .data(grafoData.nodos)
            .enter()
            .append("circle")
            .attr("r", 10)
            .attr("fill", d => d.tipo === 'Inicial' ? 'green' : (d.tipo === 'Proveedor' ? '#ffc107' : '#17a2b8'))
            .call(d3.drag()
                .on("start", dragStarted)
                .on("drag", dragged)
                .on("end", dragEnded));

        const labels = g.append("g")
            .attr("class", "node-label")
            .selectAll("text")
            .data(grafoData.nodos)
            .enter()
            .append("text")
            .attr("class", "node-label")
            .attr("dx", 12)
            .attr("dy", ".35em")
            .text(d => d.id)
            .style("visibility", "visible");

        const edgeLabels = g.append("g")
            .attr("class", "edge-labels")
            .selectAll("text")
            .data(grafoData.aristas)
            .enter()
            .append("text")
            .attr("dx", 20)
            .attr("dy", ".35em")
            .text(d => d.weight + " ms")
            .style("visibility", "visible"); 
        

        function ticked() {
            link.attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            node.attr("cx", d => d.x)
                .attr("cy", d => d.y);

            labels.attr("x", d => d.x)
                .attr("y", d => d.y);

            edgeLabels.attr("x", d => (d.source.x + d.target.x) / 2)
                .attr("y", d => (d.source.y + d.target.y) / 2);
        }

        simulation.on("tick", ticked);
        simulation.alpha(1).restart();  
        setTimeout(() => simulation.stop(), 3000); 


        svg.on("dblclick.zoom", null); 
        svg.on("click", (event) => {
            const scale = svg.property("__zoom").k;
            if (scale > 2) {
                labels.style("visibility", "visible");
                edgeLabels.style("visibility", "visible");
            } else {
                labels.style("visibility", "hidden");
                edgeLabels.style("visibility", "hidden");
            }
        });

        function dragStarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }

        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }

        function dragEnded(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }

        ticked();