import React from 'react';
import ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import axios from 'axios';
import './index.scss';

import MainPage from './routes/MainPage';
import AddProjectPage from './routes/AddProjectPage';
import LoginPage from './routes/LoginPage';
import ErrorPage from './routes/ErrorPage';

import AuthContextProvider from './context/AuthContextProvider';

axios.defaults.baseURL = 'http://localhost:5297/api/v1/';

const router = createBrowserRouter([
  {
    path: '/',
    element: <MainPage />,
    errorElement: <ErrorPage />
  },
  {
    path: '/add',
    element: <AddProjectPage />
  },
  {
    path: '/login',
    element: <LoginPage />
  }
]);
 
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <AuthContextProvider>
      <RouterProvider router={router} />
    </AuthContextProvider>
  </React.StrictMode>
);
