import { Content } from '@carbon/react';
import MainHeader from '@/Components/MainHeader';

import styles from './ErrorPage.module.scss';

function ErrorPage() {
    return (
        <>
        <MainHeader />
        <Content className={styles.mainContainer}>
            <h1>404 Page not found!</h1>
            <br></br><br></br><br></br>
            <h4>Unfortunately, the page you are looking for does not exist.</h4>
            <br></br>
            <h4>Please click <a href='/'>here</a> to return to the Home Page.</h4>
        </Content>
        </>
    );
}

export default ErrorPage;