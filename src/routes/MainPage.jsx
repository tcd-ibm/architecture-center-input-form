import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Content, Theme } from '@carbon/react';
import styles from './MainPage.module.scss';
import {Helmet} from 'react-helmet';

import MainHeader from '@/Components/MainHeader';
import ProjectQuerySidePanel from '@/Components/ProjectQuerySidePanel';
import Card from '@/Components/Card';
import FeaturedCard from '../Components/FeaturedCard';

function MainPage() {

    const [isLoading, setIsLoading] = useState(true);
    const [projects, setProjects] = useState([]);
    const [queryMenuContent, setQueryMenuContent] = useState([]);
    const queryMenuRef = useRef();

    const stored = localStorage.getItem('toggleDarkMode');
    const color=(stored==='true' ? '161616': 'white');

    useEffect(() => {
        axios.get('/tags').then(res => {
            const content = res.data.map(item => ({
                title: item.categoryName,
                tags: item.tags.map(tagItem => ({id: String(tagItem.tagId), name: tagItem.tagName}))
            }));
            setQueryMenuContent(content);
        })
        .catch(err => {
            console.log(err);
        });
    }, []);

    useEffect(() => {
        axios.get('/projects').then(res => {
            setProjects(res.data);
            setIsLoading(false);
        })
        .catch(err => {
            console.log(err);
        });
    }, []);


    const handleSearchAndFilterChange = () => {
        const params = {
            keyword: document.querySelector('input').value,
            tags: queryMenuRef.current.selectedTagList.join(',')
        };

        axios.get('./projects', { params }).then(res => {
            setProjects(res.data);
            setIsLoading(false);
        })
        .catch(err => {
            console.log(err);
        });
    };

    return (
        <>
        <Theme theme ={stored==='true' ? 'g100' : 'white'}>
            <Helmet>
                <style>{'body { background-color:#'+ color + '; }'}</style> 
            </Helmet>
            <MainHeader />
            <ProjectQuerySidePanel menuContent={queryMenuContent} ref={queryMenuRef} onChange={handleSearchAndFilterChange} />
            
            <Content>
                { isLoading ? <div>Loading...</div> : 
                    <div id={styles.cardContainer}>
                        <FeaturedCard project={projects[0]} />
                        {projects.map((projectData, index) => (
                            <Card projectData={projectData} key={index} />
                        ))}
                    </div>
                }
            </Content>
        </Theme>
        </>
    );
}

export default MainPage;