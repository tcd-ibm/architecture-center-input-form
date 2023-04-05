import { Events, Book, Growth } from '@carbon/icons-react';
import { Heading, Tile } from '@carbon/react';
import { SimpleBarChart, DonutChart} from '@carbon/charts-react';
import styles from '@carbon/charts/styles.css';
import styles2 from './DashboardPage.module.scss';

import useAppTheme from '@/hooks/useAppTheme';

function DashboardPage() {
    
    const [theme, setTheme] = useAppTheme();

    const state = {
        data: [
            {
                group: 'a',
                value: 1,
            },
            {
                group: 'b',
                value: 3,
            },
            {
                group: 'c',
                value: 5,
            },
            {
                group: 'd',
                value: 1,
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

    const state2 = {
        data2: [
            {
                group: 'a',
                value: 1,
            },
            {
                group: 'b',
                value: 3,
            },
            {
                group: 'c',
                value: 5,
            },
            {
                group: 'd',
                value: 1,
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
                <h1 style={{textAlign: 'center'}}>103</h1>
            </Tile>

            {/*Projects*/}
            <Tile style = {{maxWidth: '300px', minWidth: '250px', paddingBottom: '30px', marginBottom: '5px', marginRight: '10px', flex: '33.33%'}}>
                <div className={styles2.divCenter}>
                    <Book style={{height:'60px', width: '40px'}}></Book>
                </div>
                <h4 style={{textAlign: 'center'}}>Projects</h4>
                <h1 style={{textAlign: 'center'}}>643</h1>
            </Tile>
            

            {/*Sponsors*/}
            <Tile style = {{maxWidth: '300px', minWidth: '250px', paddingBottom: '30px', marginBottom: '5px', marginRight: '10px', flex: '33.33%'}}>
                <div className={styles2.divCenter}>
                    <Growth style={{height:'60px', width:'40px'}}></Growth>
                </div>
                <h4 style={{textAlign: 'center'}}>Page visits</h4>
                <h1 style={{textAlign: 'center'}}>45</h1>
            </Tile>

        </div>

        <br></br>

        <div className = {styles2.tileContainer}>
            {/*Tags*/}
            <Tile style = {{maxWidth: '450px', minWidth: '400px', paddingBottom: '30px', marginBottom: '50px', marginRight: '10px', flex: '50%'}}>
                <h4 style={{textAlign: 'center'}}>Popular Tags</h4>
                <DonutChart 
                        data={state2.data2}
                        options={state2.options2}>
                </DonutChart>
            </Tile>

            {/*Project Additions*/}
            <Tile style = {{maxWidth: '450px', minWidth: '400px', paddingBottom: '30px', marginBottom: '50px', marginRight: '10px', flex: '50%'}}>
                <h4 style={{textAlign: 'center'}}>Showcase Project Additions</h4>
                <SimpleBarChart 
                    data={state.data}
                    options={state.options}>
                </SimpleBarChart>
            </Tile>

        </div>

        </>
    );
}


export default DashboardPage;