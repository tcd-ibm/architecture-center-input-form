import { Heading, TextInput, IconButton } from '@carbon/react';
import styles from './MyAccountPage.module.scss';
import { Edit } from '@carbon/icons-react';
import axios from 'axios';
import useAuth from '@/hooks/useAuth';
import { useNavigate } from 'react-router';
import { useEffect, useState } from 'react';


function MyProjectsPage() {
    
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
                        Update Email<Edit style={{marginLeft: '10px'}}/>
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
                        Change Password<Edit style={{marginLeft: '10px'}}/>
                    </IconButton>
                </div>

                <div className={styles.mainText}>
                    <p>Account Created Date</p>
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
        </>
    );
}

export default MyProjectsPage;
