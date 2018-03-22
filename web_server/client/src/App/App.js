import 'materialize-css/dist/css/materialize.min.css';
import 'materialize-css/dist/js/materialize.js';
import './App.css'

import logo from './logo.png';
import React from 'react';
import NewsPannel from '../NewsPanel/NewsPanel';

class App extends React.Component {
    render() {
        return (
            <div>
                <img className='logo' src={logo} alt='logo'/>
                <div className='container'>
                    <NewsPannel/>
                </div>
            </div>
        );
    }
}

export default App;