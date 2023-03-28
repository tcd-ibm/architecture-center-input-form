import React from 'react';
import ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import axios from 'axios';

// eslint-disable-next-line custom-rules/no-global-css
import './index.scss';

import MainPage from './routes/MainPage';
import AddProjectPage from './routes/AddProjectPage';
import LoginPage from './routes/LoginPage';
import ErrorPage from './routes/ErrorPage';
import SignUpPage from './routes/SignUpPage';
import ProjectDetails from './routes/ProjectDetails';
import MyAccountPage from './routes/MyAccountPage';

import { AuthContextProvider } from '@/hooks/useAuth';

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
  },
  {
    path: '/signup',
    element: <SignUpPage />
  },
  {
    path: '/account',
    element: <MyAccountPage />
  },
  {
    path: '/details/:projectId',
    element: <ProjectDetails />,
  }
]);
 
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <AuthContextProvider>
      <RouterProvider router={router} />
    </AuthContextProvider>
  </React.StrictMode>
);
