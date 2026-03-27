import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import './Charts.css';

function Charts({ networks }) {
  const [chartWidth, setChartWidth] = useState(300);

  useEffect(() => {
    const updateWidth = () => {
      const container = document.querySelector('.charts-panel');
      if (container) {
        setChartWidth(container.offsetWidth - 60); // Account for padding
      }
    };

    updateWidth();
    window.addEventListener('resize', updateWidth);
    return () => window.removeEventListener('resize', updateWidth);
  }, []);

  // Encryption type distribution
  const encryptionCounts = networks.reduce((acc, network) => {
    acc[network.encryption] = (acc[network.encryption] || 0) + 1;
    return acc;
  }, {});

  const pieData = [{
    values: Object.values(encryptionCounts),
    labels: Object.keys(encryptionCounts),
    type: 'pie',
    marker: {
      colors: ['#ff4444', '#ffaa00', '#00ff88', '#4a90e2', '#9b59b6']
    },
    textinfo: 'label+percent',
    textfont: {
      color: '#fff',
      size: chartWidth < 400 ? 10 : 12
    }
  }];

  const pieLayout = {
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: {
      color: '#fff',
      size: chartWidth < 400 ? 10 : 12
    },
    showlegend: chartWidth > 400,
    legend: {
      font: { color: '#fff', size: chartWidth < 400 ? 9 : 11 },
      orientation: chartWidth < 400 ? 'h' : 'v'
    },
    height: chartWidth < 400 ? 200 : 250,
    width: chartWidth,
    margin: { t: 10, b: 10, l: 10, r: 10 },
    autosize: true
  };

  // Signal strength bar chart
  const barData = [{
    x: networks.map(n => n.ssid.substring(0, chartWidth < 400 ? 8 : 15)),
    y: networks.map(n => n.signal_strength),
    type: 'bar',
    marker: {
      color: networks.map(n => {
        if (n.risk_category === 'high') return '#ff4444';
        if (n.risk_category === 'medium') return '#ffaa00';
        return '#00ff88';
      })
    }
  }];

  const barLayout = {
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: {
      color: '#fff',
      size: chartWidth < 400 ? 9 : 11
    },
    xaxis: {
      title: chartWidth > 400 ? 'Network' : '',
      color: '#fff',
      gridcolor: '#333',
      tickfont: { size: chartWidth < 400 ? 8 : 10 },
      tickangle: chartWidth < 400 ? -45 : -30
    },
    yaxis: {
      title: chartWidth > 400 ? 'Signal (dBm)' : 'dBm',
      color: '#fff',
      gridcolor: '#333',
      tickfont: { size: chartWidth < 400 ? 9 : 10 }
    },
    height: chartWidth < 400 ? 200 : 250,
    width: chartWidth,
    margin: { 
      t: 10, 
      b: chartWidth < 400 ? 50 : 60, 
      l: chartWidth < 400 ? 40 : 50, 
      r: 10 
    },
    autosize: true
  };

  // Risk heatmap data
  const heatmapData = [{
    z: [networks.map(n => n.risk_score)],
    x: networks.map(n => n.ssid.substring(0, chartWidth < 400 ? 6 : 10)),
    y: ['Risk'],
    type: 'heatmap',
    colorscale: [
      [0, '#00ff88'],
      [0.5, '#ffaa00'],
      [1, '#ff4444']
    ],
    showscale: chartWidth > 400,
    colorbar: {
      tickfont: { size: 9, color: '#fff' }
    }
  }];

  const heatmapLayout = {
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: {
      color: '#fff',
      size: chartWidth < 400 ? 9 : 11
    },
    xaxis: {
      tickfont: { size: chartWidth < 400 ? 8 : 10 },
      tickangle: chartWidth < 400 ? -45 : -30
    },
    yaxis: {
      tickfont: { size: chartWidth < 400 ? 9 : 10 }
    },
    height: chartWidth < 400 ? 120 : 150,
    width: chartWidth,
    margin: { 
      t: 10, 
      b: chartWidth < 400 ? 50 : 60, 
      l: chartWidth < 400 ? 50 : 80, 
      r: chartWidth < 400 ? 10 : 20 
    },
    autosize: true
  };

  const plotConfig = { 
    displayModeBar: false,
    responsive: true
  };

  return (
    <div className="charts-container">
      <div className="chart">
        <h3>Encryption Distribution</h3>
        <Plot
          data={pieData}
          layout={pieLayout}
          config={plotConfig}
          useResizeHandler={true}
          style={{ width: '100%', height: '100%' }}
        />
      </div>

      <div className="chart">
        <h3>Signal Strength</h3>
        <Plot
          data={barData}
          layout={barLayout}
          config={plotConfig}
          useResizeHandler={true}
          style={{ width: '100%', height: '100%' }}
        />
      </div>

      <div className="chart">
        <h3>Risk Heatmap</h3>
        <Plot
          data={heatmapData}
          layout={heatmapLayout}
          config={plotConfig}
          useResizeHandler={true}
          style={{ width: '100%', height: '100%' }}
        />
      </div>
    </div>
  );
}

export default Charts;
