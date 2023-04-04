import { Content, SideNav, SideNavItems, Theme, Heading } from '@carbon/react';
import { CubeView, Information} from '@carbon/icons-react';
import MainHeader from '@/Components/MainHeader';
import CustomSideNavLink from '@/Components/CustomSideNavLink';
import { Outlet } from 'react-router';
import axios from 'axios';
import useAuth from '@/hooks/useAuth';
import { useEffect, useState } from 'react';
import {Helmet} from 'react-helmet';


function MyAccountPage() {

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
                    <CustomSideNavLink href='user-info' renderIcon={Information}>
                        User Info
                    </CustomSideNavLink>
                    <CustomSideNavLink href='my-projects' renderIcon={CubeView}>
                        My Projects
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

export default MyAccountPage;
