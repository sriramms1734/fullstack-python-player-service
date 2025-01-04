import React from 'react';
import ReactDOM from 'react-dom/client';
import './styling/index.css';
import { MyProvider } from './components/MyProvider';
import PlayerMain from './components/PlayerMain';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <MyProvider>
        <PlayerMain/>
    </MyProvider>
  </React.StrictMode>
);
