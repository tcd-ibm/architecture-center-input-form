import { Content, Heading, Section, SideNav, SideNavItems, SideNavDivider, SideNavLink, TextInput } from '@carbon/react';
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
                <Heading className={styles.mainHeading} >User Info</Heading>    
                <div className={styles.mainText}>
                    <p1>Email</p1>
                    <TextInput
                    className={styles.textBox} 
                    defaultValue='example@example.com'
                    readOnly={true}
                    size='lg'
                    />
                </div>

                <div className={styles.mainText}>
                    <p1>Password</p1>
                    <TextInput
                    className={styles.textBox} 
                    defaultValue='password'
                    readOnly={true}
                    type='password'
                    size='lg'
                    />
                </div>
                
            </div>
            
            </Content>
        </>
    );
}

export default MyAccountPage;
