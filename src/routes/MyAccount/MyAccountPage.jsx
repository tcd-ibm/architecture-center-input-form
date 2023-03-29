import { Content, Heading, SideNav, SideNavItems, SideNavDivider, SideNavLink, TextInput, IconButton } from '@carbon/react';
import MainHeader from '@/Components/MainHeader';
import styles from './MyAccountPage.module.scss';
import { Edit } from '@carbon/icons-react';
import axios from 'axios';
import useAuth from '@/hooks/useAuth';
import { useNavigate } from 'react-router';
import { useEffect, useState } from 'react';


function MyAccountPage() {
    

    const { user } = useAuth();
    const navigate = useNavigate();
    const [userEmail, setUserEmail] = useState(null);
    const [date, setDate] = useState(null);

    useEffect(() => {
        if(!user) {
            navigate('/login', { replace: true });
            const noUserEmail = 'example@example.com';
            setUserEmail(noUserEmail);
            setDate('0000-00-00');
        } else {
            axios.get('/user/info', { headers: { 'Content-Type': 'application/json', 'Accept': 'application/json', Authorization: `Bearer ${user.accessToken}` } }).then(res => {
                setUserEmail(res.data.email);
                setDate(res.data.created_at.slice(0, 10));
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

            <div className={styles.mainContainer}>
                <Heading className={styles.mainHeading} >User Info</Heading>    
                <div className={styles.mainText}>
                    <p>Email</p>
                    <TextInput
                        labelText=''
                        id='email'
                        className={styles.textBox} 
                        defaultValue={userEmail}
                        readOnly={true}
                        size='lg'
                    />
                    <IconButton href='/account/changeemail' className={styles.icon} label='Edit' kind='ghost' >
                        <Edit/>
                    </IconButton>
                </div>

                <div className={styles.mainText}>
                    <p>Password</p>
                    <TextInput
                        labelText=''
                        id='password'
                        className={styles.textBox} 
                        defaultValue='password'
                        readOnly={true}
                        type='password'
                        size='lg'
                    />
                    <IconButton href='/account/changepassword' className={styles.icon} label='Edit' kind='ghost' >
                        <Edit/>
                    </IconButton>
                </div>

                <div className={styles.mainText}>
                    <p>Created At</p>
                    <TextInput
                        labelText=''
                        id='password'
                        className={styles.textBox} 
                        defaultValue={date}
                        readOnly={true}
                        type='text'
                        size='lg'
                    />
                </div>
                
            </div>
            
            </Content>
        </>
    );
}

export default MyAccountPage;
