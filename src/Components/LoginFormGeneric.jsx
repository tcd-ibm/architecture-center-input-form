import { forwardRef } from 'react';
import { Tile, FluidForm, InlineNotification, Checkbox, Button } from '@carbon/react';
import { ArrowRight } from '@carbon/icons-react';
import './LoginFormGeneric.scss';

import EmailInput from './EmailInput';
import PasswordInput from './PasswordInput';

function LoginFormGeneric(props, ref) {
    const {subheadingContentNode, errorText, setErrorText, inputType, rememberIdCheckbox, buttonText, onSubmit} = props;

    const onSubmitWrapper = event => {
        event.preventDefault();
        onSubmit();
    };

    return (
        <Tile className='loginFormTile'>
            <FluidForm onSubmit={onSubmitWrapper}>
                <div className='innerContainer'>
                    <p className='heading'>Log in</p>
                    <p>{subheadingContentNode}</p>
                    
                    { errorText ?
                        <InlineNotification
                            title='Error:'
                            subtitle={errorText}
                            lowContrast={true}
                            className='notification'
                            onCloseButtonClick={() => setErrorText(null)}
                        />
                        :
                        <div className='notificationPlaceholder'></div>
                    }
                    
                    { inputType === 'email' &&
                        <EmailInput autoFocus className='input' id='email' ref={ref} />
                    }
                    { inputType === 'password' &&
                        <PasswordInput autoFocus className='input' id='password' ref={ref} />
                    }

                    { rememberIdCheckbox ?
                        <div><Checkbox labelText='Remember ID' id='remember-id-checkbox' className='checkbox' /></div> :
                        <div style={{visibility: 'hidden'}}><Checkbox labelText='Remember ID' id='remember-id-checkbox' className='checkbox' /></div>
                    }
                    
                </div>
                <div className='buttonContainer'>
                    <div className='flexColumn'></div>
                    <div className='flexColumn'>
                        <Button renderIcon={ArrowRight} className='button' type='submit'>{buttonText}</Button>
                    </div>
                </div>
            </FluidForm>
        </Tile>
    );
}

LoginFormGeneric = forwardRef(LoginFormGeneric);

export default LoginFormGeneric;