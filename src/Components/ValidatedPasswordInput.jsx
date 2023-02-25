import { useState, useRef, useImperativeHandle, forwardRef } from "react";
import { TextInput } from "@carbon/react";

function ValidatedPasswordInput(props, ref) {

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
        if (!inputRef.current.value) {
            setInvalidText('Password is required');
            return false;
        }
        if (inputRef.current.value.length < 8) {
            setInvalidText('Password must be at least 8 characters');
            return false;
        } 
        setInvalidText(null);
        return true;
    };

    return (
        <TextInput 
            type='password'
            labelText='Password'
            invalid={Boolean(invalidText)}
            invalidText={invalidText}
            ref={inputRef}
            onBlur={validate}
            {...props}
        />
    );
}

export default forwardRef(ValidatedPasswordInput);