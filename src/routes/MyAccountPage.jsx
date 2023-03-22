import { Content, Heading } from '@carbon/react';
import MainHeader from '@/Components/MainHeader';
import styles from './MyAccountPage.module.scss';
import { useRouteError } from 'react-router-dom';

function MyAccountPage() {
    return (
        <>
         <MainHeader />
            <Content className={styles.mainContainer}>
                <Heading>Hello</Heading>    
            </Content>
        </>
    );
}

export default MyAccountPage;
