import { Content, SideNav, SideNavItems, } from '@carbon/react';
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
            <Content>
                <Outlet />
                <ProjectManager/>
            </Content>
        </>
    );
}

export default MyAccountPage;
