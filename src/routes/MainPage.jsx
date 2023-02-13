import { useState, useEffect } from 'react';
import axios from 'axios';
import { Content } from '@carbon/react';
import './MainPage.scss';

import MainHeader from '../Components/MainHeader';
import ProjectQuerySidePanel from '../Components/ProjectQuerySidePanel';
import Card from '../Components/Card';

function MainPage() {

    const [isLoading, setIsLoading] = useState(true);
    const [projects, setProjects] = useState([]);

    useEffect(() => {
        axios.get('pa/0').then(res => {
            setProjects(res.data);
            setIsLoading(false);
        })
        .catch(err => {
            console.log(err);
        });
    }, []);
    
    return (
        <>
        <MainHeader />
        <ProjectQuerySidePanel />
        <Content>
            { isLoading ? <div>Loading...</div> : 
                <div id="cardContainer">
                    {projects.map((projectData, index) => (
                        <Card projectData={projectData} key={index} />
                    ))}
                </div>
            }
        </Content>
        </>
    );
}

export default MainPage;