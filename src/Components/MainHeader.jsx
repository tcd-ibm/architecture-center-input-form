import { Header, HeaderName, HeaderNavigation, HeaderGlobalBar } from '@carbon/react';

import useAuth from '@/hooks/useAuth';
import CustomHeaderMenuItem from './CustomHeaderMenuItem';

//TODO replace HeaderName react-router Link component or equivalent
//TODO replace the login and signup links when proper design ready

function MainHeader() {
    const { user, logout } = useAuth();
    const url = 'https://firebasestorage.googleapis.com/v0/b/arch-center.appspot.com/o/logo.png?alt=media&token=9f7ab576-c49a-40ec-879a-152942825667';
    const defaultURL = 'https://firebasestorage.googleapis.com/v0/b/arch-center.appspot.com/o/default.png?alt=media&token=ae21c5b6-a2fc-4cd4-a83a-5ca7fb47a724';

    return (
        <Header aria-label='Amazing SwEng Project'>
            <HeaderName href='/' prefix=''>
                <img src={url} style={{maxWidth: '50px', marginLeft: '15px', marginRight: '10px'}} onError={(event) => event.target.style.display = defaultURL} />
                Project Showcase
            </HeaderName>
            <HeaderNavigation aria-label='Amazing SwEng Project'>
                <CustomHeaderMenuItem href='/add'>
                    Add new project
                </CustomHeaderMenuItem>
                { user?.isAdmin() &&
                    <CustomHeaderMenuItem href='/adminpanel/showcase'>
                        Admin panel
                    </CustomHeaderMenuItem>
                }
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