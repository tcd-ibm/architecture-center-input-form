import { Content, SideNav, SideNavItems, SideNavDivider, SideNavLink } from '@carbon/react';
import MainHeader from '@/Components/MainHeader';
import styles from './MyAccountPage.module.scss';
import axios from 'axios';
import useAuth from '@/hooks/useAuth';
import { useNavigate } from 'react-router';
import { useEffect } from 'react';


function ChangePasswordPage() {
    

    const { user } = useAuth();
    const navigate = useNavigate();
    
    useEffect(() => {
        if(!user) {
            navigate('/login', { replace: true });
        } else {
            axios.get('/user/info', { headers: { 'Content-Type': 'application/json', 'Accept': 'application/json', Authorization: `Bearer ${user.accessToken}` } }).then(res => {
                // console.log(res.data);
            })
            .catch(err => {
                console.log(err);
            }); 
        }

    }, [navigate, user]);

    return (
        <>
         <MainHeader />
            <Content>
                
            <SideNav
                isFixedNav
                expanded={true}
                isChildOfHeader={false}
                aria-label='Side navigation'
                className={styles.sideNav}
            >
                <SideNavItems >
                    <p className={styles.sideNavHeading}>My Account</p>
                    <SideNavDivider />
                    <SideNavLink href='/account' >User Info</SideNavLink>
                </SideNavItems>
            </SideNav>

            <div>
                
            </div>
            
            </Content>
        </>
    );
}

export default ChangePasswordPage;
