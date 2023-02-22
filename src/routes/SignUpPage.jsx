import { useState, useRef, useContext, useEffect } from 'react'
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

import MainHeader from '@/Components/MainHeader';
import EmailInput from '@/Components/EmailInput';
import PasswordInput from '@/Components/PasswordInput';

import { ArrowRight } from '@carbon/icons-react';
import { Content, Tile, Form, Button, InlineNotification, Link } from '@carbon/react';

import AuthContext from '@/context/AuthContext';
import User from '@/utils/User';

import './loginPage.scss';

function SignUpPage() {

    const [user, setUser] = useContext(AuthContext);

    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')

    const [emailErrorText, setEmailErrorText] = useState(null);
    const [passwordErrorText, setPasswordErrorText] = useState(null);
    const [confirmPasswordErrorText, setConfirmPasswordErrorText] = useState(null);

    const [canSubmit, setCanSubmit] = useState(false);

    const emailRef = useRef(null);
    const passwordRef = useRef(null);
    const confirmPasswordRef = useRef(null);

    const handleEmailInputChange = (value) => {
        emailRef.current.validate() ? setEmail(value) : setEmail(null)
    }
    const handlePasswordInputChange = (value) => {
        passwordRef.current.validate() ? setPassword(value) : setPassword(null)
    }
    const handleConfirmPasswordInputChange = (value) => {
        confirmPasswordRef.current.validate() ? setConfirmPassword(value) : setConfirmPassword(null)
    }

    useEffect(() => {
        if (!(Boolean)(email && password && confirmPassword)) {
            setCanSubmit(false)
            return
        }
        if (password !== confirmPassword) {
            setConfirmPasswordErrorText('Passwords do not match')
            setCanSubmit(false)
            return
        }
        setConfirmPasswordErrorText(null)
        setCanSubmit(true)
    }, [email, password, confirmPassword])

    const navigate = useNavigate();
    const onSubmitWrapper = async event => {

        event.preventDefault()

        if (!email || !password || !confirmPassword) return

        const requestData = {
            email: email,
            username: '',
            password: password
        }
        try {
            const response = await axios.post('/user/signup', requestData, { headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' } });
            setUser(new User(response.data.access_token));

            navigate('/', { replace: true });
        } catch (error) {
            console.error(error);
            if (error?.response?.status === 400) {
                const detail = error.response.data.detail
                if (detail == 'Email registered already')
                    setEmailErrorText(detail)
                else if (detail == 'Password invalid, should be at least 8 characters')
                    setPasswordErrorText(detail)
                else
                    setConfirmPasswordErrorText(detail)
            }
        }
    }

    return (
        <>
            <MainHeader />
            <Content style={{ display: "flex", justifyContent: "center" }}>
                <Tile className='loginFormTile'>
                    <Form onSubmit={onSubmitWrapper}>
                        {user ? <p>Logged in already? <Link href='/'>index</Link></p> : <></>}
                        <div className='loginInnerContainer'>
                            {emailErrorText ?
                                <InlineNotification
                                    height='2rem'
                                    title='Error:'
                                    subtitle={emailErrorText}
                                    lowContrast={true}
                                    className='notification'
                                    onCloseButtonClick={() => setEmailErrorText(null)}
                                />
                                :
                                <div className='notificationPlaceholder'></div>
                            }
                            <EmailInput
                                className="input"
                                id="email"
                                labelText="Email"
                                placeholder="Enter your Email"
                                onInputChange={handleEmailInputChange}
                                ref={emailRef}
                            />
                            {passwordErrorText ?
                                <InlineNotification
                                    height='2rem'
                                    title='Error:'
                                    subtitle={passwordErrorText}
                                    lowContrast={true}
                                    className='notification'
                                    onCloseButtonClick={() => setPasswordErrorText(null)}
                                />
                                :
                                <div className='notificationPlaceholder'></div>
                            }
                            <PasswordInput
                                labelText="Password"
                                className="input"
                                id="password"
                                placeholder="Enter your password"
                                onInputChange={handlePasswordInputChange}
                                ref={passwordRef}
                            />
                            {confirmPasswordErrorText ?

                                <InlineNotification
                                    height='2rem'
                                    title='Error:'
                                    subtitle={confirmPasswordErrorText}
                                    lowContrast={true}
                                    className='notification'
                                    onCloseButtonClick={() => setConfirmPasswordErrorText(null)}
                                />
                                :
                                <div className='notificationPlaceholder'></div>
                            }
                            <PasswordInput
                                labelText="Confirm Password"
                                className="input"
                                id="confirmPassword"
                                placeholder="Re-enter your password"
                                onInputChange={handleConfirmPasswordInputChange}
                                ref={confirmPasswordRef}
                            />
                        </div>
                        <div className='buttonContainer'>
                            <div className='flexColumn'></div>
                            <div className='flexColumn'>
                                <Button renderIcon={ArrowRight} className='button' type='submit' disabled={!canSubmit}>Register</Button>
                            </div>
                        </div>
                    </Form>
                </Tile>
            </Content>
        </>
    )
}

export default SignUpPage;