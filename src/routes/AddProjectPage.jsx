import MainHeader from '@/Components/MainHeader';

import useAuth from '@/hooks/useAuth';
import EditProject from '../Components/EditProject';
import { useEffect } from 'react';
import { useNavigate } from 'react-router';

import { Theme } from '@carbon/react';
import { Helmet } from 'react-helmet';

function AddProjectPage() {

    const { user } = useAuth();
    const navigate = useNavigate();
    const isEditPage = false;

    const stored = localStorage.getItem('toggleDarkMode');
    const color=(stored==='true' ? '161616': 'white');

    const project = {
        title: null,
        link: null,
        description: null,
        content: null,
        date: new Date(),
        tags: []
    };

    return (
        <>
        <Theme theme ={stored==='true' ? 'g100' : 'white'}>
            <Helmet>
                <style>{'body { background-color:#'+ color + '; }'}</style> 
            </Helmet>
            <MainHeader />
            <EditProject projectData={project} user={user} isEdit={isEditPage}/>
        </Theme>
        </>
    );
}

export default AddProjectPage;