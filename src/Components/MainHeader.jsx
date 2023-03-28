import { useState } from 'react';
import { Header, HeaderNavigation, HeaderGlobalBar, HeaderPanel, Switcher, SwitcherDivider } from '@carbon/react';
import { User, DocumentAdd } from '@carbon/icons-react';

import useAuth from '@/hooks/useAuth';
import { CustomHeaderGlobalAction, CustomHeaderMenuItem, CustomHeaderName, CustomSwitcherItem } from './CustomCarbonNavigation';

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
                        <CustomHeaderGlobalAction isActive={open}
                            aria-label='Account'
                            tooltipAlignment='end'
                            onClick={() => setOpen(!open)}>
                            <User />
                        </CustomHeaderGlobalAction>
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
                    <CustomSwitcherItem aria-label='' 
                        onClick={() => {
                            setOpen(false);
                            logout();
                        }}>
                        Log out
                    </CustomSwitcherItem>
                </Switcher>
            </HeaderPanel>}
        </Header>
    );
}

export default MainHeader;