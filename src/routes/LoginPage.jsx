import { useState, useRef } from 'react';
import { Content } from '@carbon/react';
import './LoginPage.scss';

import MainHeader from '@/Components/MainHeader';
import LoginFormEmailStep from '@/Components/LoginFormEmailStep';
import LoginFormPasswordStep from '../Components/LoginFormPasswordStep';

function LoginPage() {

    const [email, setEmail] = useState(null);
    const inputRef = useRef();

    const getEmail = () => {
        if(inputRef.current.validate()) {
            setEmail(inputRef.current.value);
        } else {
            setEmail(null);
        }
    };

    const getPassword = () => {
        if(inputRef.current.validate()) {
            
        }
    }

    return (
        <>
        <MainHeader />
        <Content>
            <div className='loginFormContainer'>
                { email ?
                    <LoginFormPasswordStep email={email} onSubmit={getPassword} ref={inputRef} /> :
                    <LoginFormEmailStep onSubmit={getEmail} ref={inputRef} />
                }
            </div>
        </Content>
        </>
    );
}

export default LoginPage;