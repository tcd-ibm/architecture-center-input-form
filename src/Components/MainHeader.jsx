import { useContext } from 'react';
import { Header, HeaderName, HeaderNavigation, HeaderMenuItem, HeaderGlobalBar } from '@carbon/react';

import AuthContext from '../context/AuthContext';

//TODO replace standard hrefs with react-router Link component or equivalent
//TODO replace the login and signup links when proper design ready

function MainHeader() {
    const [user, setUser] = useContext(AuthContext);

    return (
        <Header aria-label="Amazing SwEng Project">
            <HeaderName href="/" prefix="">
                Amazing SwEng Project
            </HeaderName>
            <HeaderNavigation aria-label="Amazing SwEng Project">
                <HeaderMenuItem href="/add">
                    Add new project
                </HeaderMenuItem>
            </HeaderNavigation>
            <HeaderGlobalBar>
                { user &&
                    <HeaderNavigation aria-label="Account options">
                        <HeaderMenuItem onClick={() => setUser(null)}>
                            Log out
                        </HeaderMenuItem>
                    </HeaderNavigation>
                }
                { !user &&
                    <HeaderNavigation aria-label="Account options">
                        <HeaderMenuItem href="/signup">
                            Sign up
                        </HeaderMenuItem>
                        <HeaderMenuItem href="/login">
                            Log in
                        </HeaderMenuItem>
                    </HeaderNavigation>
                }
            </HeaderGlobalBar>
        </Header>
    );
}

export default MainHeader;