import { Content, SideNav, SideNavItems, SideNavLink} from '@carbon/react';
import { Outlet } from 'react-router';
import MainHeader from '@/Components/MainHeader';

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
                <SideNavLink isActive>
                    Showcase settings
                </SideNavLink>
                <SideNavLink>
                    Content settings
                </SideNavLink>
                <SideNavLink>
                    Manage users
                </SideNavLink>
                <SideNavLink>
                    Manage projects
                </SideNavLink>
                <SideNavLink>
                    Statistics
                </SideNavLink>
            </SideNavItems>
            
        </SideNav>
        <Content>
            <Outlet />
        </Content>
        </>
    );
}

export default AdminPanel;