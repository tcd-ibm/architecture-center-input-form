import { useState, useRef, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

import MainHeader from '@/Components/MainHeader';
import EmailInput from '@/Components/EmailInput';
import ValidatedPasswordInput from '../Components/ValidatedPasswordInput';
import ValidatedPasswordConfirmationInput from '../Components/ValidatedPasswordConfirmationInput';

import { ArrowRight } from '@carbon/icons-react';
import { Content, Tile, Button, InlineNotification, Link, FluidForm } from '@carbon/react';

import AuthContext from '@/context/AuthContext';
import User from '@/utils/User';

import styles from './SignUpPage.module.scss';

function SignUpPage() {

    const [user, setUser] = useContext(AuthContext);

    const [errorText, setErrorText] = useState(null);

    const emailRef = useRef(null);
    const passwordRef = useRef(null);
    const confirmPasswordRef = useRef(null);

    const navigate = useNavigate();

    const handleSubmit = async event => {

        event.preventDefault();

        if(!emailRef.current.validate()) return;
        if(!passwordRef.current.validate()) return;
        if(!confirmPasswordRef.current.validate()) return;

        const requestData = {
            email: emailRef.current.value,
            username: '',
            password: passwordRef.current.value
        };

        try {
            const response = await axios.post('/user/signup', requestData, { headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' } });
            setUser(new User(response.data.access_token));

            navigate('/', { replace: true });
        } catch (error) {
            console.error(error);
            if (error?.response?.status === 400) {
                const detail = error.response.data.detail;
                if (detail === 'Email registered already')
                    setErrorText(detail);
                else if (detail === 'Password invalid, should be at least 8 characters')
                    setErrorText(detail);
                else
                    setErrorText(detail);
            }
        }
    };

    if(user) {
        navigate('/', { replace: true });
    }

    return (
        <>
        <MainHeader />
        <Content className={styles.signupFormContainer}>
            <Tile className={styles.signupFormTile}>
                <FluidForm onSubmit={handleSubmit}>
                    <div className={styles.innerContainer}>
                        <p className={styles.heading}>Sign up</p>
                        <p>Already have an account? <Link href='/login'>Log in</Link></p>

                        { errorText ?
                            <InlineNotification
                                title='Error:'
                                subtitle={errorText}
                                lowContrast={true}
                                className={styles.notification}
                                onCloseButtonClick={() => setErrorText(null)}
                            />
                            :
                            <div className={styles.notificationPlaceholder}></div>
                        }

                        <EmailInput 
                            autoFocus 
                            className={styles.input}
                            id='email' 
                            ref={emailRef} 
                        />

                        <ValidatedPasswordInput 
                            className={styles.input} 
                            id='password' 
                            ref={passwordRef} 
                            onChange={() => confirmPasswordRef.current.validate()} 
                        />

                        <ValidatedPasswordConfirmationInput 
                            className={styles.input}
                            id='passwordConfirmation' 
                            primaryRef={passwordRef} 
                            ref={confirmPasswordRef} 
                        />

                    </div>
                    <div className={styles.buttonContainer}>
                        <div className={styles.flexColumn}></div>
                        <div className={styles.flexColumn}>
                            <Button renderIcon={ArrowRight} className={styles.button} type='submit'>Sign up</Button>
                        </div>
                    </div>
                </FluidForm>
            </Tile>
        </Content>
        </>
    );
}

export default SignUpPage;