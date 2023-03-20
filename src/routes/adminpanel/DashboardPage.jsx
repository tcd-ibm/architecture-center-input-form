import { Badge, Events, Book } from '@carbon/icons-react';
import { Heading, Tile } from '@carbon/react';
import styles from './DashboardPage.module.scss';

function DashboardPage() {
    return (
        <>
        <Heading style={{marginBottom: '20px'}}>Dashboard</Heading>
        <div className={styles.tileContainer}>

            {/*Users*/}
            <Tile style = {{maxWidth: '300px', paddingBottom: '30px', marginBottom: '5px', marginRight: '10px', flex: '33.33%'}}>
                <div className={styles.divCenter}>
                    <Events style = {{height: '60px', width: '40px'}}></Events>
                </div> 
                <h4 style={{textAlign: 'center'}}>Users</h4>
                <h1 style={{textAlign: 'center'}}>103</h1>
            </Tile>

            {/*Projects*/}
            <Tile style = {{maxWidth: '300px', paddingBottom: '30px', marginBottom: '5px', marginRight: '10px', flex: '33.33%'}}>
                <div className={styles.divCenter}>
                    <Book style={{height:'60px', width: '40px'}}></Book>
                </div>
                <h4 style={{textAlign: 'center'}}>Projects</h4>
                <h1 style={{textAlign: 'center'}}>643</h1>
            </Tile>
            

            {/*Sponsors*/}
            <Tile style = {{maxWidth: '300px', paddingBottom: '30px', marginBottom: '5px', marginRight: '10px', flex: '33.33%'}}>
                <div className={styles.divCenter}>
                    <Badge style={{height:'60px', width:'40px'}}></Badge>
                </div>
                <h4 style={{textAlign: 'center'}}>Sponsors</h4>
                <h1 style={{textAlign: 'center'}}>45</h1>
            </Tile>

        </div>
        </>
    );
}


export default DashboardPage;