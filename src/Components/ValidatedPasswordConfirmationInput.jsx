import { useState, useRef, useImperativeHandle, forwardRef } from 'react';
import { TextInput } from '@carbon/react';

function ValidatedPasswordConfirmationInput(props, ref) {
    const { primaryRef, ...remainingProps } = props;

    const inputRef = useRef();
    useImperativeHandle(ref, () => ({
        validate: () => {
            return validate();
        },
        get value() {
            return inputRef.current.value;
        }
    }), []);

    const [invalidText, setInvalidText] = useState(null);

    const validate = () => {
        if(inputRef.current.value !== primaryRef.current.value) {
            setInvalidText('Passwords do not match');
            return false;
        }
        setInvalidText(null);
        return true;
    };

    return (
        <TextInput 
            type='password'
            labelText='Confirm password'
            invalid={Boolean(invalidText)}
            invalidText={invalidText}
            ref={inputRef}
            onChange={validate}
            {...remainingProps}
        />
    );
}

export default forwardRef(ValidatedPasswordConfirmationInput);