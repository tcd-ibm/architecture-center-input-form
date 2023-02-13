import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import axios from 'axios'
import './index.scss'

import MainPage from './routes/MainPage';
import AddProjectPage from './routes/AddProjectPage';

axios.defaults.baseURL = 'http://localhost:5297/api/v1/'

const router = createBrowserRouter([
  {
    path: '/',
    element: <MainPage />,
  },
  {
    path: '/add',
    element: <AddProjectPage />,
  }
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
