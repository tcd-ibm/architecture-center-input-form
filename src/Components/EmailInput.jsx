import { useState, useRef, useImperativeHandle, forwardRef } from 'react';
import { TextInput } from '@carbon/react';

function EmailInput(props, ref) {

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
        if(!inputRef.current.value) {
            setInvalidText('Email is required');
            return false;
        }
        if(!/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(inputRef.current.value)) {
            setInvalidText('Enter a valid email address');
            return false;
        }
        setInvalidText(null);
        return true;
    };

    return (
        <TextInput 
            type='email'
            labelText='Email'
            invalid={Boolean(invalidText)}
            invalidText={invalidText}
            ref={inputRef}
            onBlur={validate}
            {...props}
        />
    );
}

export default forwardRef(EmailInput);