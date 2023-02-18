import { forwardRef } from 'react';
import { Tile, FluidForm, InlineNotification, Checkbox, Button } from '@carbon/react';
import { ArrowRight } from '@carbon/icons-react';
import './LoginFormGeneric.scss';

import EmailInput from './EmailInput';
import PasswordInput from './PasswordInput';

function LoginFormGeneric(props, ref) {
    const {subheadingContentNode, errorText, inputType, rememberIdCheckbox, buttonText, onSubmit} = props;

    return (
        <Tile className='loginFormTile'>
            <FluidForm onSubmit={onSubmit}>
                <div className='innerContainer'>
                    <p className='heading'>Log in</p>
                    <p>{subheadingContentNode}</p>
                    
                    { errorText ?
                        <InlineNotification
                            title='Error:'
                            subtitle={errorText}
                            lowContrast={true}
                            className='notification'
                        />
                        :
                        <div className='notificationPlaceholder'></div>
                    }
                    
                    { inputType === 'email' &&
                        <EmailInput className='input' ref={ref} />
                    }
                    { inputType === 'password' &&
                        <PasswordInput className='input' ref={ref} />
                    }

                    { rememberIdCheckbox ?
                        <div><Checkbox labelText='Remember ID' id='remember-id-checkbox' className='checkbox' /></div> :
                        <div style={{visibility: 'hidden'}}><Checkbox id='remember-id-checkbox' className='checkbox' /></div>
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