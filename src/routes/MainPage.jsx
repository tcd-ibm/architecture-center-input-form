import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Content } from '@carbon/react';
import styles from './MainPage.module.scss';

import MainHeader from '@/Components/MainHeader';
import ProjectQuerySidePanel from '@/Components/ProjectQuerySidePanel';
import Card from '@/Components/Card';

function MainPage() {

    const [isLoading, setIsLoading] = useState(true);
    const [projects, setProjects] = useState([]);
    const [queryMenuContent, setQueryMenuContent] = useState([]);
    const queryMenuRef = useRef();

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

    const handleFilterChange = () => {
        const params = {
            tags: queryMenuRef.current.selectedTagList.join(',')
        };

        axios.get('/projects', { params }).then(res => {
            setProjects(res.data);
            setIsLoading(false);
        })
        .catch(err => {
            console.log(err);
        });
    };
    
    const handleSearch = () => {
        const searchText = document.querySelector('input').value;
        
        let result = {};
        axios.get('/projects', { searchText }).then(res => {
            result = res.data;
            
            for (let i = 0; i < res.data.length; i++) {    
                if (res.data[i].title.toLowerCase().includes(searchText.toLowerCase()) === false) {
                    delete result[i];    
                }
            }
            
            setProjects(result);
            setIsLoading(false);
        })
        .catch(err => {
            console.log(err);
        });
    };

    return (
        <>
        <MainHeader />
        <ProjectQuerySidePanel menuContent={queryMenuContent} ref={queryMenuRef} onChange={handleFilterChange} />
        
        <Content>
            { isLoading ? <div>Loading...</div> : 
                <div id={styles.cardContainer}>
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