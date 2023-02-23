import { Header, HeaderName, SkipToContent } from '@carbon/react';
import { HeaderGlobalBar, HeaderGlobalAction } from '@carbon/react';
import { Add, UserAvatar, Star, Bee } from '@carbon/icons-react';

//TODO replace standard hrefs with react-router Link component or equivalent

function MainHeader() {
    return (
        <Header aria-label="Amazing SwEng Project">
            <HeaderName href="/" prefix="Project Showcase:">
                SHOWCASE NAME
            </HeaderName>
            <HeaderGlobalBar aria-label="Amazing SwEng Project">
                <HeaderGlobalAction href="/" aria-label="Favourites">
                    <Star size={20}/>
                </HeaderGlobalAction>
                <HeaderGlobalAction href="/add" aria-label="Add Project">
                    <Add size={20}/>
                </HeaderGlobalAction>
                <HeaderGlobalAction href="/" aria-label="My Profile"
                    tooltipAlignment="end">
                    <UserAvatar size={20}/>
                </HeaderGlobalAction>
            </HeaderGlobalBar>
            
        </Header>
    );
}

export default MainHeader;