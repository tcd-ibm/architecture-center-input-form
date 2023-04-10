import { useState, useEffect } from 'react';
import axios from 'axios';

import { Events, Book, Growth } from '@carbon/icons-react';
import { Heading, Tile } from '@carbon/react';
import { SimpleBarChart, DonutChart} from '@carbon/charts-react';
import styles from '@carbon/charts/styles.css';
import styles2 from './DashboardPage.module.scss';

import useAuth from '@/hooks/useAuth';
import { useNavigate } from 'react-router';
import useAppTheme from '@/hooks/useAppTheme';

function DashboardPage() {
    
    const [theme, setTheme] = useAppTheme();
    const [page, setPage] = useState(1);
    const [pageSize, setPageSize] = useState(10);

    const [numberOfUsers, setNumberOfUsers] = useState([]);
    const [numberOfProjects, setNumberOfProjects] = useState([]);
    const [numberOfVisits, setNumberOfVisits] = useState([]);
    const [recentProjectsData, setRecentProjectsData] = useState();
    const [popularTags, setPopularTags] = useState();


    const { user } = useAuth();
    const navigate = useNavigate();

    function onLoad() {
        if(!user) {
            navigate('/login', { replace: true });
            return;
        }
        const requestConfig = { 
            params: {
                page: page,
                per_page: pageSize
            },
            headers: { 
                'Content-Type': 'application/json', 
                'Accept': 'application/json', 
                'Authorization': `Bearer ${user.accessToken}` 
            } 
        };

        axios.get('/admin/users/total', requestConfig).then(res => {
            setNumberOfUsers(res.data);
            console.log(res.data);
        })
        .catch(err => {
            console.log(err);
        });

        axios.get('/admin/projects/total', requestConfig).then(res => {
            setNumberOfProjects(res.data);
            console.log(res.data);
        })
        .catch(err => {
            console.log(err);
        });

        axios.get('/admin/projects/total/visit', requestConfig).then(res => {
            setNumberOfVisits(res.data);
            console.log(res.data);
        })
        .catch(err => {
            console.log(err);
        });

        axios.get('/admin/tags/popular/5', requestConfig).then(res => {
            const state2 = {
                data2: [
                    {
                        group: res.data[0].tag,
                        value: res.data[0].count
                    },
                    {
                        group: res.data[1].tag,
                        value: res.data[1].count
                    },
                    {
                        group: res.data[2].tag,
                        value: res.data[2].count
                    },
                    {
                        group: res.data[3].tag,
                        value: res.data[3].count
                    },
                    {
                        group: res.data[4].tag,
                        value: res.data[4].count
                    }
                ],
                options2: {
                    title: '',
                    resizable: true,
                    donut: {
                        center: {
                            label: 'Tags',
                        }
                    },
                    height: '300px',
                    theme: theme
                }
            };
            setPopularTags(state2);
            //console.log(res.data);
            //console.log(state2);
        })
        .catch(err => {
            console.log(err);
        });
          

        axios.get('/admin/projects/recent/5', requestConfig).then(res => {
            const state = {
                data: [
                    {
                        group: res.data[0].date,
                        value: res.data[0].count
                    },
                    {
                        group: res.data[1].date,
                        value: res.data[1].count
                    },
                    {
                        group: res.data[2].date,
                        value: res.data[2].count
                    },
                    {
                        group: res.data[3].date,
                        value: res.data[3].count
                    },
                    {
                        group: res.data[4].date,
                        value: res.data[4].count
                    }
                ],
                options: {
                    title: '',
                    axes: {
                        left: {
                            mapsTo: 'group',
                            scaleType: 'labels',
                        },
                        bottom: {
                            mapsTo: 'value',
                        }
                    },
                    height: '300px',
                    theme: theme
                }
            };
            setRecentProjectsData(state);
            //console.log(res.data);
            //console.log(state);
        })
        .catch(err => {
            console.log(err);
        });
    }

    //console.log(recentProjectsData);

    useEffect(onLoad, [ user, page, pageSize]);




    return (
        <>
        <Heading style={{marginBottom: '20px'}}>Dashboard</Heading>
        <div className = {styles2.tileContainer}>

            {/*Users*/}
            <Tile style = {{maxWidth: '300px', minWidth: '250px', paddingBottom: '30px', marginBottom: '5px', marginRight: '10px', flex: '33.33%'}}>
                <div className={styles2.divCenter}>
                    <Events style = {{height: '60px', width: '40px'}}></Events>
                </div> 
                <h4 style={{textAlign: 'center'}}>Users</h4>
                <h1 style={{textAlign: 'center'}}>{numberOfUsers.total}</h1>
            </Tile>

            {/*Projects*/}
            <Tile style = {{maxWidth: '300px', minWidth: '250px', paddingBottom: '30px', marginBottom: '5px', marginRight: '10px', flex: '33.33%'}}>
                <div className={styles2.divCenter}>
                    <Book style={{height:'60px', width: '40px'}}></Book>
                </div>
                <h4 style={{textAlign: 'center'}}>Projects</h4>
                <h1 style={{textAlign: 'center'}}>{numberOfProjects.total}</h1>
            </Tile>
            

            {/*Sponsors*/}
            <Tile style = {{maxWidth: '300px', minWidth: '250px', paddingBottom: '30px', marginBottom: '5px', marginRight: '10px', flex: '33.33%'}}>
                <div className={styles2.divCenter}>
                    <Growth style={{height:'60px', width:'40px'}}></Growth>
                </div>
                <h4 style={{textAlign: 'center'}}>Page visits</h4>
                <h1 style={{textAlign: 'center'}}>{numberOfVisits.total}</h1>
            </Tile>

        </div>

        <br></br>

        <div className = {styles2.tileContainer}>
            {/*Tags*/}
            <Tile style = {{maxWidth: '450px', minWidth: '400px', paddingBottom: '30px', marginBottom: '50px', marginRight: '10px', flex: '50%'}}>
                <h4 style={{textAlign: 'center'}}>Popular Tags</h4>
                <DonutChart 
                        data={popularTags.data2}
                        options={popularTags.options2}>
                </DonutChart>
            </Tile>

            {/*Project Additions*/}
            <Tile style = {{maxWidth: '450px', minWidth: '400px', paddingBottom: '30px', marginBottom: '50px', marginRight: '10px', flex: '50%'}}>
                <h4 style={{textAlign: 'center'}}>Showcase Project Additions</h4>
                <SimpleBarChart
                    data={recentProjectsData.data}
                    options={recentProjectsData.options}>
                </SimpleBarChart>
            </Tile>

        </div>

        </>
    );
}


export default DashboardPage;