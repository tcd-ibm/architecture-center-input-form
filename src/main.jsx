import React from 'react';
import ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider, Outlet, Navigate } from 'react-router-dom';
import axios from 'axios';

// eslint-disable-next-line custom-rules/no-global-css
import './index.scss';

import MainPage from './routes/MainPage';
import AddProjectPage from './routes/AddProjectPage';
import SettingsPage from './routes/SettingsPage';
import EditProjectPage from './routes/EditProjectPage';
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
import MyProjectsPage from './routes/MyAccount/MyProjectsPage';
import UserInfoPage from './routes/MyAccount/UserInfoPage';

import { AuthContextProvider } from '@/hooks/useAuth';

axios.defaults.baseURL = 'http://localhost:5297/api/v1/';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Outlet />,
    errorElement: <ErrorPage />,
    children: [
      {
        index: true,
        element: <MainPage />
      },
      {
        path: 'add',
        element: <AddProjectPage />
      },
      {
        path: 'edit/:projectId',
        element: <EditProjectPage />,
      },
      {
        path: 'settings',
        element: <SettingsPage />
      },
      {
        path: 'login',
        element: <LoginPage />
      },
      {
        path: 'signup',
        element: <SignUpPage />
      },
      {
        path: 'details/:projectId',
        element: <ProjectDetails />,
      },
      {
        path: 'account',
        element: <MyAccountPage />,
        children: [
          {
            index: true,
            element: <Navigate to='user-info' replace={true} />
          },
          {
            path: 'user-info',
            element: <UserInfoPage />
          },
          {
            path: 'my-projects',
            element: <MyProjectsPage />
          }
        ]
      },
      {
        path: 'adminpanel',
        element: <AdminPanel />,
        children: [
          {
            index: true,
            element: <Navigate to='dashboard' replace={true} />
          },
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
