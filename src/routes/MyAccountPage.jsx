import { Content, Heading, Section, SideNav, SideNavItems, SideNavDivider, SideNavLink } from '@carbon/react';
import MainHeader from '@/Components/MainHeader';
import styles from './MyAccountPage.module.scss';

function MyAccountPage() {
    return (
        <>
         <MainHeader />
            <Content>
                
            <SideNav className={styles.sideNav}>
                <SideNavItems >
                    <p1 className={styles.sideNavHeading} >My Account</p1>
                    <SideNavDivider />
                    <SideNavLink href='/account' >User Info</SideNavLink>
                </SideNavItems>
            </SideNav>

            <div className={styles.mainContainer}>
                <Heading>User Info</Heading>    
                <div className={styles.mainText}>
                    <p1>Email: example@gamil.com</p1>
                </div>
            </div>
            
            </Content>
        </>
    );
}

export default MyAccountPage;
