import { Header, HeaderName, HeaderNavigation, HeaderGlobalBar } from '@carbon/react';

import useAuth from '@/hooks/useAuth';
import CustomHeaderMenuItem from './CustomHeaderMenuItem';

//TODO replace HeaderName react-router Link component or equivalent
//TODO replace the login and signup links when proper design ready

function MainHeader() {
    const { user, logout } = useAuth();

    return (
        <Header aria-label='Amazing SwEng Project'>
            <HeaderName href='/' prefix=''>
                Amazing SwEng Project
            </HeaderName>
            <HeaderNavigation aria-label='Amazing SwEng Project'>
                <CustomHeaderMenuItem href='/add'>
                    Add new project
                </CustomHeaderMenuItem>
            </HeaderNavigation>
            <HeaderGlobalBar>
                { user &&
                    <HeaderNavigation aria-label='Account options'>
                        <CustomHeaderMenuItem onClick={logout}>
                            Log out
                        </CustomHeaderMenuItem>
                    </HeaderNavigation>
                }
                { !user &&
                    <HeaderNavigation aria-label='Account options'>
                        <CustomHeaderMenuItem href='/signup'>
                            Sign up
                        </CustomHeaderMenuItem>
                        <CustomHeaderMenuItem href='/login'>
                            Log in
                        </CustomHeaderMenuItem>
                    </HeaderNavigation>
                }
            </HeaderGlobalBar>
        </Header>
    );
}

export default MainHeader;