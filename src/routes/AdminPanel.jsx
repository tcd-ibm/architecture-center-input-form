import { Content, SideNav, SideNavItems } from '@carbon/react';
import { Outlet } from 'react-router';

import MainHeader from '@/Components/MainHeader';
import CustomSideNavLink from '@/Components/CustomSideNavLink';

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
            <CustomSideNavLink href='dashboard'>
                    Dashboard
                </CustomSideNavLink>
                <CustomSideNavLink href='showcase'>
                    Showcase settings
                </CustomSideNavLink>
                <CustomSideNavLink href='content'>
                    Content settings
                </CustomSideNavLink>
                <CustomSideNavLink href='users'>
                    Manage users
                </CustomSideNavLink>
                <CustomSideNavLink href='projects'>
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