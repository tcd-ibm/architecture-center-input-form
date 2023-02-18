import { Header, HeaderName, HeaderNavigation, HeaderMenuItem, HeaderGlobalBar } from '@carbon/react';

//TODO replace standard hrefs with react-router Link component or equivalent
//TODO replace the login and signup links when proper design ready

function MainHeader() {
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
                <HeaderNavigation>
                    <HeaderMenuItem href="/signup">
                        Sign up
                    </HeaderMenuItem>
                    <HeaderMenuItem href="/login">
                        Log in
                    </HeaderMenuItem>
                </HeaderNavigation>
            </HeaderGlobalBar>
        </Header>
    );
}

export default MainHeader;