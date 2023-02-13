import { Header, HeaderName, HeaderNavigation, HeaderMenuItem } from '@carbon/react';

//TODO replace standard hrefs with react-router Link component or equivalent

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
        </Header>
    );
}

export default MainHeader;