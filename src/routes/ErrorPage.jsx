import { Content, Heading, Section} from '@carbon/react';
import MainHeader from '@/Components/MainHeader';
import styles from './ErrorPage.module.scss';

function ErrorPage() {
    return (
        <>
        <MainHeader />
            <Content className={styles.mainContainer}>
                    <Heading className={styles.notFound}>404 Page not found!</Heading>
                    <p class='text' >Unfortunately, the page you are looking for does not exist.</p>
                    <p class='text' >Please click <a href='/'>here</a> to return to the Home Page.</p>
            </Content>
        </>
    );
}

export default ErrorPage;