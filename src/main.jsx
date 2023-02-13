import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.scss'
import axios from 'axios'

axios.defaults.baseURL = 'http://localhost:5297/api/v1/'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
