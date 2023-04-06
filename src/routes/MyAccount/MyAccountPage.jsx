import { Content, SideNav, SideNavItems, Tile} from '@carbon/react';
import { CubeView, Information} from '@carbon/icons-react';
import MainHeader from '@/Components/MainHeader';
import CustomSideNavLink from '@/Components/CustomSideNavLink';
import { Outlet } from 'react-router';
import ProjectManager from '../../Components/ProjectManager';
import styles from './MyAccountPage.module.scss';

function MyAccountPage() {

    return (
        <>
            <MainHeader />
            <Content style={{width: '80%', marginLeft: 'auto', marginRight: 'auto'}}>
                <Tile style={{padding:'40px'}}>
                <Outlet/>
                </Tile>
                <div style={{marginBottom: '40px'}}></div>
                <ProjectManager/>
            </Content>
        </>
    );
}

export default MyAccountPage;
