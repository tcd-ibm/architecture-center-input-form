import { useState, useRef, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import qs from 'qs';
import { Content } from '@carbon/react';
import styles from './LoginPage.module.scss';

import MainHeader from '@/Components/MainHeader';
import LoginFormEmailStep from '@/Components/LoginFormEmailStep';
import LoginFormPasswordStep from '@/Components/LoginFormPasswordStep';

import AuthContext from '@/context/AuthContext';
import User from '@/utils/User';

function LoginPage() {

    const [user, setUser] = useContext(AuthContext);
    const [email, setEmail] = useState(null);
    const [errorText, setErrorText] = useState(null);
    const inputRef = useRef();
    const navigate = useNavigate();

    const getEmail = () => {
        if(inputRef.current.validate()) {
            setEmail(inputRef.current.value);
        } else {
            setEmail(null);
        }
    };

    const getPassword = async () => {
        if(inputRef.current.validate()) {
            
            const requestData = {
                username: email,
                password: inputRef.current.value
            };

            try {
                const response = await axios.post('/user/token', qs.stringify(requestData));
                setUser(new User(response.data.access_token));
                navigate('/', {replace: true});
            } catch(error) {
                if(error?.response?.status === 401) {
                    setErrorText('Incorrect email or password. Try again.');
                } else {
                    setErrorText('Unknown error occurred. Try again.');
                }
            }

        }
    };

    if(user) {
        navigate('/', {replace: true});
    }

    return (
        <>
        <MainHeader />
        <Content>
            <div className={styles.loginFormContainer}>
                { email ?
                    <LoginFormPasswordStep email={email} onSubmit={getPassword} errorText={errorText} setErrorText={setErrorText} ref={inputRef} /> :
                    <LoginFormEmailStep onSubmit={getEmail} ref={inputRef} />
                }
            </div>
        </Content>
        </>
    );
}

export default LoginPage;