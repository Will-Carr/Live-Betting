import React from 'react';
import ReactDOM from 'react-dom';
import Timeline from './timeline';

ReactDOM.render(
  <Timeline url="/api/v1/game/" />,
  document.getElementById('reactEntry'),
);
