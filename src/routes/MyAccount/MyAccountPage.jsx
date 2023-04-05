import { Content, SideNav, SideNavItems, } from '@carbon/react';
import { CubeView, Information} from '@carbon/icons-react';
import MainHeader from '@/Components/MainHeader';
import CustomSideNavLink from '@/Components/CustomSideNavLink';
import { Outlet } from 'react-router';

function MyAccountPage() {

    return (
        <>
            <MainHeader />
            {/* <SideNav
                isFixedNav
                expanded={true}
                isChildOfHeader={false}
                aria-label='Admin panel navigation'>

                <SideNavItems>
                    <CustomSideNavLink href='user-info' renderIcon={Information}>
                        User Info
                    </CustomSideNavLink>
                    <CustomSideNavLink href='my-projects' renderIcon={CubeView}>
                        My Projects
                    </CustomSideNavLink>
                </SideNavItems>

            </SideNav> */}
            <Content>
                <Outlet />
            </Content>
        </>
    );
}

export default MyAccountPage;
