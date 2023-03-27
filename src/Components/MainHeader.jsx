import { Header, HeaderNavigation, HeaderGlobalBar, HeaderGlobalAction, HeaderPanel,
    Switcher, SwitcherDivider, SwitcherItem } from '@carbon/react';
import { User, DocumentAdd } from '@carbon/icons-react';

import useAuth from '@/hooks/useAuth';
import { CustomHeaderGlobalAction, CustomHeaderMenuItem, CustomHeaderName, CustomSwitcherItem } from './CustomCarbonNavigation';
import { useState } from 'react';

function MainHeader() {
    const { user, logout } = useAuth();
    const [open, setOpen] = useState(false);

    return (
        <Header aria-label='Amazing SwEng Project'>
            <CustomHeaderName href='/' prefix=''>
                Amazing SwEng Project
            </CustomHeaderName>
            <HeaderGlobalBar>
                { user &&
                    <HeaderNavigation aria-label='Account options'>
                        <CustomHeaderGlobalAction href='/add' aria-label='Add new project'>
                            <DocumentAdd />
                        </CustomHeaderGlobalAction>
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
                    <CustomSwitcherItem aria-label='' href='/account'>
                        My Account
                    </CustomSwitcherItem>
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