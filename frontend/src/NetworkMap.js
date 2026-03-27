import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import './NetworkMap.css';

function NetworkMap({ networks, devices }) {
  const svgRef = useRef();
  const [dimensions, setDimensions] = useState({ width: 300, height: 250 });

  useEffect(() => {
    const updateDimensions = () => {
      const container = svgRef.current?.parentElement;
      if (container) {
        const width = container.offsetWidth - 20;
        const height = Math.min(width * 0.7, window.innerWidth < 600 ? 250 : 350);
        setDimensions({ width, height });
      }
    };

    updateDimensions();
    window.addEventListener('resize', updateDimensions);
    return () => window.removeEventListener('resize', updateDimensions);
  }, []);

  useEffect(() => {
    if (!networks || networks.length === 0) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const { width, height } = dimensions;
    const padding = Math.max(30, width * 0.08);

    svg.attr('viewBox', `0 0 ${width} ${height}`)
       .attr('preserveAspectRatio', 'xMidYMid meet');

    // Create nodes from REAL networks only
    const nodes = networks.map((network, i) => ({
      id: network.bssid || `network-${i}`,
      label: network.ssid || 'Unknown',
      type: 'network',
      risk: network.risk_category || 'low',
      connected: network.connected || false,
      x: width / 2,
      y: height / 2
    }));

    // Add REAL device nodes from captured packets
    if (devices && typeof devices === 'object') {
      Object.entries(devices).forEach(([mac, device]) => {
        if (device.type === 'Client') {
          nodes.push({
            id: mac,
            label: 'Device',
            type: 'device',
            connectedTo: device.ssid,
            x: width / 2,
            y: height / 2
          });
        }
      });
    }

    // Add YOUR device if connected to a network
    const connectedNetwork = networks.find(n => n.connected);
    if (connectedNetwork) {
      nodes.push({
        id: 'your-device',
        label: 'Your Device',
        type: 'device',
        connectedTo: connectedNetwork.ssid,
        isYourDevice: true,
        x: width / 2,
        y: height / 2
      });
    }

    // Create links between REAL devices and networks
    const links = [];
    nodes.forEach(node => {
      if (node.type === 'device' && node.connectedTo) {
        const target = nodes.find(n => n.type === 'network' && n.label === node.connectedTo);
        if (target) {
          links.push({
            source: node.id,
            target: target.id
          });
        }
      }
    });

    // Responsive node sizes
    const networkRadius = width < 400 ? 20 : 25;
    const deviceRadius = width < 400 ? 12 : 15;
    const fontSize = width < 400 ? 14 : 18;
    const labelFontSize = width < 400 ? 9 : 11;

    // Create force simulation with boundary constraints
    const simulation = d3.forceSimulation(nodes)
      .force('link', d3.forceLink(links).id(d => d.id).distance(width < 400 ? 80 : 100))
      .force('charge', d3.forceManyBody().strength(width < 400 ? -300 : -400))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius(width < 400 ? 35 : 40))
      .force('x', d3.forceX(width / 2).strength(0.1))
      .force('y', d3.forceY(height / 2).strength(0.1));

    // Draw links
    const link = svg.append('g')
      .selectAll('line')
      .data(links)
      .enter()
      .append('line')
      .attr('stroke', '#444')
      .attr('stroke-width', width < 400 ? 1.5 : 2)
      .attr('stroke-opacity', 0.6);

    // Draw nodes
    const node = svg.append('g')
      .selectAll('g')
      .data(nodes)
      .enter()
      .append('g')
      .call(d3.drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended));

    // Add circles
    node.append('circle')
      .attr('r', d => d.type === 'network' ? networkRadius : deviceRadius)
      .attr('fill', d => {
        if (d.type === 'device') {
          return d.isYourDevice ? '#9b59b6' : '#4a90e2';
        }
        if (d.risk === 'high') return '#ff4444';
        if (d.risk === 'medium') return '#ffaa00';
        return '#00ff88';
      })
      .attr('stroke', d => d.connected ? '#ffff00' : '#fff')
      .attr('stroke-width', d => d.connected ? 3 : 2)
      .style('cursor', 'pointer');

    // Add icons
    node.append('text')
      .text(d => {
        if (d.type === 'network') return '📡';
        return d.isYourDevice ? '👤' : '💻';
      })
      .attr('x', 0)
      .attr('y', 5)
      .attr('text-anchor', 'middle')
      .attr('font-size', `${fontSize}px`)
      .style('pointer-events', 'none');

    // Add labels with connected indicator
    node.append('text')
      .text(d => {
        const maxLength = width < 400 ? 8 : 12;
        const label = d.label.substring(0, maxLength);
        return d.connected ? `⭐ ${label}` : label;
      })
      .attr('x', 0)
      .attr('y', width < 400 ? 30 : 35)
      .attr('text-anchor', 'middle')
      .attr('fill', d => d.connected ? '#ffff00' : '#fff')
      .attr('font-size', `${labelFontSize}px`)
      .attr('font-weight', d => d.connected ? '700' : '600')
      .style('pointer-events', 'none');

    // Update positions with boundary constraints
    simulation.on('tick', () => {
      // Constrain nodes within bounds
      nodes.forEach(d => {
        d.x = Math.max(padding, Math.min(width - padding, d.x));
        d.y = Math.max(padding, Math.min(height - padding, d.y));
      });

      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);

      node.attr('transform', d => `translate(${d.x},${d.y})`);
    });

    function dragstarted(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event, d) {
      // Constrain dragging within bounds
      d.fx = Math.max(padding, Math.min(width - padding, event.x));
      d.fy = Math.max(padding, Math.min(height - padding, event.y));
    }

    function dragended(event, d) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

    // Stop simulation after nodes settle
    setTimeout(() => {
      simulation.stop();
    }, 3000);

  }, [networks, devices, dimensions]);

  return (
    <div className="network-map">
      {networks && networks.length > 0 ? (
        <>
          <svg ref={svgRef}></svg>
          <div className="map-legend">
            <div className="legend-item">
              <span className="legend-color high"></span>
              <span>High Risk</span>
            </div>
            <div className="legend-item">
              <span className="legend-color medium"></span>
              <span>Medium Risk</span>
            </div>
            <div className="legend-item">
              <span className="legend-color low"></span>
              <span>Low Risk</span>
            </div>
            <div className="legend-item">
              <span className="legend-color your-device"></span>
              <span>Your Device</span>
            </div>
          </div>
        </>
      ) : (
        <div className="no-data">
          <p>No networks detected yet. Start scanning to see the network map.</p>
        </div>
      )}
    </div>
  );
}

export default NetworkMap;
