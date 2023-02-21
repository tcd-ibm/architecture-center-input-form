import { Content } from '@carbon/react';
import MainHeader from '@/Components/MainHeader';
import PageNotFound from '@/Components/PageNotFound';

function ErrorPage() {
    return (
        <>
        <MainHeader />
        <Content>
            <PageNotFound />
        </Content>
        </>
    );
}

export default ErrorPage;