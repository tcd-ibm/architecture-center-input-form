import { Content, SideNav, SideNavItems } from '@carbon/react';
import { Outlet } from 'react-router';

import MainHeader from '@/Components/MainHeader';
import CustomSideNavLink from '@/Components/CustomSideNavLink';
import { Cube, Dashboard, Events, Settings } from '@carbon/icons-react';

function AdminPanel() {
    return (
        <>
        <MainHeader />
        <SideNav
            isFixedNav
            expanded={true}
            isChildOfHeader={false}
            aria-label='Admin panel navigation'>

            <SideNavItems>
            <CustomSideNavLink href='dashboard' renderIcon={Dashboard}>
                    Dashboard
                </CustomSideNavLink>
                <CustomSideNavLink href='showcase' renderIcon={Settings}>
                    Showcase settings
                </CustomSideNavLink>
                <CustomSideNavLink href='content' renderIcon={Settings}>
                    Content settings
                </CustomSideNavLink>
                <CustomSideNavLink href='users' renderIcon={Events}>
                    Manage users
                </CustomSideNavLink>
                <CustomSideNavLink href='projects' renderIcon={Cube}>
                    Manage projects
                </CustomSideNavLink>
                <CustomSideNavLink href='statistics'>
                    Statistics
                </CustomSideNavLink>
            </SideNavItems>
            
        </SideNav>
        <Content>
            <Outlet />
        </Content>
        </>
    );
}

export default AdminPanel;