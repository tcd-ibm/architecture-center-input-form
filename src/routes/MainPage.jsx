import { useState } from 'react';
import { Content } from '@carbon/react';
import './MainPage.scss';

import MainHeader from '../Components/MainHeader';
import ProjectQuerySidePanel from '../Components/ProjectQuerySidePanel';
import Card from '../Components/Card';

function MainPage() {

    return (
        <>
        <MainHeader />
        <ProjectQuerySidePanel />
        <Content>
            <div id="cardContainer">
                <Card />
            </div>
        </Content>
        </>
    );
}

export default MainPage;