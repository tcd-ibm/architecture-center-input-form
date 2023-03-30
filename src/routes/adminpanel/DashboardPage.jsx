import { Badge, Events, Book } from '@carbon/icons-react';
import { Heading, Tile } from '@carbon/react';
import { SimpleBarChart } from '@carbon/charts-react';
import styles from './DashboardPage.module.scss';

function DashboardPage() {
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
            height: '700px'
        }
    };

    return (
        <>
        <Heading style={{marginBottom: '20px'}}>Dashboard</Heading>
        <div className={styles.tileContainer}>

            {/*Users*/}
            <Tile style = {{maxWidth: '300px', minWidth: '250px', paddingBottom: '30px', marginBottom: '5px', marginRight: '10px', flex: '33.33%'}}>
                <div className={styles.divCenter}>
                    <Events style = {{height: '60px', width: '40px'}}></Events>
                </div> 
                <h4 style={{textAlign: 'center'}}>Users</h4>
                <h1 style={{textAlign: 'center'}}>103</h1>
            </Tile>

            {/*Projects*/}
            <Tile style = {{maxWidth: '300px', minWidth: '250px', paddingBottom: '30px', marginBottom: '5px', marginRight: '10px', flex: '33.33%'}}>
                <div className={styles.divCenter}>
                    <Book style={{height:'60px', width: '40px'}}></Book>
                </div>
                <h4 style={{textAlign: 'center'}}>Projects</h4>
                <h1 style={{textAlign: 'center'}}>643</h1>
            </Tile>
            

            {/*Sponsors*/}
            <Tile style = {{maxWidth: '300px', minWidth: '250px', paddingBottom: '30px', marginBottom: '5px', marginRight: '10px', flex: '33.33%'}}>
                <div className={styles.divCenter}>
                    <Badge style={{height:'60px', width:'40px'}}></Badge>
                </div>
                <h4 style={{textAlign: 'center'}}>Sponsors</h4>
                <h1 style={{textAlign: 'center'}}>45</h1>
            </Tile>

        </div>

        <div>

            {/*Tags*/}
            <Tile style = {{maxWidth: '920px', minWidth: '850px', paddingBottom: '30px', marginBottom: '50px', marginRight: '10px'}}>
                <h4 style={{textAlign: 'center'}}>Popular Tags</h4>
            </Tile>

            {/*Project Additions*/}
            <Tile style = {{maxWidth: '920px', minWidth: '850px', paddingBottom: '30px', marginBottom: '50px', marginRight: '10px'}}>
                <h4 style={{textAlign: 'center'}}>Showcase Project Additions</h4>
                {/*    <SimpleBarChart 
                    data={state.data}
                    options={state.options}>
    </SimpleBarChart> */}
            </Tile>

        </div>

        </>
    );
}


export default DashboardPage;