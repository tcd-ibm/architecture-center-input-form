import { forwardRef } from 'react';
import { Tile, FluidForm, InlineNotification, Checkbox, Button } from '@carbon/react';
import { ArrowRight } from '@carbon/icons-react';
import styles from './LoginFormGeneric.module.scss';

import EmailInput from './EmailInput';
import PasswordInput from './PasswordInput';

function LoginFormGeneric(props, ref) {
    const {subheadingContentNode, errorText, setErrorText, inputType, rememberIdCheckbox, buttonText, onSubmit} = props;

    const onSubmitWrapper = event => {
        event.preventDefault();
        onSubmit();
    };

    return (
        <Tile className={styles.loginFormTile}>
            <FluidForm onSubmit={onSubmitWrapper}>
                <div className={styles.innerContainer}>
                    <p className={styles.heading}>Log in</p>
                    <p>{subheadingContentNode}</p>
                    
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
                    
                    { inputType === 'email' &&
                        <EmailInput autoFocus className={styles.input} id='email' ref={ref} />
                    }
                    { inputType === 'password' &&
                        <PasswordInput autoFocus className={styles.input} id='password' ref={ref} />
                    }

                    { rememberIdCheckbox ?
                        <div><Checkbox labelText='Remember ID' id='remember-id-checkbox' className={styles.checkbox} /></div> :
                        <div style={{visibility: 'hidden'}}><Checkbox labelText='Remember ID' id='remember-id-checkbox' className={styles.checkbox} /></div>
                    }
                    
                </div>
                <div className={styles.buttonContainer}>
                    <div className={styles.flexColumn}></div>
                    <div className={styles.flexColumn}>
                        <Button renderIcon={ArrowRight} className={styles.button} type='submit'>{buttonText}</Button>
                    </div>
                </div>
            </FluidForm>
        </Tile>
    );
}

export default forwardRef(LoginFormGeneric);