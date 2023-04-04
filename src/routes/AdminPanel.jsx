import { Content, SideNav, SideNavItems, Theme } from '@carbon/react';
import { Outlet } from 'react-router';

import MainHeader from '@/Components/MainHeader';
import CustomSideNavLink from '@/Components/CustomSideNavLink';
import { Cube, Dashboard, Events, Settings } from '@carbon/icons-react';
import { Helmet } from 'react-helmet';

function AdminPanel() {

    const stored = localStorage.getItem('toggleDarkMode');
    const color=(stored==='true' ? '161616': 'white');

    return (
        <>
        <Theme theme ={stored==='true' ? 'g100' : 'white'}>
            <Helmet>
                <style>{'body { background-color:#'+ color + '; }'}</style> 
            </Helmet>
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
                </SideNavItems>

            </SideNav>
            <Content>
                <Outlet />
            </Content>
        </Theme>
        </>
    );
}

export default AdminPanel;