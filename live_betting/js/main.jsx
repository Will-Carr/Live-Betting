import React from 'react';
import ReactDOM from 'react-dom';
import AllOdds from './allOdds';

ReactDOM.render(
  <AllOdds url="/api/v1/odds/" />,
  document.getElementById('reactEntry'),
);
