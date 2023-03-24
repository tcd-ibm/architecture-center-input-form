import { Content, Heading, SideNav, SideNavItems, SideNavDivider, SideNavLink, TextInput, IconButton } from '@carbon/react';
import MainHeader from '@/Components/MainHeader';
import styles from './MyAccountPage.module.scss';
import { Edit } from '@carbon/icons-react';
import axios from 'axios';
import useAuth from '@/hooks/useAuth';
import { useNavigate } from 'react-router';
import { useEffect, useState, useRef } from 'react';


function MyAccountPage() {
    

    const { user } = useAuth();
    const navigate = useNavigate();
    let userInfo = [];
    userInfo.email = '';

    useEffect(() => {
        if(!user) {
            navigate('/login', { replace: true });
        }

        axios.get('/user/info', { headers: { 'Content-Type': 'application/json', 'Accept': 'application/json', Authorization: `Bearer ${user.accessToken}` } }).then(res => {
            userInfo = res.data;
            console.log(userInfo);
        })
        .catch(err => {
            console.log(err);
        });

    }, [navigate, user]);

    return (
        <>
         <MainHeader />
            <Content>
                
            <SideNav className={styles.sideNav}>
                <SideNavItems >
                    <p1 className={styles.sideNavHeading}>My Account</p1>
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
                        defaultValue={userInfo.email}
                        readOnly={true}
                        size='lg'
                    />
                    <IconButton className={styles.icon} label='Edit' kind='ghost' >
                        <Edit/>
                    </IconButton>
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
                    <IconButton className={styles.icon} label='Edit' kind='ghost' >
                        <Edit/>
                    </IconButton>
                </div>
                
            </div>
            
            </Content>
        </>
    );
}

export default MyAccountPage;
