import MainHeader from '@/Components/MainHeader';
import { useState, useEffect } from 'react';
import { useParams } from 'react-router';
import axios from 'axios';
import useAuth from '@/hooks/useAuth';
import EditProject from '../Components/EditProject';
import { Theme } from '@carbon/react';
import {Helmet} from 'react-helmet';

function EditProjectPage() {

    const { user } = useAuth();
    const { projectId } = useParams();
    const isEditPage = true;

    const [isLoading, setIsLoading] = useState(true);
    const [project, setProject] = useState();
    const stored = localStorage.getItem('toggleDarkMode');
    const color=(stored==='true' ? '161616': 'white');

    useEffect(() => {
        axios.get(`/project/${projectId}`).then(res => {
            setProject(res.data);
            setIsLoading(false);
        })
        .catch(err => {
            console.log(err);
        });
    }, [projectId]);

    return (
        <>
        <Theme theme ={stored==='true' ? 'g100' : 'white'}>
            <Helmet>
                <style>{'body { background-color:#'+ color + '; }'}</style> 
            </Helmet>
        <MainHeader />
        { isLoading ? <div>Loading...</div> : 
            <EditProject projectData={project} user={user} isEdit={isEditPage}/>
        }
        </Theme>
        </>
    );
}

export default EditProjectPage;