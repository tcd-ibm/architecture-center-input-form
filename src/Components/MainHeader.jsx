import { Header, HeaderName, HeaderNavigation, HeaderGlobalBar, HeaderGlobalAction, HeaderPanel,
    Switcher, SwitcherDivider, SwitcherItem } from '@carbon/react';
import { User, DocumentAdd } from '@carbon/icons-react';

import useAuth from '@/hooks/useAuth';
import { CustomHeaderMenuItem } from './CustomCarbonNavigation';
import { useState } from 'react';

//TODO replace HeaderName react-router Link component or equivalent
//TODO replace the login and signup links when proper design ready
function MainHeader() {
    const { user, logout } = useAuth();
    const [open, setOpen] = useState(false);

    return (
        <Header aria-label='Amazing SwEng Project'>
            <HeaderName href='/' prefix=''>
                Amazing SwEng Project
            </HeaderName>
            <HeaderGlobalBar>
                { user &&
                    <HeaderNavigation aria-label='Account options'>
                        <HeaderGlobalAction href='/add' aria-label='Add new project'>
                            <DocumentAdd />
                        </HeaderGlobalAction>
                        <HeaderGlobalAction isActive={open}
                                            aria-label='Account'
                                            tooltipAlignment='end'
                                            onClick={() => setOpen(!open)}>
                            <User />
                        </HeaderGlobalAction>
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
            {
            <HeaderPanel aria-label='' expanded={open}>
                <Switcher aria-label='' >
                    <SwitcherItem aria-label='' href='/account'>
                        My Account
                    </SwitcherItem>
                    <SwitcherDivider />
                    <SwitcherItem aria-label='' onClick={() => {
                        setOpen(false);
                        logout();
                        }}>
                        Log out
                    </SwitcherItem>
                </Switcher>
            </HeaderPanel>}
        </Header>
    );
}

export default MainHeader;