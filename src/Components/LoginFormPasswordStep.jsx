import { forwardRef } from 'react';
import { Link } from '@carbon/react';

import LoginFormGeneric from './LoginFormGeneric';

function LoginFormPasswordStep(props, ref) {
    const { email, onSubmit, errorText, setErrorText } = props;

    const componentProps = {
        subheadingContentNode: <>Logging in as {email} <Link href='/login'>Not you?</Link></>,
        inputType: 'password',
        rememberIdCheckbox: false, 
        backLink: '/login',
        buttonText: 'Log in',
        onSubmit: onSubmit,
        errorText,
        setErrorText
    };

    return (
        <LoginFormGeneric {...componentProps} ref={ref} />
    );
}

export default forwardRef(LoginFormPasswordStep);