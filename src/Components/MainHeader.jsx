import { useState } from 'react';
import { Header, HeaderNavigation, HeaderGlobalBar, HeaderPanel, Switcher, SwitcherDivider } from '@carbon/react';
import { User, DocumentAdd } from '@carbon/icons-react';

import useAuth from '@/hooks/useAuth';
import { CustomHeaderGlobalAction, CustomHeaderMenuItem, CustomHeaderName, CustomSwitcherItem } from './CustomCarbonNavigation';

function MainHeader() {
    const { user, logout } = useAuth();

    const [open, setOpen] = useState(false);

    const url = 'https://firebasestorage.googleapis.com/v0/b/arch-center.appspot.com/o/logo.png?alt=media&token=9f7ab576-c49a-40ec-879a-152942825667';
    const defaultURL = 'https://firebasestorage.googleapis.com/v0/b/arch-center.appspot.com/o/default.png?alt=media&token=ae21c5b6-a2fc-4cd4-a83a-5ca7fb47a724';

    return (
        <Header aria-label='Amazing SwEng Project'>
            <CustomHeaderName href='/' prefix=''>
                <img src={url} style={{maxWidth: '50px', marginLeft: '15px', marginRight: '10px'}} onError={(event) => event.target.style.display = defaultURL} />
                Project Showcase
            </CustomHeaderName>
            <HeaderNavigation aria-label='Amazing SwEng Project'>
                <CustomHeaderMenuItem href='/add'>
                    Add new project
                </CustomHeaderMenuItem>
                { user?.isAdmin() &&
                    <CustomHeaderMenuItem href='/adminpanel/dashboard'>
                        Admin panel
                    </CustomHeaderMenuItem>
                }
            </HeaderNavigation>
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