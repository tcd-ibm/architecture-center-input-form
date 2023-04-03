import { Header, HeaderNavigation, HeaderGlobalBar, OverflowMenu } from '@carbon/react';
import { User, DocumentAdd, InventoryManagement } from '@carbon/icons-react';

import useAuth from '@/hooks/useAuth';
import { CustomHeaderMenuItem, CustomHeaderName, CustomOverflowMenuItem } from './CustomCarbonNavigation';

function MainHeader() {
    const { user, logout } = useAuth();

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
                    <DocumentAdd style={{marginLeft: '10px', top: '2px', position: 'relative'}}/>
                </CustomHeaderMenuItem>
                <CustomHeaderMenuItem href='/settings'>
                    Settings
                </CustomHeaderMenuItem>
                { user?.isAdmin() &&
                    <CustomHeaderMenuItem href='/adminpanel/dashboard'>
                        Admin panel
                        <InventoryManagement style={{marginLeft: '10px', top: '2px', position: 'relative'}}/>
                    </CustomHeaderMenuItem>
                }
            </HeaderNavigation>
            <HeaderGlobalBar>
                { user &&
                    <OverflowMenu size='lg' renderIcon={User} flipped={true} style={{boxShadow: 'none'}} ariaLabel='My Account'>
                            <CustomOverflowMenuItem itemText='My Account' href='/account' />
                            <CustomOverflowMenuItem itemText='Log out' onClick={logout} />
                    </OverflowMenu>
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