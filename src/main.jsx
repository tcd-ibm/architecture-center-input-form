import React from 'react';
import ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import axios from 'axios';

// eslint-disable-next-line custom-rules/no-global-css
import './index.scss';

import MainPage from './routes/MainPage';
import AddProjectPage from './routes/AddProjectPage';
import SettingsPage from './routes/SettingsPage';
import LoginPage from './routes/LoginPage';
import ErrorPage from './routes/ErrorPage';
import SignUpPage from './routes/SignUpPage';
import ProjectDetails from './routes/ProjectDetails';
import ShowcaseSettingsPage from './routes/adminpanel/ShowcaseSettingsPage';
import ContentSettingsPage from './routes/adminpanel/ContentSettingsPage';
import ManageUsersPage from './routes/adminpanel/ManageUsersPage';
import ManageProjectsPage from './routes/adminpanel/ManageProjectsPage';
import DashboardPage from './routes/adminpanel/DashboardPage';
import AdminPanel from './routes/AdminPanel';
import MyAccountPage from './routes/MyAccount/MyAccountPage';
import ChangePasswordPage from './routes/MyAccount/ChangePasswordPage';

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
    path: '/settings',
    element: <SettingsPage />
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
    path: '/details/:projectId',
    element: <ProjectDetails />,
  },
  {
    path: '/account',
    element: <MyAccountPage />,
  },
  {
    path: '/account/changepassword',
    element: <ChangePasswordPage />
  },
  {
    path: '/adminpanel',
    element: <AdminPanel />,
    children: [
      {
        path: 'showcase',
        element: <ShowcaseSettingsPage />
      },
      {
        path: 'content',
        element: <ContentSettingsPage />
      },
      {
        path: 'users',
        element: <ManageUsersPage />
      },
      {
        path: 'projects',
        element: <ManageProjectsPage />
      },
      {
        path: 'dashboard',
        element: <DashboardPage />
      }
    ]
  }
]);
 
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <AuthContextProvider>
      <RouterProvider router={router} />
    </AuthContextProvider>
  </React.StrictMode>
);
