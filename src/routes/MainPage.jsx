import { useState, useEffect } from 'react';
import axios from 'axios';
import { Content } from '@carbon/react';
import './MainPage.scss';

import MainHeader from '@/Components/MainHeader';
import ProjectQuerySidePanel from '@/Components/ProjectQuerySidePanel';
import Card from '@/Components/Card';

function MainPage() {

    const [isLoading, setIsLoading] = useState(true);
    const [projects, setProjects] = useState([]);
    const [queryMenuContent, setQueryMenuContent] = useState([]);

    const [filteredProjects, setFilteredProjects] = useState([]);
    
    const [filterTagList, setFilterTagList] = useState([]);
    const [pageNum, setPageNum] = useState(0);

    useEffect(() => {
        axios.get('pa/0').then(res => {
            setProjects(res.data);
            setIsLoading(false);
        })
        .catch(err => {
            console.log(err);
        });
    }, []);

    useEffect(() => {
        const fetchMenuContent = async () => [
            {
                title: 'Solution',
                tags: (await axios.get('solution')).data.map(item => ({id: item.sid, name: item.sname}))
            },
            {
                title: 'Vertical',
                tags: (await axios.get('vertical')).data.map(item => ({id: item.vid, name: item.vname}))
            },
            {
                title: 'Product',
                tags: (await axios.get('product')).data.map(item => ({id: item.pid, name: item.pname}))
            },
            {
                title: 'Type',
                tags: (await axios.get('type')).data.map(item => ({id: item.tid, name: item.typename}))
            }
        ];

        fetchMenuContent().then(menuContent => setQueryMenuContent(menuContent))
            .catch(err => console.log(err));
    }, []);

    useEffect(() => {
        if(filterTagList.length > 0) {
            let results = [];
            for (const tag of filterTagList) {
                for (const item of projects) {
                if (item.ProductType.includes(tag) || item.Solutions.includes(tag) || item.Vertical.includes(tag) || item.Product.includes(tag)) {
                    results.push(item);
                }
                }
            }
            setFilteredProjects(results);
        } else {
            setFilteredProjects(projects);
        }
    }, [projects, filterTagList]);

    const handleFilterChange = (event) => {
        const { checked, id } = event.target;
        if (checked) {
            setFilterTagList([...filterTagList, id]);
        } else {
            setFilterTagList(filterTagList.filter((item) => item !== id));
        }

    }
    
    return (
        <>
        <MainHeader />
        <ProjectQuerySidePanel menuContent={queryMenuContent} filterTagList={filterTagList} handleFilterChange={handleFilterChange} />
        <Content>
            { isLoading ? <div>Loading...</div> : 
                <div id="cardContainer">
                    {filteredProjects.slice(pageNum*10,(pageNum*10)+10).map((projectData, index) => (
                        <Card projectData={projectData} key={index} />
                    ))}
                </div>

            }

            { isLoading ? null: 
                <div id="pagination">
                       <button className={pageNum == 0? "btnInvisible": " "} onClick={()=>{ 
                        if (pageNum > 0) {
                        setPageNum(pageNum -1);
                        console.log(filteredProjects.length);
                        }
                    }}>
                        Back
                    </button>
               
                    <p>
                        { "page " + (pageNum+1) + " of " + Math.ceil(filteredProjects.length/10)}
                    </p>

                    <button className={pageNum +1 == Math.ceil(filteredProjects.length/10)? "btnInvisible": " "} onClick={()=>{
                        if (pageNum+1 < Math.ceil(filteredProjects.length/10)) {
                            setPageNum(pageNum+1);
                        }

                    }}>
                        Next
                    </button>
                </div>


            }
        </Content>
        </>
    );
}

export default MainPage;