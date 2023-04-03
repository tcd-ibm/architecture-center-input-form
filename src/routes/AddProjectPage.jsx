import MainHeader from '@/Components/MainHeader';

import useAuth from '@/hooks/useAuth';
import EditProject from '../Components/EditProject';
import { useEffect } from 'react';
import { useNavigate } from 'react-router';

function AddProjectPage() {

    const { user } = useAuth();
    const navigate = useNavigate();
    const isEditPage = false;

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
        <MainHeader />
        <EditProject projectData={project} user={user} isEdit={isEditPage}/>
        </>
    );
}

export default AddProjectPage;