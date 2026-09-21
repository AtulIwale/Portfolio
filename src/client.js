import React from 'react';
import {hydrateRoot} from 'react-dom/client';
import App from './App.js';
hydrateRoot(document.getElementById('root'),React.createElement(App,{initialPath:location.pathname}));
